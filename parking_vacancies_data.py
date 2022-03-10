from sodapy import Socrata
import pandas as pd

# City of Chicago Data Portal
chicago = Socrata("data.cityofchicago.org", None)
# Cook County Data Portal
cook_county = Socrata("datacatalog.cookcountyil.gov", None)

# Pins for city-owned property
city_owned = chicago.get("aksk-kvfp", limit=12811,
                         select="pin", where="property_status='Owned by City'")
# Pins for vacant land, including sideyards & unclassified land
vacant = cook_county.get("tnes-dgyi", limit=2032408, select="pin", where="class=0 OR class=100 OR class=190 OR \
class=000 OR class=241")
# Pins for low utility, low intensity properties & parking lots
low_utility = cook_county.get("tnes-dgyi", limit=355368, select="pin", where="class=190 OR class=290 OR class=390 OR \
class=401 OR class=480 OR class=490 OR class=580 OR class=590 OR class=654 OR class=670 OR class=680 OR class=790 OR \
class=880 OR class=890 or class=990")
# Pins and shapefiles for all properties 1430137
shapefiles = cook_county.get(
    "2yvh-uwrw", limit=613182, select="pin10, the_geom", where="municipality='Chicago'")
for idx, _ in enumerate(shapefiles):
    if "pin10" in shapefiles[idx]:
        shapefiles[idx]["pin"] = '-'.join([shapefiles[idx]["pin10"][:2], shapefiles[idx]["pin10"][2:4],
                                          shapefiles[idx]["pin10"][4:7], shapefiles[idx]["pin10"][7:10], shapefiles[idx]["pin10"][10:]])
        shapefiles[idx]["pin"] += "0000"

# Convert lists to pandas DataFrames
city_owned_df = pd.DataFrame.from_records(city_owned)
vacant_df = pd.DataFrame.from_records(vacant)
low_utility_df = pd.DataFrame.from_records(low_utility)
shapefiles_df = pd.DataFrame.from_records(shapefiles)

# Inner join vacant & low-utility dataframes with city-owned dataframe on pin
city_owned_vacant_df = pd.merge(city_owned_df, vacant_df, on='pin')
city_owned_low_utility_df = pd.merge(city_owned_df, low_utility_df, on='pin')
# Inner join city-owned vacant & low-utility dataframes with shapefiles dataframe on pin
city_owned_vacant_shapefiles_df = pd.merge(
    city_owned_vacant_df, shapefiles_df, on='pin')
city_owned_low_utility_shapefiles_df = pd.merge(
    city_owned_low_utility_df, shapefiles_df, on='pin')
# Outer join city-owned vacant & low-utility shapefile dataframes with on pin
city_owned_vacant_or_low_utility_shapefiles_df = pd.merge(
    city_owned_vacant_shapefiles_df, city_owned_low_utility_shapefiles_df, on='pin', how='outer')

city_owned_vacant_or_low_utility_shapefiles_df.to_csv("vacant_lots.csv")
