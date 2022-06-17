import pandas
import sqlite3 as sql
def get_countries(conn):
    return pandas.read_sql("SELECT * FROM T_Pays", conn)

def get_energies(conn):
    return pandas.read_sql("SELECT * FROM T_Energies", conn)

def get_sectors(conn):
    return pandas.read_sql("SELECT * FROM T_Secteurs", conn)

def merge_countries(conn, df):
    countries = get_countries(conn)
    return df.merge(countries, on="id_Pays")

def merge_energies(conn, df):
    energies = get_energies(conn)
    return df.merge(energies, on="id_Energie")

def merge_sectors(conn, df):
    sectors = get_sectors(conn)
    return df.merge(sectors, on="id_Secteur")

def get_emissions(conn):
    emissions = pandas.read_sql("SELECT * FROM T_Emissions", conn)
    emissions = merge_countries(conn, emissions)
    return emissions

def get_utilise(conn):
    utilise = pandas.read_sql("SELECT * FROM TJ_Energies_Pays", conn)
    utilise = merge_countries(conn, utilise)
    utilise = merge_energies(conn, utilise)
    return utilise

def get_consumption(conn):
    consumption = pandas.read_sql("SELECT * FROM TJ_Secteurs_Energies", conn)
    consumption = merge_energies(conn, consumption)
    consumption = merge_sectors(conn, consumption)
    return consumption

def connect():
    return sql.connect('CaffeePierre.db')
