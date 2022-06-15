from lib2to3.pytree import convert
from dash import Dash, dcc, html, Input, Output
import netCDF4 as nc
import sqlite3
import xarray as xr
import pandas
import plotly.express as px
conn = sqlite3.connect("test.db")
# Convertir netcdf en csv
def netcdf_to_csv(input, output):
    xr.open_dataset(input).to_dataframe().to_csv(output)

netcdf_to_csv("CMIP6 - Mean temperature (T) Change deg C - Medium Term (2041-2060) SSP5-8.5 (rel. to 1995-2014) - Annual (34 models).nc", "change_deg.csv")

# Créér une table dans la BD à partir d'un fichier CSV
def table_from_csv(file, name):
    df = pandas.read_csv(file)
    df.to_sql(name, conn, if_exists="replace")

table_from_csv("change_deg.csv", "change_deg")

def columns_to_values(df, index, name, value_name="Value", end_index=None):
    return df.melt(id_vars=df.iloc[:, 0:index], 
        var_name=name,
        value_vars=df.iloc[:, index:end_index],
        value_name=value_name)

# Sélectionner un pays
def select_country(name, df):
    return df[df['Country Name']==name]

gdp = pandas.read_csv("API_NY.GDP.MKTP.KD_DS2_en_csv_v2_4150850.csv")
gdp = columns_to_values(gdp, 4, 'Date', 'GDP')

energy = pandas.read_csv("Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv")
# TODO: INSERT 0s WHEN CELL IS EMPTY
energy = columns_to_values(energy, 1, 'Source', end_index=11)


energy_countries=[
    ("Primary Energy Consumption by source, France, 1980-2016 (in Mtoe).csv", "France"),
    ("Primary Energy Consumption by source, China, 1980-2016 (in Mtoe).csv", "China")
]
energy["Country Name"] = "World"
for val in energy_countries:
    energy_country = pandas.read_csv(val[0])
    energy_country= columns_to_values(energy_country, 1, 'Source', end_index=11)
    energy_country["Country Name"] = val[1]
    energy = pandas.concat([energy, energy_country], axis=0)
sea_level = pandas.read_csv("CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual.csv")

change_deg = pandas.read_csv("change_deg.csv")

ghg = pandas.read_csv("Greenhouse Gas per capita, 1850-2015 (in tCO2eq).csv", sep=";", decimal=",")
ghg = columns_to_values(ghg, 1, 'Country','Emissions', end_index=6)

energy_by_sector = pandas.read_excel("IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx")
energy_by_sector = energy_by_sector[energy_by_sector["Sub-category"] == "Total"]
energy_by_sector = energy_by_sector[energy_by_sector["Region"] == "World"]
energy_by_sector = energy_by_sector[energy_by_sector["Case"] == "Planned Energy Scenario"]
energy_by_sector = energy_by_sector[energy_by_sector["type (Unit)"] == "Supply and demand (EJ)"]
energy_by_sector = energy_by_sector[energy_by_sector["Category"] != "TFEC (excl. non-energy uses)"]
energy_by_sector = energy_by_sector[energy_by_sector["Category"] != "TPES"]


app = Dash(__name__, suppress_callback_exceptions=True)

# Renommer la première colonne sans nom
def rename_column(df, name):
    df.rename( columns={'Unnamed: 0':name}, inplace=True )

def select_date(date, df):
    return df[df["Date"]==date]

def select_source(source, df):
    return df[df["Source"]==source]

# Prendre seulement l'année dans la date
def convert_date(df):
    df["Date"] = df['Date'].astype(str).str[:4]
    return df

def map(df, z):
    return px.density_mapbox(df, lat='lat', lon='lon', z=z, radius=6,
                        opacity=0.5, zoom=0.4,
                        mapbox_style="stamen-terrain")

rename_column(energy, "Date")
convert_date(energy)
rename_column(ghg, "Date")
convert_date(ghg)
comparison = gdp.merge(ghg, left_on=["Date", "Country Name"], right_on=["Date", "Country"])

energy_by_sector_fig = px.pie(energy_by_sector, values=2017, names="Category")

degree_map = map(change_deg, 'tas_anom')
sea_level_map  = map(sea_level, 'total')
print(energy)
app.layout = html.Div(children=[
    html.H1(children='CoffeeRock'),
    html.H2(children='Countries'),

    html.Div(children=['''
    ''', html.Label('Country'),
        dcc.Dropdown(comparison['Country Name'].unique(), id="country-name", value='France')]),

    dcc.Tabs(id='data', value='GDP', children=[
        dcc.Tab(label='GDP', value='GDP'),
        dcc.Tab(label='Emissions', value='Emissions'),
    ]),
    
        # Fonctionnalité: Afficher les GES en fonction du pays
    # Fonctionnalité: Causes des émissions GES
    dcc.Graph(
        id='gdp'
    ),

    html.H2(children='Energy consumption'),

        # Afficher la production d’énergies
    html.Div(children=['''
    ''', html.Label('Year'),
        dcc.Dropdown(energy['Date'].unique(), id="date", value="2016")]),

    dcc.Graph(
        id='energy-by-source',
    ),

    dcc.Graph(
        id='energy-consumption',
    ),

    html.H2(children='Global energy consumption by sector (2017)'),

    dcc.Graph(
        id='energy-by-sector',
        figure=energy_by_sector_fig
    ),

    html.H2(children='Degree change'),
    dcc.Graph(
        id='degree-map',
        figure=degree_map
    ),


    html.H2(children='Sea level change'),

    dcc.Graph(
        id='sea-level-map',
        figure=sea_level_map
    ),

], style={'font-family': 'Arial'})


pandas.options.plotting.backend = "plotly"

@app.callback(
    Output('gdp', 'figure'),
    Output('energy-consumption', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = select_country(country_name, comparison)
    energy_data = energy[energy["Country Name"] == country_name]
    return (comparison_data.plot(x='Date', y=data), px.line(energy_data, x="Date", y="Value", color="Source", title='Energy consumption by source over time'))

@app.callback(
    Output('energy-by-source', 'figure'),
    Input('country-name', 'value'),
    Input('date', 'value'))
def update_energy(country_name, date):
    energy_data = select_date(date, energy)
    energy_data = select_country(country_name, energy_data)
    return px.pie(energy_data, values="Value", names="Source")

if __name__ == '__main__':
    app.run_server(debug=True)
