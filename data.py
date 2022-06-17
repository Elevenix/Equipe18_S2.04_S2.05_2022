import lib
import pandas as pd

pd.options.plotting.backend = "plotly"

def get_sea_level():
    return pd.read_csv("data/CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual.csv")

def get_change_deg():
    lib.netcdf_to_csv("data/CMIP6 - Mean temperature (T) Change deg C - Medium Term (2041-2060) SSP5-8.5 (rel. to 1995-2014) - Annual (34 models).nc", "data/change_deg.csv")
    return pd.read_csv("data/change_deg.csv")

def get_ghg():
    ghg = pd.read_csv("data/Greenhouse Gas per capita, 1850-2015 (in tCO2eq).csv", sep=";", decimal=",")
    ghg = lib.columns_to_values(ghg, 1, 'Country','Emissions', end_index=8)
    lib.rename_column(ghg, "Date")
    lib.convert_date(ghg)
    return ghg

def get_gdp():
    #modif csv en xls
    gdp = pd.read_excel("data/API_NY.GDP.MKTP.KD_DS2_en_excel_v2_4150998.xls")
    gdp.to_csv("data/API_NY.GDP.MKTP.KD_DS2_en_csv_v2_4150850.csv", sep=";", decimal=",")
    gdp = lib.columns_to_values(gdp, 4, 'Date', 'GDP')
    gdp['Country Name'].replace({"United States": "United States of America", "Cote d'Ivoire": "Ivory Coast"}, inplace=True)
    return gdp

def get_footprint():
    footprint = pd.read_csv("data/Carbon Footprint, 1990-2017 (in MtCO2).csv", sep=";", decimal=",")
    footprint = lib.columns_to_values(footprint, 1, 'Country', 'FootPrint', end_index=8)
    lib.rename_column(footprint, "Date")
    lib.convert_date(footprint)
    for i in range(len(footprint)):
        footprint["Country"][i] = footprint["Country"][i][0:-19]
    return footprint
     

def get_comparison():
    gdp = get_gdp()
    ghg = get_ghg()
    print(ghg['Country'])
    comparison = gdp.merge(ghg, left_on=["Date", "Country Name"], right_on=["Date", "Country"])
    return comparison

def get_energy_cons_by_source():
    energy = pd.read_csv("data/Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv",sep=";", decimal=",")
    # TODO: INSERT 0s WHEN CELL IS EMPTY
    energy = lib.columns_to_values(energy, 1, 'Source', end_index=11)


    energy_countries=[
        ("data/Primary Energy Consumption by source, France, 1980-2016 (in Mtoe).csv", "France"),
        ("data/Primary Energy Consumption by source, China, 1980-2016 (in Mtoe).csv", "China"),
        ("data/Primary Energy Consumption by source, India, 1980-2016 (in Mtoe).csv", "India"),
        ("data/Primary Energy Consumption by source, Denmark, 1980-2016 (in Mtoe).csv", "Denmark"),
        ("data/Primary Energy Consumption by source, Germany, 1980-2016 (in Mtoe).csv", "Germany"),
        ("data/Primary Energy Consumption by source, Ivory Coast, 1980-2016 (in Mtoe).csv", "Ivory Coast"),
        ("data/Primary Energy Consumption by source, United States of America, 1980-2016 (in Mtoe).csv", "United States of America"),
    ]
    energy["Country Name"] = "World"
    for val in energy_countries:
        energy_country = pd.read_csv(val[0], sep=";", decimal=",")
        energy_country= lib.columns_to_values(energy_country, 1, 'Source', end_index=11)
        energy_country["Country Name"] = val[1]
        energy = pd.concat([energy, energy_country], axis=0)
    lib.rename_column(energy, "Date")
    lib.convert_date(energy)
    return energy


def get_energy_prod_by_source():
    energy = pd.read_csv("data/Primary Energy Production by source, World, 1900-2016 (in Mtoe).csv",sep=";", decimal=",")
    # TODO: INSERT 0s WHEN CELL IS EMPTY
    energy = lib.columns_to_values(energy, 1, 'Source', end_index=11)


    energy_countries=[
        ("data/Primary Energy Production by source, France, 1900-2016 (in Mtoe).csv", "France"),
        ("data/Primary Energy Production by source, China, 1900-2016 (in Mtoe).csv", "China"),
        ("data/Primary Energy Production by source, India, 1900-2016 (in Mtoe).csv", "India"),
        ("data/Primary Energy Production by source, Denmark, 1900-2016 (in Mtoe).csv", "Denmark"),
        ("data/Primary Energy Production by source, Germany, 1900-2016 (in Mtoe).csv", "Germany"),
        ("data/Primary Energy Production by source, Ivory Coast, 1900-2016 (in Mtoe).csv", "Ivory Coast"),
        ("data/Primary Energy Production by source, United States of America, 1900-2016 (in Mtoe).csv", "United States of America"),
    ]
    energy["Country Name"] = "World"
    for val in energy_countries:
        energy_country = pd.read_csv(val[0], sep=";", decimal=",")
        energy_country= lib.columns_to_values(energy_country, 1, 'Source', end_index=11)
        energy_country["Country Name"] = val[1]
        energy = pd.concat([energy, energy_country], axis=0)
    lib.rename_column(energy, "Date")
    lib.convert_date(energy)
    return energy

def get_energy_by_sector():
    energy_by_sector = pd.read_excel("data/IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx")
    energy_by_sector = lib.columns_to_values(energy_by_sector, 5, "Annee", "Consumption", end_index=8)
    energy_by_sector = energy_by_sector[
        (energy_by_sector["Sub-category"] == "Total")
        & (energy_by_sector["Region"] == "World")
        & (energy_by_sector["Case"] == "Planned Energy Scenario")
        & (energy_by_sector["type (Unit)"] == "Supply and demand (EJ)")
    ]

    energy_by_sector = lib.exclude(energy_by_sector, "Category", ["TFEC (excl. non-energy uses)", "TPES"])
    return energy_by_sector

