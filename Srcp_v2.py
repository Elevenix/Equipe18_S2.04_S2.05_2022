import pandas as pd
import sqlite3 as sql
import data

conn = sql.connect('CaffeePierre.db')

cursor = conn.cursor()

"""
constantes pays
"""
df_pays = pd.read_csv('Primary Energy Production, 1900-2016 (in Mtoe).csv', sep=';')
pays = pd.Series(df_pays.columns[1:])

"""
supprression des tables
"""
def Supprimer_Tables():
    cursor.execute("DROP TABLE IF EXISTS T_Continents")
    cursor.execute("DROP TABLE IF EXISTS T_Pays")
    cursor.execute("DROP TABLE IF EXISTS T_Energies")
    cursor.execute("DROP TABLE IF EXISTS T_Secteurs")
    cursor.execute("DROP TABLE IF EXISTS TJ_Secteurs_Energies")
    cursor.execute("DROP TABLE IF EXISTS TJ_Energies_Pays")
    cursor.execute("DROP TABLE IF EXISTS T_Emissions")

#vide les tables
Supprimer_Tables()


"""
remplit la table Continents
"""
def Continents(conn):
    continents = pd.Series(['Europe', 'Oceania', 'Afrique', 'Amérique', 'Asie', 'Antarctique'])
    continents.name = 'Nom_Continent'
    continents.to_sql('T_Continents', conn, if_exists='append', index=True, index_label='id_Continent')

"""
remplit la table Pays
"""
def Pays(conn):
    pays.name = 'Nom_Pays'
    pays.to_sql('T_Pays', conn, if_exists='append', index=True, index_label='id_Pays')

"""
remplit la table Energie
"""
def Energie(conn):
    df_energies = pd.read_csv('Primary Energy Consumption by source, United States of America, 1980-2016 (in Mtoe).csv', sep=';')
    df_energies['Renewable'] = None
    ren = df_energies.columns[1:]
    print(ren)
    energies = pd.Series(ren)
    
    energies.name = 'Nom_Energie'
    energies.to_sql('T_Energies', conn, if_exists='append', index=True, index_label='id_Energie')
    

"""
remplit la table Secteur
"""
def Secteur(conn):
    df_Secteur = pd.DataFrame(pd.read_excel('IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx'))
    df_Secteur = df_Secteur[df_Secteur['Category']!='TPES']
    df_Secteur = df_Secteur[df_Secteur['Category']!='TFEC (excl. non-energy uses)']
    df_Secteur = df_Secteur[df_Secteur['Sub-category']=='Total']
    df_Secteur = df_Secteur[df_Secteur['Case']=='Planned Energy Scenario']
    df_Secteur = df_Secteur[df_Secteur['Region']=='World']
    df_Secteur = df_Secteur[df_Secteur['type (Unit)']=='Supply and demand (EJ)']
    Secteur = pd.Series(df_Secteur.get('Category'))
    Secteur.name = 'Nom_Secteur'
    Secteur.to_sql('T_Secteurs', conn, if_exists='append', index=True, index_label='id_Secteur')

"""
remplit la collone EmissionGES de la table T_Emissions
"""
def EmissionGES(conn):
    df_EmpreinteCarbone = pd.read_csv('Gas Consumption, 1980-2016 (in Mtoe).csv', sep=';')
    for i in range(1, len(df_EmpreinteCarbone.columns)-1):
        conn.execute("""
            INSERT INTO T_Emissions (id_Emission, Emission_GES, REF_Emission_Pays, Annee)
                VALUES (?, ?, ?, ?)
            """, (i, i, i, df_EmpreinteCarbone.get(df_EmpreinteCarbone.columns[0])[len(df_EmpreinteCarbone.columns)][0:4]))


    a=df_EmpreinteCarbone.get(df_EmpreinteCarbone.columns)
    print(a[1])
    print(df_EmpreinteCarbone.get(df_EmpreinteCarbone.columns[0])[len(df_EmpreinteCarbone.columns)][0:4])

Continents(conn)
Pays(conn)
Secteur(conn)
Energie(conn)

def insert_emissions(conn):
    base = data.get_comparison()
    print(base)
    pays = pd.read_sql('SELECT * FROM T_Pays', conn)
    base = base.merge(pays, left_on='Country Name', right_on="Nom_Pays", how="inner")
    base.rename(columns={"GDP": "PIB", "Date": "Annee", "Emissions": "Emission_GES"}, inplace=True)
    base = base[["id_Pays", "PIB", "Emission_GES", "Annee"]]
    print(base)
    base.to_sql("T_Emissions", conn, if_exists='append', index=True, index_label='id_Emission')

insert_emissions(conn)


def insert_Consomme(conn):
    base = data.get_energy_by_sector()
    cursor.execute("SELECT id_Energie FROM T_Energies WHERE Nom_Energie LIKE '%Renewable%'")
    index = cursor.fetchone()
    base["id_Energie"] = index[0]
    secteurs = pd.read_sql('SELECT * FROM T_Secteurs', conn)
    base = base.merge(secteurs, left_on='Category', right_on="Nom_Secteur", how="inner")
    base.rename(columns={"Consumption": "Quantite", "Year": "Annee"}, inplace=True)
    base = base[["id_Energie", "id_Secteur", "Quantite", "Annee"]]
    base.to_sql("TJ_Secteurs_Energies", conn, if_exists='append', index=False)

insert_Consomme(conn)

def insert_utilise(conn):
    base = data.get_energy_cons_by_source()
    energie = pd.read_sql('SELECT * FROM T_Energies', conn)
    base = base.merge(energie, left_on='Source', right_on="Nom_Energie", how="inner")
    pays = pd.read_sql('SELECT * FROM T_Pays', conn)
    base = base.merge(pays, left_on='Country Name', right_on="Nom_Pays", how="inner")
    base.rename(columns={"Date": "Annee", "Value": "Qtt_Energie_Cons"}, inplace=True)
    base = base[['id_Energie', 'id_Pays', 'Qtt_Energie_Cons', 'Annee']]
    base.to_sql("TJ_Energies_Pays", conn, if_exists='append', index=False)
    
insert_utilise(conn)

conn.close()