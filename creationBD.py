import pandas as pd
import sqlite3 as sql

conn = sql.connect('CaffeePierre.db')

cursor = conn.cursor()

# Creation des table

# Creation de la table Continent
cursor.execute("""
CREATE TABLE T_Continents (
    id_Continent INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Nom_Continent VARCHAR(100) NOT NULL,
    REF_Continent_pays INT NOT NULL,
    CONSTRAINT FK_Continent_pays FOREIGN KEY (REF_Continent_pays) 
        REFERENCES T_Pays (id_Pays)
)
""")

# Creation de la table Pays
cursor.execute("""
CREATE TABLE T_Pays (
    id_Pays INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    REF_Pays_Continent INT NOT NULL,
    REF_Pays_Secteurs INT NOT NULL,
    REF_Pays_Emission INT NOT NULL,
    Nom_Pays VARCHAR(100) NOT NULL,
    CONSTRAINT FK_Pays_Continent FOREIGN KEY (REF_Pays_Continent) 
        REFERENCES T_Continents(id_Continent),
    CONSTRAINT FK_Pays_Secteur FOREIGN KEY (REF_Pays_Secteurs)
        REFERENCES T_Secteurs(id_Secteur)
    CONSTRAINT FK_Pays_Emission FOREIGN KEY (REF_Pays_Emission)
        REFERENCES T_Emissions(id_Emission)
)
""")

# Creation de la relation Pays/Annee
cursor.execute("""
CREATE TABLE TJ_Secteurs_Energies (
    id_Secteur INT NOT NULL,
    id_Energie INT NOT NULL,
    Quantite REAL NOT NULL,
    Annee INT NOT NULL,
    CONSTRAINT FK_Pays FOREIGN KEY (id_Secteur)
        REFERENCES T_Secteurs(id_Secteur),
    CONSTRAINT FK_Energie FOREIGN KEY (id_Energie)
        REFERENCES T_Energies(id_Energie)
    )
""")

# Creation de la table Energie
cursor.execute("""
CREATE TABLE T_Energies (
    id_Energie INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Nom_Energie VARCHAR(100) NOT NULL
)
""")

# Creation de la relation Energie/Annee
cursor.execute("""
CREATE TABLE TJ_Energies_Pays (
    id_Energie INT NOT NULL,
    id_Pays INT NOT NULL,
    Qtt_Energie_Cons REAL NOT NULL,
    Annee INT NOT NULL,
    CONSTRAINT FK_Energie FOREIGN KEY (id_Energie)
        REFERENCES T_Energies(id_Energie),
    CONSTRAINT FK_Pays FOREIGN KEY (id_Pays)
        REFERENCES T_Pays(id_Pays)
)
""")

# Creation de la table activite
cursor.execute("""
CREATE TABLE T_Secteurs (
    id_Secteur INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    REF_Secteur_Pays INT,
    Nom_Secteur VARCHAR(100) NOT NULL,
    CONSTRAINT FK_Secteur_Pays FOREIGN KEY (REF_Secteur_Pays)
        REFERENCES T_Pays(id_Pays)
)
""")

# Creation de la table Emission
cursor.execute("""
    CREATE TABLE T_Emissions (
        id_Emission INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        REF_Emission_Pays INT NOT NULL,
        PIB REAL,
        Emission_GES REAL,
        Annee INT NOT NULL,
        CONSTRAINT FK_Emission_Pays FOREIGN KEY (REF_Emission_Pays)
            REFERENCES T_Pays(id_Pays)
)
""")


conn.close()