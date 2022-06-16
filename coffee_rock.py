import pandas
import plotly.express as px
import lib
import data
from dash import Dash, dcc, html, Input, Output
pandas.options.plotting.backend = "plotly"

### Chargement des données
energy_cons_by_source = data.get_energy_cons_by_source()
sea_level = data.get_sea_level()
change_deg = data.get_change_deg()
comparison = data.get_comparison()
energy_by_sector = data.get_energy_by_sector()

### Affichage

app = Dash(__name__, suppress_callback_exceptions=True)

energy_by_sector_fig = px.bar(energy_by_sector, x="Year", y="Consumption", color="Category")

degree_map = lib.map(change_deg, 'tas_anom')
sea_level_map  = lib.map(sea_level, 'total')
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
        dcc.Dropdown(energy_cons_by_source['Date'].unique(), id="date", value="2016")]),

    dcc.Graph(
        id='energy-by-source',
    ),

    dcc.Graph(
        id='energy-consumption',
    ),

    html.H2(children='Global energy consumption by sector'),

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

@app.callback(
    Output('gdp', 'figure'),
    Output('energy-consumption', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = lib.select_country(country_name, comparison)
    energy_data = lib.select_country(country_name, energy_cons_by_source)
    return (comparison_data.plot(x='Date', y=data), px.line(energy_data, x="Date", y="Value", color="Source", title='Energy consumption by source over time'))

@app.callback(
    Output('energy-by-source', 'figure'),
    Input('country-name', 'value'),
    Input('date', 'value'))
def update_energy(country_name, date):
    energy_data = lib.select_date(date, energy_cons_by_source)
    energy_data = lib.select_country(country_name, energy_data)
    return px.pie(energy_data, values="Value", names="Source")

if __name__ == '__main__':
    app.run_server(debug=True)
