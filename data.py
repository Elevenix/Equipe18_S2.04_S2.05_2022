import pandas as pd
import lib

pd.options.plotting.backend = "plotly"

# On replace les read_csv par des read_sql

def get_sea_level():
    return pd.read_csv("data/CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual.csv")

def get_prim_energy_prod():
    return pd.read_csv("data/Primary Energy Production, 1900-2016 (in Mtoe).csv", decimal=",", sep=";")

def get_prim_energy_prod_world():
    return pd.read_csv("data/Primary Energy Production, World, 1900-2016 (in Mtoe).csv", decimal=",", sep=";")

def get_change_deg():
    lib.netcdf_to_csv("data/CMIP6 - Mean temperature (T) Change deg C - Medium Term (2041-2060) SSP5-8.5 (rel. to 1995-2014) - Annual (34 models).nc", "change_deg.csv")
    change_deg = pd.read_csv("change_deg.csv")
    return change_deg[change_deg["tas_anom"] != None]

def get_ghg():
    ghg = pd.read_csv("data/Greenhouse Gas per capita, 1850-2015 (in tCO2eq).csv", sep=";", decimal=",")
    ghg = lib.columns_to_values(ghg, 1, "Country","Emissions", end_index=8)
    lib.rename_column(ghg, "Date")
    lib.convert_date(ghg)
    return ghg

def get_gdp():
    gdp = pd.read_csv("data/API_NY.GDP.MKTP.KD_DS2_en_csv_v2_4150850.csv", sep=";")
    gdp = lib.columns_to_values(gdp, 4, "Date", "GDP")
    return gdp


def get_comparison():
    gdp = get_gdp()
    ghg = get_ghg()
    comparison = gdp.merge(ghg, left_on=["Date", "Country Name"], right_on=["Date", "Country"])
    return comparison


def get_energy_cons_by_source():
    energy = pd.read_csv("data/Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv", sep=";", decimal=",")
    # TODO: INSERT 0s WHEN CELL IS EMPTY
    energy = lib.columns_to_values(energy, 1, "Source", end_index=11)

    energy_countries=[
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, China, 1980-2016 (in Mtoe).csv", "China"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, Denmark, 1980-2016 (in Mtoe).csv", "Denmark"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, France, 1980-2016 (in Mtoe).csv", "France"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, Germany, 1980-2016 (in Mtoe).csv", "Germany"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, India, 1980-2016 (in Mtoe).csv", "India"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, Ivory Coast, 1980-2016 (in Mtoe).csv", "Ivory Coast"),
        ("data/primaryEnergyConsumption/Primary Energy Consumption by source, United States of America, 1980-2016 (in Mtoe).csv", "United States of America")
    ]

    energy["Country Name"] = "World"
    for val in energy_countries:
        energy_country = pd.read_csv(val[0], sep=";", decimal=",")
        energy_country= lib.columns_to_values(energy_country, 1, "Source", end_index=11)
        energy_country["Country Name"] = val[1]
        energy = pd.concat([energy, energy_country], axis=0)
    lib.rename_column(energy, "Date")
    lib.convert_date(energy)
    return energy

def get_energy_cons_by_sector():
    energy_by_sector = pd.read_excel("data/IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx")
    energy_by_sector = lib.columns_to_values(energy_by_sector, 5, "Year", "Consumption", end_index=8)
    energy_by_sector = energy_by_sector[
        (energy_by_sector["Sub-category"] == "Total")
        & (energy_by_sector["Region"] == "World")
        & (energy_by_sector["Case"] == "Planned Energy Scenario")
        & (energy_by_sector["type (Unit)"] == "Supply and demand (EJ)")
    ]

    energy_by_sector = lib.exclude(energy_by_sector, "Category", ["TFEC (excl. non-energy uses)", "TPES"])
    return energy_by_sector

def get_energy_prod_by_source():
    energy = pd.read_csv("data/Primary Energy Production, World, 1900-2016 (in Mtoe).csv", sep=";", decimal=",")
    # TODO: INSERT 0s WHEN CELL IS EMPTY
    energy = lib.columns_to_values(energy, 1, "Source", end_index=11)

    energy_countries=[
        ("data/primaryEnergyProduction/Primary Energy Production by source, China, 1900-2016 (in Mtoe).csv", "China"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, Denmark, 1900-2016 (in Mtoe).csv", "Denmark"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, France, 1900-2016 (in Mtoe).csv", "France"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, Germany, 1900-2016 (in Mtoe).csv", "Germany"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, India, 1900-2016 (in Mtoe).csv", "India"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, Ivory Coast, 1900-2016 (in Mtoe).csv", "Ivory Coast"),
        ("data/primaryEnergyProduction/Primary Energy Production by source, United States of America, 1900-2016 (in Mtoe).csv", "United States of America")
    ]

    energy["Country Name"] = "World"
    for val in energy_countries:
        energy_country = pd.read_csv(val[0], sep=";", decimal=",")
        energy_country= lib.columns_to_values(energy_country, 1, "Source", end_index=11)
        energy_country["Country Name"] = val[1]
        energy = pd.concat([energy, energy_country], axis=0)
    lib.rename_column(energy, "Date")
    lib.convert_date(energy)
    return energy
