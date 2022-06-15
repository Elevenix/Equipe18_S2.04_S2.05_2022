import pandas as pd
import sqlite3 as sql

conn = sql.connect('CaffeePierre.db')

cursor = conn.cursor()

"""
supprression des tables
"""
def Supprimer_Tables(conn):
    cursor.execute("DROP TABLE IF EXISTS T_Annees")
    cursor.execute("DROP TABLE IF EXISTS T_Continents")
    cursor.execute("DROP TABLE IF EXISTS T_Pays")
    cursor.execute("DROP TABLE IF EXISTS T_Energie")

"""
remplit la table Annee
"""
def Annee(conn):
    annee = pd.Series([ i for i in range(1990, 2018) ])
    annee.name = 'Annee'
    annee.to_sql('T_Annees', conn, if_exists='replace', index=True, index_label='id_Annee')
        
"""
remplit la table Continents
"""
def Continents(conn):
    continents = pd.Series(['Europe', 'Oceania', 'Afrique', 'Amérique', 'Asie', 'Antarctique'])
    continents.name = 'Nom_Continent'
    continents.to_sql('T_Continents', conn, if_exists='replace', index=True, index_label='id_Continent')

"""
remplit la table Pays
"""
def Pays(conn):
    df_pays = pd.read_csv('data/Primary Energy Production, 1900-2016 (in Mtoe).csv', sep=';')
    pays = pd.Series(df_pays.columns[1:])
    pays.name = 'Nom_Pays'
    pays.to_sql('T_Pays', conn, if_exists='replace', index=True, index_label='id_Pays')

"""
remplit la table Energie
"""
def Energie(conn):
    df_energies = pd.read_csv('data/Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv', sep=';')
    energies = pd.Series(df_energies.columns[1:])
    energies.name = 'Nom_Energie'
    energies.to_sql('T_Energies', conn, if_exists='replace', index=True, index_label='id_Energie')
    

"""
remplit la table Activite
"""
def Activite(conn):
    df_activite = pd.DataFrame(pd.read_excel('data/IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx'))
    df_activite = df_activite[df_activite['Category']!='TPES']
    df_activite = df_activite[df_activite['Category']!='TFEC (excl. non-energy uses)']
    df_activite = df_activite[df_activite['Sub-category']=='Total']
    df_activite = df_activite[df_activite['Case']=='Planned Energy Scenario']
    df_activite = df_activite[df_activite['Region']=='World']
    df_activite = df_activite[df_activite['type (Unit)']=='Supply and demand (EJ)']
    activite = pd.Series(df_activite.get('Category'))
    activite.name = 'Nom_Activitee'
    activite.to_sql('T_Activitees', conn, if_exists='replace', index=True, index_label='id_Activitee')

"""
remplit la table TJ_Energie_Annee
"""
def Energie_Annee(conn):
    df_energiesCons = pd.read_csv('data/Primary Energy Production, 1900-2016 (in Mtoe).csv', sep=';')
    df_EmpreinteCarbone = pd.read_csv('data/Carbon Footprint, 1990-2017 (in MtCO2).csv', sep=';')
    #df_sousRequete1 = "SELECT id_Energie FROM T_Energie WHERE Nom_Energie LIKE ?", [ x for x in df_EmpreinteCarbone.columns ].remove('Unnamed: 0')
    df = ()
    conn.execute("""
        INSERT INTO TJ_Energie_Annee (id_Energie, id_Annee, Emission_GES, Qtt_Energie_Prod) 
            VALUES (?, ? ,?, ?)""", 
            [ x for x in df_EmpreinteCarbone.columns ][1:], [ x for x in df_energiesCons.columns ][1:], df_EmpreinteCarbone.get(df_EmpreinteCarbone.columns), df_energiesCons.get(df_energiesCons.columns))



Annee(conn)
Continents(conn)
Pays(conn)
Activite(conn)
Energie(conn)