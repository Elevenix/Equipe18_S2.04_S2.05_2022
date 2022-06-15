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

# Creation de la table Annee
cursor.execute("""
CREATE TABLE T_Annees (
    id_Annee INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Annee INT NOT NULL
)
""")

# Creation de la table Pays
cursor.execute("""
CREATE TABLE T_Pays (
    id_Pays INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    REF_Pays_Continent INT NOT NULL,
    REF_Pays_Activitee INT NOT NULL,
    Nom_Pays VARCHAR(100) NOT NULL,
    CONSTRAINT FK_Pays_Continent FOREIGN KEY (REF_Pays_Continent) 
        REFERENCES T_Continents(id_Continent),
    CONSTRAINT FK_Pays_Activitee FOREIGN KEY (REF_Pays_Activitee)
        REFERENCES T_Activitees(id_Activitee)
)
""")

# Creation de la relation Pays/Annee
cursor.execute("""
CREATE TABLE TJ_Pays_Annee (
    id_Pays INT NOT NULL,
    id_Annee INT NOT NULL,
    Nb_Habitants INT NOT NULL,
    Temperature INT NOT NULL,
    Precipitation REAL NOT NULL,
    Niv_Mer REAL NOT NULL,
    CONSTRAINT FK_Pays FOREIGN KEY (id_Pays)
        REFERENCES T_Pays(id_Pays),
    CONSTRAINT FK_Annee FOREIGN KEY (id_Annee)
        REFERENCES T_Annees(id_Annee)
)
""")

# Creation de la table Energie
cursor.execute("""
CREATE TABLE T_Energies (
    id_Energie INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    REF_Energie_Pays INT,
    REF_Energie_Activitee INT,
    Nom_Energie VARCHAR(100) NOT NULL,
    Renouvelabilité BOOLEAN,
    CONSTRAINT FK_Energie_Pays FOREIGN KEY (REF_Energie_Pays)
        REFERENCES T_Pays(id_Pays)
    CONSTRAINT FK_Energie_Activitee FOREIGN KEY (REF_Energie_Activitee)
        REFERENCES T_Activitees(id_Activitee)
)
""")

# Creation de la relation Energie/Annee
cursor.execute("""
CREATE TABLE TJ_Eng_Annee (
    id_Energie INT NOT NULL,
    id_Annee INT NOT NULL,
    Empreinte_Carb REAL NOT NULL,
    Qtt_Energie_Prod REAL,
    Qtt_Energie_Cons REAL NOT NULL,
    CONSTRAINT FK_Energie FOREIGN KEY (id_Energie)
        REFERENCES T_Energies(id_Energie),
    CONSTRAINT FK_Annee FOREIGN KEY (id_Annee)
        REFERENCES T_Annees(id_Annee)
)
""")

# Creation de la table activite
cursor.execute("""
CREATE TABLE T_Activitees (
    id_Activitee INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    REF_Activitee_Pays INT,
    REF_Activitee_Energie INT,
    Nom_Activitee VARCHAR(100) NOT NULL,
    CONSTRAINT FK_Activitee_Pays FOREIGN KEY (REF_Activitee_Pays)
        REFERENCES T_Pays(id_Pays)
    CONSTRAINT FK_Activitee_Energie FOREIGN KEY (REF_Activitee_Energie)
        REFERENCES T_Energies(id_Energie)
)
""")

conn.close()