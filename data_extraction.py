from sodapy import Socrata
import pandas as pd
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon
from pyproj import Geod
from shapely import wkt

"""
The following code pulls data from City of Chicago and Cook County Data portals, then 
cleans and transforms the data to be used for analysis, then generates the community_areas.csv, 
parks.csv, and vacants.csv files.
    
Inputs:
    None
 
Outputs:
    community_areas: csv file containing the following columns 
        Neighborhood: (str) community area
        vacant_count: (int) total count of city-owned vacancies by community area
        vacant_acres: (float) total amount of city-owned vacancy acreage by community area
        park_count: (int) total count of parks by community area
        park_acres: (float) total amount of park acreage by community area
        census_tracts: (list) census tract polygons by community area
        community_area_polygons: (list) polygons within community area
        park_polygons: (list) park polygons within community area
        parks: csv file containing the following columns
        index: (str) park name
        latitude: (float)
        longitude: (float)
        size: (float) normalized park acreage
        community_area_name: (str)
    vacants: csv file containing the following columns
        index: (str) uniquely identifying pin
        latitude: (int)
        longitude: (int)
        community_area_name: (str)
        size: (float) normalized lot acres
"""

# Access Cook County & Chicago Data Portal API
print("10% - Accessing APIs...")
cook_county = Socrata("datacatalog.cookcountyil.gov", None)
chicago = Socrata("data.cityofchicago.org", None)
 
# Pull Cook County data on the classifications of all land parcels in Chicago
# https://datacatalog.cookcountyil.gov/Property-Taxation/ccgisdata-Parcel-2021/77tz-riq7
print("20% - Pulling vacancy data...")
vacant_api = cook_county.get("tnes-dgyi", select="pin", limit=2032408, where="class=0 OR class=100 OR class=190 OR "
                                                                                 "class=000 OR class=241")
vacant_pins = set()
for vacant in vacant_api:
    vacant_pins.add(vacant['pin'])

# Pull Chicago data on location and community area of all city-owned land parcels
print("30% - Pulling city-owned land data...")
# https://data.cityofchicago.org/Community-Economic-Development/City-Owned-Land-Inventory/aksk-kvfp
parcels_list_api = chicago.get("aksk-kvfp", select="pin, community_area_number, community_area_name, latitude, "
                                                       "longitude", limit=12810, where="property_status="
                                                                                       "'Owned by City'")

# Pull Chicago data on community area boundaries
print("40% - Pulling community area boundaries data...")
# https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6
community_areas_api = chicago.get("igwz-8jzy", select="the_geom, area_numbe, community", limit=77)
community_areas = {}
community_areas_num = {}
for community in community_areas_api:
    community_areas[community["community"]] = {'vacant_count': 0, 'vacant_acres': 0, 'park_count': 0,
                                               'park_acres': 0, 'census_tracts': [], 'community_area_polygons': [],
                                               'park_polygons': []}
    community_areas[community["community"]]['community_area_polygons'].append(community['the_geom'])
    community_areas_num[community['area_numbe']] = community['community']
pin_dict = {}
vacants = {}
for parcel in parcels_list_api:
    if "community_area_name" in parcel:
        if parcel["pin"] in vacant_pins:
            vacants[parcel["pin"]] = {'latitude': parcel['latitude'], 'longitude': parcel['longitude'],
                            'community_area_name': parcel['community_area_name'], 'size': None}
            community_areas[parcel["community_area_name"]]["vacant_count"] += 1
            pin_dict[parcel["pin"]] = parcel["community_area_name"]

# Pull Cook County data on the boundaries of all land parcels in Chicago
print("50% - Pulling land parcel boundaries data...")
# https://datacatalog.cookcountyil.gov/Property-Taxation/ccgisdata-Parcel-2021/77tz-riq7
shapefiles = cook_county.get("77tz-riq7", select="pin10, the_geom", limit=612202, where="municipality='Chicago'")
# Use boundaries of land parcels to calculate total area by community area (no alternative data available)
print("60% - Cleaning & converting land parcel data...")
geod = Geod(ellps="WGS84")
for shapefile in shapefiles:
    if "pin10" in shapefile:
        shapefile["pin"] = '-'.join([shapefile["pin10"][:2], shapefile["pin10"][2:4],
                                            shapefile["pin10"][4:7], shapefile["pin10"][7:10],
                                            shapefile["pin10"][10:]])
        shapefile["pin"] += "0000"
        if shapefile["pin"] in pin_dict:
            for polygon in shapefile["the_geom"]['coordinates']:
                community_areas[pin_dict[shapefile["pin"]]]["vacant_acres"] += \
                    abs(geod.geometry_area_perimeter(Polygon(polygon[0]))[0])*0.000247105
            vacants[shapefile["pin"]]["size"] = community_areas[pin_dict[shapefile["pin"]]]["vacant_acres"]

# Pull Chicago data on the boundaries, address, acreage and name of all parks
print("70% - Pulling park boundaries data...")
# https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr
parks_api = chicago.get("ejsh-fztr", select="the_geom, location, acres, park", limit=614)
print("80% - Cleaning & converting park data...")
# Clean address & convert to latitude & longitude (no singular lat long data available)
parks_api[374]['location'] = '1805 N Ridgeway Ave'
parks_api[10]['location'] = '5531 S King Dr'
parks_api[28]['location'] = '1400 S LINN WHITE DR'
parks_api[91]['location'] = '6935 W Addison St'
parks_api[136]['location'] = '3461 N Page Ave'
parks_api[239]['location'] = '2840 N Mozart St'
parks_api[290]['location'] = '4446 S Emerald Ave'
parks_api[302]['location'] = '5445 N Chester Ave'
parks_api[304]['location'] = 'E 87TH ST'
parks_api[323]['location'] = '4433 S St Lawrence Ave'
parks_api[335]['location'] = '2139 W Lexington St'
parks_api[336]['location'] = '630 N Kingsbury St'
parks_api[345]['location'] = '5914 N SHERIDAN RD'
parks_api[364]['location'] = '6426 N Kedzie Ave'
parks_api[369]['location'] = '10609 S Western Ave'
parks_api[377]['location'] = '353 N DESPLAINES ST'
parks_api[383]['location'] = '7211 N KEDZIE AVE'
parks_api[386]['location'] = '1629 S Wabash Ave'
parks_api[390]['location'] = '13298 S Torrence Ave'
parks_api[395]['location'] = '2754 S ELEANOR ST'
parks_api[448]['location'] = '7140 S. King Drive'
parks_api[463]['location'] = '230 N Kolmar Ave'
parks_api[480]['location'] = '1049 W Buena Ave'
parks_api[552]['location'] = '1701 N LaSalle Dr'
parks_api[591]['location'] = '3150 S Robinson St'
parks_api[596]['location'] = '10440 S CORLISS AVE'
parks_api[601]['location'] = '1601 W BLOOMINGDALE AVE'
parks_api[602]['location'] = '9202 S VANDERPOEL AVE'
parks_api[608]['location'] = '4149 S VINCENNES AVE'
parks_api[611]['location'] = '4826 S WESTERN AVE'
geolocator = Nominatim(user_agent="my_user_agent")
parks = {}
for park in parks_api:
    if type(park['location']) == str:
        park_location = geolocator.geocode(park['location'] + ', Chicago, US')
        parks[park['park']] = {'latitude': park_location.latitude, 'longitude': park_location.longitude,
                               'size': float(park['acres'])}
        point = Point(park_location.longitude, park_location.latitude)
        for community in community_areas:
            for multipolygon in community_areas[community]['community_area_polygons']:
                for polygon in multipolygon['coordinates'][0]:
                    if point.within(Polygon(polygon)):
                        parks[park['park']]['community_area_name'] = community
                        community_areas[community]['park_polygons'].append(park['the_geom'])
                        community_areas[community]['park_count'] += 1
                        community_areas[community]['park_acres'] += float(park['acres'])

# Pull Chicago data on the boundaries of all census tracts and the community areas they are within for matching
print("90% - Pulling census tract boundaries data...")
# https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik
census_tracts_api = chicago.get("74p9-q2aq", select="commarea, GEOID10")
for census_tract in census_tracts_api:
    community_areas[community_areas_num[census_tract["commarea"]]]["census_tracts"]\
        .append(census_tract["GEOID10"])
 
# Convert lists to pandas DataFrames & generate csv files
print("100% - Converting dictionaries to dataframes & generating csv files...")
parks_df = pd.DataFrame.from_dict(parks, orient='index')
parks_df["size"] = parks_df["size"] / parks_df["size"].abs().max()
parks_df.to_csv('parks.csv', index=True)
vacants_df = pd.DataFrame.from_dict(vacants, orient='index')
vacants_df["size"] = vacants_df["size"] / vacants_df["size"].abs().max()
vacants_df.to_csv('vacants.csv', index=True)
community_areas_df = pd.DataFrame.from_dict(community_areas, orient='index')
community_areas_df.reset_index(inplace=True)
community_areas_df = community_areas_df.rename(columns = {'index':'Neighborhood'})
community_areas_df.to_csv('community_areas.csv', index=True)
