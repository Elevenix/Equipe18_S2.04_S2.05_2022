import lib
import pandas as pd

pd.options.plotting.backend = "plotly"

def get_sea_level():
    return pd.read_csv("CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual.csv")

def get_change_deg():
    lib.netcdf_to_csv("CMIP6 - Mean temperature (T) Change deg C - Medium Term (2041-2060) SSP5-8.5 (rel. to 1995-2014) - Annual (34 models).nc", "change_deg.csv")
    return pd.read_csv("change_deg.csv")

#
def get_ghg():
    ghg = pd.read_csv("Greenhouse Gas per capita, 1850-2015 (in tCO2eq).csv", sep=";", decimal=",")
    ghg = lib.columns_to_values(ghg, 1, 'Country','Emissions', end_index=6)
    lib.rename_column(ghg, "Date")
    lib.convert_date(ghg)
    return ghg

def get_gdp():
    #modif csv en xls
    gdp = pd.read_excel("API_NY.GDP.MKTP.KD_DS2_en_excel_v2_4150998.xls")
    gdp.to_csv("API_NY.GDP.MKTP.KD_DS2_en_csv_v2_4150850.csv", sep=";", decimal=",")
    print(gdp.columns)
    gdp = lib.columns_to_values(gdp, 4, 'Date', 'GDP')
    return gdp


def get_comparison():
    gdp = get_gdp()
    ghg = get_ghg()
    comparison = gdp.merge(ghg, left_on=["Date", "Country Name"], right_on=["Date", "Country"])
    return comparison

def get_energy_cons_by_source():
    energy = pd.read_csv("Primary Energy Consumption by source, World, 1980-2016 (in Mtoe).csv",sep=";")
    # TODO: INSERT 0s WHEN CELL IS EMPTY
    energy = lib.columns_to_values(energy, 1, 'Source', end_index=11)


    energy_countries=[
        ("Primary Energy Consumption by source, France, 1980-2016 (in Mtoe).csv", "France"),
        ("Primary Energy Consumption by source, China, 1980-2016 (in Mtoe).csv", "China")
    ]
    energy["Country Name"] = "World"
    for val in energy_countries:
        energy_country = pd.read_csv(val[0], sep=";")
        energy_country= lib.columns_to_values(energy_country, 1, 'Source', end_index=11)
        energy_country["Country Name"] = val[1]
        energy = pd.concat([energy, energy_country], axis=0)
    lib.rename_column(energy, "Date")
    lib.convert_date(energy)
    return energy

def get_energy_by_sector():
    energy_by_sector = pd.read_excel("IRENA_REmap_Global_Renewables_Outlook_2020_edition.xlsx")
    energy_by_sector = lib.columns_to_values(energy_by_sector, 5, "Year", "Consumption", end_index=8)
    energy_by_sector = energy_by_sector[
        (energy_by_sector["Sub-category"] == "Total")
        & (energy_by_sector["Region"] == "World")
        & (energy_by_sector["Case"] == "Planned Energy Scenario")
        & (energy_by_sector["type (Unit)"] == "Supply and demand (EJ)")
    ]

    energy_by_sector = lib.exclude(energy_by_sector, "Category", ["TFEC (excl. non-energy uses)", "TPES"])
    return energy_by_sector

