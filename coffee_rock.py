from lib2to3.pytree import convert
from dash import Dash, dcc, html, Input, Output
import netCDF4 as nc
import sqlite3
import xarray as xr
import pandas
import plotly.express as px
conn = sqlite3.connect("test.db")
def netcdf_to_csv(input, output):
    xr.open_dataset(input).to_dataframe().to_csv(output)

netcdf_to_csv("CMIP6 - Mean temperature (T) Change deg C - Medium Term (2041-2060) SSP5-8.5 (rel. to 1995-2014) - Annual (34 models).nc", "change_deg.csv")

def table_from_csv(file, name):
    df = pandas.read_csv(file)
    df.to_sql(name, conn, if_exists="replace")

table_from_csv("change_deg.csv", "change_deg")

def columns_to_values(df, index, name, value_name="Value", end_index=None):
    return df.melt(id_vars=df.iloc[:, 0:index], 
        var_name=name,
        value_vars=df.iloc[:, index:end_index],
        value_name=value_name)

def select_country(name, df):
    return df[df['Country Name']==name]

gdp = pandas.read_csv("API_NY.GDP.MKTP.KD_DS2_en_csv_v2_4150850.csv")
gdp = columns_to_values(gdp, 4, 'Date', 'GDP')

energy = pandas.read_csv("Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv")
# TODO: INSERT 0s WHEN CELL IS EMPTY
energy = columns_to_values(energy, 1, 'Source', end_index=11)

ghg = pandas.read_csv("Greenhouse Gas per capita, 1850-2015 (in tCO2eq).csv", sep=";", decimal=",")
ghg = columns_to_values(ghg, 1, 'Country','Emissions', end_index=6)

app = Dash(__name__, suppress_callback_exceptions=True)

def rename_column(df, name):
    df.rename( columns={'Unnamed: 0':name}, inplace=True )

def select_date(date, df):
    return df[df["Date"]==date]

def select_source(source, df):
    return df[df["Source"]==source]

def convert_date(df):
    df["Date"] = df['Date'].astype(str).str[:4]
    return df

rename_column(energy, "Date")
convert_date(energy)
rename_column(ghg, "Date")
convert_date(ghg)
energyFig = px.line(energy, x="Date", y="Value", title='Energy production by source over time', color="Source")

comparison = gdp.merge(ghg, left_on=["Date", "Country Name"], right_on=["Date", "Country"])

degree_map = px.density_mapbox(pandas.read_csv("change_deg.csv"), lat='lat', lon='lon', z='tas_anom', radius=6,
                        opacity=0.5, zoom=0.4,
                        mapbox_style="stamen-terrain")
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

    dcc.Graph(
        id='gdp'
    ),
    html.H2(children='Degree change'),

    dcc.Graph(
        id='degree-map',
        figure=degree_map
    ),
    html.H2(children='Global energy production'),


    dcc.Graph(
        id='energy-by-source-time',
        figure=energyFig
    ),


    html.Div(children=['''
    ''', html.Label('Year'),
        dcc.Dropdown(energy['Date'].unique(), id="date", value="2016")]),

    dcc.Graph(
        id='energy-by-source',
    ),
])


pandas.options.plotting.backend = "plotly"

@app.callback(
    Output('gdp', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = select_country(country_name, comparison)
    return comparison_data.plot(x='Date', y=data)

@app.callback(
    Output('energy-by-source', 'figure'),
    Input('date', 'value'))
def update_energy(date):
    energy_data = select_date(date, energy)
    return px.pie(energy_data, values="Value", names="Source")

@app.callback(
    Output('energy-source-time', 'figure'),
    Input('source', 'value'))
def update_energy_source(source):
    energy_data = select_source(source, energy)
    return px.line(energy_data, x="Date", y="Value", title='Energy production by source over time')

if __name__ == '__main__':
    app.run_server(debug=True)
