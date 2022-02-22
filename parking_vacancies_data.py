from sodapy import Socrata
import pandas as pd

# City of Chicago Data Portal
client1 = Socrata("data.cityofchicago.org", None)
# Cook County Data Portal
client2 = Socrata("datacatalog.cookcountyil.gov", None)

# Pins & locations for city-owned property
results1 = client1.get("aksk-kvfp", limit=12811, select="pin, location", where="property_status='Owned by City'")
# Pins for vacant land, including sideyards & unclassified land
results2 = client2.get("tnes-dgyi", limit=2032408, select="pin", where="class=0 OR class=100 OR class=190 OR class=000 OR \
class=241")
# Pins for low utility, low intensity properties & parking lots
results3 = client2.get("tnes-dgyi", limit=355368, select="pin", where="class=190 OR class=290 OR class=390 OR class=401 OR \
class=480 OR class=490 OR class=580 OR class=590 OR class=654 OR class=670 OR class=680 OR class=790 OR class=880 OR \
class=890 or class=990")

# Convert to pandas DataFrame
results_df1 = pd.DataFrame.from_records(results1)
results_df2 = pd.DataFrame.from_records(results2)
results_df3 = pd.DataFrame.from_records(results3)

# Join dataframes 1-2 and 1-3 on pin
results_df4 = pd.merge(results_df1,results_df2,on='pin')
results_df5 = pd.merge(results_df1,results_df3,on='pin')

