import xarray as xr
import pandas as pd
import plotly.express as px

# Convertir netcdf en csv
def netcdf_to_csv(input, output):
    xr.open_dataset(input).to_dataframe().to_csv(output)

# Créér une table dans la BD à partir d'un fichier CSV
def table_from_csv(conn, file, name):
    df = pd.read_csv(file)
    df.to_sql(name, conn, if_exists="replace")

def columns_to_values(df, index, name, value_name="Value", end_index=None):
    return df.melt(id_vars=df.iloc[:, 0:index], 
        var_name=name,
        value_vars=df.iloc[:, index:end_index],
        value_name=value_name)

# Sélectionner un pays
def select_country(name, df):
    return df[df['Country Name']==name]

# Exclure des lignes contenant des valeurs
def exclude(df, column, values=[]):
    for value in values:
        df = df[df[column] != value]
    return df

# Renommer la première colonne sans nom
def rename_column(df, name):
    df.rename( columns={'Unnamed: 0':name}, inplace=True )

# Sélectionner avec la date
def select_date(date, df):
    return df[df["Date"]==date]

# Sélectionner avec la source
def select_source(source, df):
    return df[df["Source"]==source]

# Prendre seulement l'année dans la date
def convert_date(df):
    df["Date"] = df['Date'].astype(str).str[:4]
    return df

# Créér une carte
def map(df, z):
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", color=z, zoom=0.4, opacity=0.2,
                  color_continuous_scale=px.colors.cyclical.IceFire,  mapbox_style="stamen-terrain", width=1000, height=700)
    fig.update_traces(marker={'size': 10})
    return fig