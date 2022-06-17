import pandas
import plotly.express as px
import lib
import data
import db
from dash import Dash, dcc, html, Input, Output
pandas.options.plotting.backend = "plotly"
conn = db.connect()
### Chargement des données
#energy_cons_by_source = data.get_energy_cons_by_source()
energy_cons_by_source = db.get_utilise(conn)
sea_level = data.get_sea_level()
change_deg = data.get_change_deg()
#comparison = data.get_comparison()
comparison = db.get_emissions(conn)
energy_by_sector = db.get_consumption(conn)
#energy_by_sector = db.get()
### Affichage

app = Dash(__name__, suppress_callback_exceptions=True)

energy_by_sector_fig = px.bar(energy_by_sector, x="Annee", y="Quantite", color="Nom_Secteur")
#energy_by_sector_fig = px.bar()
print(comparison['id_Pays'].unique())

degree_map = lib.map(change_deg, 'tas_anom')
sea_level_map  = lib.map(sea_level, 'total')
app.layout = html.Div(children=[
    html.H1(children='CoffeeRock'),
    html.H2(children='Countries'),

    html.Div(children=['''
    ''', html.Label('Country'),
        dcc.Dropdown(comparison['Nom_Pays'].unique(), id="country-name", value='France')]),

    dcc.Tabs(id='data', value='PIB', children=[
        dcc.Tab(label='GDP', value='PIB'),
        dcc.Tab(label='Emissions', value='Emission_GES'),
    ]),
    
    # Fonctionnalité: Afficher les GES en fonction du pays
    # Fonctionnalité: Causes des émissions GES
    dcc.Graph(
        id='comparison'
    ),

    html.H3(children='Energy consumption'),

    # Afficher la production d’énergies
    html.Div(children=['''
    ''', html.Label('Annee'),
        dcc.Dropdown(energy_cons_by_source['Annee'].unique(), id="date", value="2016")]),

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
    Output('comparison', 'figure'),
    Output('energy-consumption', 'figure'),
    Input('country-name', 'value'),
    Input('data', 'value'))
def update_graph(country_name, data):
    comparison_data = lib.select_country(country_name, comparison)
    energy_data = lib.select_country(country_name, energy_cons_by_source)
    return (comparison_data.plot(x='Annee', y=data), px.line(energy_data, x="Annee", y="Qtt_Energie_Cons", color="Nom_Energie", title='Energy consumption by source over time'))

@app.callback(
    Output('energy-by-source', 'figure'),
    Input('country-name', 'value'),
    Input('date', 'value'))
def update_energy(country_name, date):
    energy_data = lib.select_date(date, energy_cons_by_source)
    energy_data = lib.select_country(country_name, energy_data)
    print("energy-by-source")
    return px.pie(energy_data, values="Qtt_Energie_Cons", names="Nom_Energie")

if __name__ == '__main__':
    app.run_server(debug=True)
