from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import lib
import data

pd.options.plotting.backend = "plotly"

### Chargement des données
sea_level = data.get_sea_level()
energy_cons_by_source = data.get_energy_cons_by_source()
energy_prod_by_source = data.get_energy_prod_by_source()
change_deg = data.get_change_deg()
comparison = data.get_comparison()
energy_cons_by_sector = data.get_energy_cons_by_sector()

#list_df_energyproduction_country = [df_energyproduction_china,df_energyproduction_denmark,df_energyproduction_france,df_energyproduction_germany,df_energyproduction_india,df_energyproduction_ivorycoast,df_energyproduction_unitedstates]

### Affichage

app = Dash(__name__, suppress_callback_exceptions=True)

energy_cons_by_sector_fig = px.bar(energy_cons_by_sector, x="Year", y="Consumption", color="Category")

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
        id='comparison_cons'
    ),

    dcc.Graph(
        id='comparison_prod'
    ),

    html.H2(children='Energy consumption'),

    # Afficher la consommation d’énergies
    html.Div(children=['''
    ''', html.Label('Year'),
        dcc.Dropdown(energy_cons_by_source['Date'].unique(), id="date_cons", value="2016")]),

    dcc.Graph(
        id='energy-cons-by-source',
    ),

    dcc.Graph(
        id='energy-consumption',
    ),

    html.H2(children='Global energy consumption by sector'),

    dcc.Graph(
        id='energy-cons-by-sector',
        figure=energy_cons_by_sector_fig
    ),

    html.H2(children='Energy production'),

    # Afficher la production d’énergies
    html.Div(children=['''
    ''', html.Label('Year'),
        dcc.Dropdown(energy_prod_by_source['Date'].unique(), id="date_prod", value="2016")]),

    dcc.Graph(
        id='energy-prod-by-source',
    ),

    dcc.Graph(
        id='energy-production',
    ),

    html.H2(children='Temperature change'),
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
    Output('comparison_cons', 'figure'),
    Output('energy-consumption', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = lib.select_country(country_name, comparison)
    energy_data = lib.select_country(country_name, energy_cons_by_source)
    return (comparison_data.plot(x='Date', y=data), px.line(energy_data, x="Date", y="Value", color="Source", title='Energy consumption by source over time'))

@app.callback(
    Output('energy-cons-by-source', 'figure'),
    Input('country-name', 'value'),
    Input('date_cons', 'value'))
def update_energy(country_name, date):
    energy_data = lib.select_date(date, energy_cons_by_source)
    energy_data = lib.select_country(country_name, energy_data)
    print(energy_data)
    return px.pie(energy_data, values="Value", names="Source")


@app.callback(
    Output('comparison_prod', 'figure'),
    Output('energy-production', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = lib.select_country(country_name, comparison)
    energy_data = lib.select_country(country_name, energy_prod_by_source)
    return (comparison_data.plot(x='Date', y=data), px.line(energy_data, x="Date", y="Value", color="Source", title='Energy production by source over time'))

@app.callback(
    Output('energy-prod-by-source', 'figure'),
    Input('country-name', 'value'),
    Input('date_prod', 'value'))
def update_energy(country_name, date):
    energy_data = lib.select_date(date, energy_prod_by_source)
    energy_data = lib.select_country(country_name, energy_data)
    print(energy_data)
    return px.pie(energy_data, values="Value", names="Source")

if __name__ == '__main__':
    app.run_server(debug=True)