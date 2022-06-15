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
    pays = pd.Series(['France','Germany','Ivory Coast','China','India','United States of America','Denmark', 'World'])
    pays.name = 'Nom_Pays'
    pays.to_sql('T_Pays', conn, if_exists='replace', index=True, index_label='id_Pays')

"""
remplit la table Energie
"""
def Energie(conn):
    energies = pd.Series(["Oil","Coal","Gas","Hydroelectricity","Nuclear","Biomass and Waste","Wind","Fuel Ethanol","Solar, Tide, Wave, Fuel Cell","Geothermal","Biodiesel"])
    energies.name = 'Nom_Energie'
    energies.to_sql('T_Energie', conn, if_exists='replace', index=True, index_label='id_Energie')
    
# 
"""
remplit la table TJ_Energie_Annee
"""
def Energie_Annee(conn):
    energies = pd.read_csv('data/Primary Energy Production, 1900-2016 (in Mtoe).csv', sep=';')
    conn.execute("""
        INSERT INTO TJ_Energie_Annee (id_Energie, id_Annee, Production) VALUES (?,?,?)""", 
        (1,1,energies.loc[0,'Oil']))



Annee(conn)
Continents(conn)
Pays(conn)
Energie(conn)
Energie_Annee(conn)