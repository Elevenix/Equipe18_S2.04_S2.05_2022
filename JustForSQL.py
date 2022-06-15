from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

pd.options.plotting.backend="plotly"

def columns_to_values(df, index, name):
    return df.melt(id_vars=df.iloc[:, 0:index], 
        var_name=name,
        value_name="Value")

# Création de chaque DataFrame
df_carbon = pd.read_csv('data/Carbon Footprint, 1990-2017 (in MtCO2).csv', decimal=',', sep=';')
df_carbon_world = pd.read_csv('data/Carbon Footprint, World, 1990-2017 (in MtCO2).csv', decimal=',', sep=';')
df_gaz = pd.read_csv('data/Gas Consumption, 1980-2016 (in Mtoe).csv', decimal=',', sep=';')
df_gaz_world = pd.read_csv('data/Gas Consumption, World, 1980-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction = pd.read_csv('data/Primary Energy Production, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_world = pd.read_csv('data/Primary Energy Production, World, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')

# Création de chaque DataFrame pour chaque pays producteur d'énergie primaire
df_energyproduction_china = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, China, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_denmark = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, Denmark, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_france = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, France, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_germany = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, Germany, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_india = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, India, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_ivorycoast = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, Ivory Coast, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')
df_energyproduction_unitedstates = pd.read_csv('data\primaryEnergyProduction\Primary Energy Production by source, United States of America, 1900-2016 (in Mtoe).csv', decimal=',', sep=';')

# Rajout du pays dans un DataFrame
df_energyproduction_china = df_energyproduction_china.rename(columns=({df_energyproduction_china.columns[0] : 'China'}))
df_energyproduction_denmark = df_energyproduction_denmark.rename(columns=({df_energyproduction_denmark.columns[0] : 'Denmark'}))
df_energyproduction_france = df_energyproduction_france.rename(columns=({df_energyproduction_france.columns[0] : 'France'}))
df_energyproduction_germany = df_energyproduction_germany.rename(columns=({df_energyproduction_germany.columns[0] : 'Germany'}))
df_energyproduction_india = df_energyproduction_india.rename(columns=({df_energyproduction_india.columns[0] : 'India'}))
df_energyproduction_ivorycoast = df_energyproduction_ivorycoast.rename(columns=({df_energyproduction_ivorycoast.columns[0] : 'Ivory Coast'}))
df_energyproduction_unitedstates = df_energyproduction_unitedstates.rename(columns=({df_energyproduction_unitedstates.columns[0] : 'United States of America'}))

list_df_energyproduction_country = [df_energyproduction_china,df_energyproduction_denmark,df_energyproduction_france,df_energyproduction_germany,df_energyproduction_india,df_energyproduction_ivorycoast,df_energyproduction_unitedstates]

# Dataframe World
footprint_carbon_world = px.line(df_carbon_world, x = df_carbon_world.columns[0], y = df_carbon_world.columns[1],title="Empreinte Carbone dans le Monde", 
        labels={df_carbon_world.columns[0]: "Année", "value": "Empreinte de carbone (en MtCO2)"})
footprint_gaz_world = px.line(df_gaz_world, x = df_gaz_world.columns[0], y = df_gaz_world.columns[1],title="Consommation de Gaz dans le Monde", 
        labels={df_gaz_world.columns[0]: "Année", "value": "Consommation de gaz (en Mtoe)"})
footprint_energyproduction_world = px.line(df_energyproduction_world, x = df_energyproduction_world.columns[0], y = df_energyproduction_world.columns[1],title="Production d'Energie Primaire dans le Monde", 
        labels={df_energyproduction_world.columns[0]: "Année", "value": "Production d'énergie primaire (en Mtoe)"})


# Création de l'application
app = Dash(__name__)

app.title = "Just a test for SQL !"

countrychoose = ""
app.layout = html.Div([
    # Empreinte carbone
    html.H3('Empreinte Carbone par Pays', style={'textAlign': 'center', 'padding': '10px 5px'}),
    dcc.Dropdown(id='country_drop_carbon',
                options=[{'label': country, 'value': country}
                        for country in df_carbon.columns[1:]]),
    dcc.Graph(id='country_carbon'),
    dcc.Graph(id='footprint_carbon_world', figure=footprint_carbon_world),

    html.Br(),

    # Comsommation de gaz
    html.H3('Consommation de Gaz par Pays', style={'textAlign': 'center', 'padding': '10px 5px'}),
    dcc.Dropdown(id='country_drop_gaz',
                options=[{'label': country, 'value': country}
                        for country in df_gaz.columns[1:]]),
    dcc.Graph(id='country_gaz'),
    dcc.Graph(id='footprint_gaz_world', figure=footprint_gaz_world),

    html.Br(),

    # Production d'énergie primaire par pays
    html.H3("Production d'Energie Primaire par Pays", style={'textAlign': 'center', 'padding': '10px 5px'}),
    dcc.Dropdown(id='country_drop_energyproduction',
                options=[{'label': country, 'value': country}
                        for country in df_energyproduction.columns[1:]]),
    dcc.Graph(id='country_energyproduction'),
    dcc.Graph(id='footprint_energyproduction_world', figure=footprint_energyproduction_world),

    html.Br(),

    # Production d'énergie primaire par pays choisi
    html.H3("Production d'Energie Primaire par Pays pa", style={'textAlign': 'center', 'padding': '10px 5px'}),
    dcc.Dropdown(id='country_drop_enprod_bycountry',
                options=[{'label': country, 'value': country}
                        for country in df_gaz.columns[1:]]),
    dcc.Graph(id='country_enprod_bycountry'),
])


# Empreinte carbone par pays
@app.callback(Output('country_carbon', 'figure'),
              Input('country_drop_carbon', 'value'))
def display_country_charts_carbon(country):
    cntry_stat = df_carbon
    fig = px.line(cntry_stat, x=df_carbon.columns[0], y=df_carbon.columns[df_carbon.columns == country].values, title=f'{country}', 
            labels={df_carbon.columns[0]: "Année", "value": "Empreinte de carbone (en MtCO2)"})
    return fig

# Consommation de gaz par pays
@app.callback(Output('country_gaz', 'figure'),
              Input('country_drop_gaz', 'value'))
def display_country_charts_gaz(country):
    fig = px.line(df_gaz, x=df_gaz.columns[0], y=df_gaz.columns[df_gaz.columns == country].values, title=f'{country}', 
            labels={df_gaz.columns[0]: "Année", "value": "Consommation de gaz (en Mtoe)"})
    return fig

# Production d'énergie primaire par pays
@app.callback(Output('country_energyproduction', 'figure'),
              Input('country_drop_energyproduction', 'value'))
def display_country_charts_gaz(country):
    fig = px.line(df_energyproduction, x=df_energyproduction.columns[0], y=df_energyproduction.columns[df_energyproduction.columns == country].values, title=f'{country}', 
            labels={df_energyproduction.columns[0]: "Année", "value": "Production d'énergie primaire (en Mtoe)"})
    return fig

# Production d'énergie primaire par pays choisi
@app.callback(Output('country_enprod_bycountry', 'figure'),
              Input('country_drop_enprod_bycountry', 'value'))
def display_dropdown(country):
    country_choosen_energy = pd.DataFrame(columns=[''])
    for country_energy in list_df_energyproduction_country:
        if(country_energy.columns[0] == country):
            country_choosen_energy = country_energy
    fig = px.line(country_choosen_energy, x=country_choosen_energy.columns[0], y=country_choosen_energy.columns[1:].values, title=f'{country}', 
            labels={country_choosen_energy.columns[0]: "Année", "value": "Production d'énergie primaire (en Mtoe)"})
    return fig

if __name__ == '__main__':
    app.run_server()