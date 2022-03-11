from sodapy import Socrata
import pandas as pd
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon


def city_owned_property():

    # Access Cook County Data Portal API
    cook_county = Socrata("datacatalog.cookcountyil.gov", None)
    # Access City of Chicago Data Portal API
    chicago = Socrata("data.cityofchicago.org", None)

    # https://datacatalog.cookcountyil.gov/Property-Taxation/ccgisdata-Parcel-2021/77tz-riq7
    # Pins for vacant land, including sideyards & unclassified land
    vacant = cook_county.get("tnes-dgyi", select="pin", where="class=0 OR class=100 OR class=190 OR "
                                                                             "class=000 OR class=241")
    vacant_pins = set()
    for val in vacant:
        vacant_pins.add(val['pin'])

    # https://data.cityofchicago.org/Community-Economic-Development/City-Owned-Land-Inventory/aksk-kvfp
    # Pins, square footage, and locations(lat, lon) for city-owned property
    parcels_list = chicago.get("aksk-kvfp", select="pin, community_area_number, community_area_name",
                               where="property_status='Owned by City'")
    # https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6
    community_areas = chicago.get("igwz-8jzy", select="the_geom, area_numbe, community")
    community_areas_dict = {}
    for community in community_areas:
        community_areas_dict[community["community"]] = {"vacant_count":0}
    pin_dict = {}
    for idx, _ in enumerate(parcels_list):
        if "community_area_name" in parcels_list[idx]:
            if parcels_list[idx]["pin"] in vacant_pins:
                community_areas_dict[parcels_list[idx]["community_area_name"]]["vacant_count"] += 1
                pin_dict[parcels_list[idx]["pin"]] = parcels_list[idx]["community_area_name"]
                if pin_dict[parcels_list[idx]["pin"]] == "EDISON PARK":
                    print("True")
    # https://datacatalog.cookcountyil.gov/Property-Taxation/ccgisdata-Parcel-2021/77tz-riq7
    # Pins and shapefiles for all property polygons
    shapefiles = cook_county.get("77tz-riq7", select="pin10, the_geom", where="municipality='Chicago'")
    for idx, _ in enumerate(shapefiles):
        if "pin10" in shapefiles[idx]:
            shapefiles[idx]["pin"] = '-'.join([shapefiles[idx]["pin10"][:2], shapefiles[idx]["pin10"][2:4],
                                               shapefiles[idx]["pin10"][4:7], shapefiles[idx]["pin10"][7:10],
                                               shapefiles[idx]["pin10"][10:]])
            shapefiles[idx]["pin"] += "0000"
            if shapefiles[idx]["pin"] in pin_dict:
                if "vacant_polygons" not in community_areas_dict[pin_dict[shapefiles[idx]["pin"]]]:
                    community_areas_dict[pin_dict[shapefiles[idx]["pin"]]]["vacant_polygons"] = []
                community_areas_dict[pin_dict[shapefiles[idx]["pin"]]]["vacant_polygons"]\
                    .append(shapefiles[idx]["the_geom"])

    # https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr
    # Shapefiles, location, and acreage for park polygons
    parks = chicago.get("ejsh-fztr", select="the_geom, location, acres")
    # Clean location & convert to latitude & longitude
    parks[374]['location'] = '1805 N Ridgeway Ave'
    parks[10]['location'] = '5531 S King Dr'
    parks[28]['location'] = '1400 S LINN WHITE DR'
    parks[91]['location'] = '6935 W Addison St'
    parks[136]['location'] = '3461 N Page Ave'
    parks[239]['location'] = '2840 N Mozart St'
    parks[290]['location'] = '4446 S Emerald Ave'
    parks[302]['location'] = '5445 N Chester Ave'
    parks[304]['location'] = 'E 87TH ST'
    parks[323]['location'] = '4433 S St Lawrence Ave'
    parks[335]['location'] = '2139 W Lexington St'
    parks[336]['location'] = '630 N Kingsbury St'
    parks[345]['location'] = '5914 N SHERIDAN RD'
    parks[364]['location'] = '6426 N Kedzie Ave'
    parks[369]['location'] = '10609 S Western Ave'
    parks[377]['location'] = '353 N DESPLAINES ST'
    parks[383]['location'] = '7211 N KEDZIE AVE'
    parks[386]['location'] = '1629 S Wabash Ave'
    parks[390]['location'] = '13298 S Torrence Ave'
    parks[395]['location'] = '2754 S ELEANOR ST'
    parks[448]['location'] = '7140 S. King Drive'
    parks[463]['location'] = '230 N Kolmar Ave'
    parks[480]['location'] = '1049 W Buena Ave'
    parks[552]['location'] = '1701 N LaSalle Dr'
    parks[591]['location'] = '3150 S Robinson St'
    parks[596]['location'] = '10440 S CORLISS AVE'
    parks[601]['location'] = '1601 W BLOOMINGDALE AVE'
    parks[602]['location'] = '9202 S VANDERPOEL AVE'
    parks[608]['location'] = '4149 S VINCENNES AVE'
    parks[611]['location'] = '4826 S WESTERN AVE'
    geolocator = Nominatim(user_agent="my_user_agent")
    park_location_sqft = []
    for index, _ in enumerate(parks):
        print(index)
        parks[index]['polygon'] = parks[index]['the_geom']['coordinates'][0]
        parks[index]['acres'] = float(parks[index]['acres'])
        if type(parks[index]['location']) == str:
            park_location = geolocator.geocode(parks[index]['location'] + ', Chicago, US')
            park_location_sqft.append((Point(park_location.longitude, park_location.latitude), parks[index]['acres'],
                                       parks[index]['the_geom']))

    # Shapefiles for community area polygons
    community_areas_num = {}
    for index, _ in enumerate(community_areas):
        print(index)
        community_areas_num[community_areas[index]['area_numbe']] = community_areas[index]['community']
        if community_areas[index]['community'] not in community_areas_dict:
            community_areas_dict[community_areas[index]['community']] = {}
        community_areas_dict[community_areas[index]['community']]['park_count'] = 0
        community_areas_dict[community_areas[index]['community']]['park_acres'] = 0
        community_areas_dict[community_areas[index]['community']]['park_polygons'] = []
        community_area_polygon = Polygon(community_areas[index]['the_geom']['coordinates'][0][0])
        for park_index, (point, acres, the_geom) in enumerate(park_location_sqft):
            if point.within(community_area_polygon):
                community_areas_dict[community_areas[index]['community']]['park_count'] += 1
                community_areas_dict[community_areas[index]['community']]['park_acres'] += int(acres)
                community_areas_dict[community_areas[index]['community']]['park_polygons'].append(the_geom)

    # https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik
    # Shapefiles for census tract polygons
    census_tracts = chicago.get("74p9-q2aq", select="commarea, GEOID10")
    for index, _ in enumerate(census_tracts):
        if "census_tracts" not in community_areas_dict[community_areas_num[census_tracts[index]["commarea"]]]:
            community_areas_dict[community_areas_num[census_tracts[index]["commarea"]]]["census_tracts"] = []
        community_areas_dict[community_areas_num[census_tracts[index]["commarea"]]]["census_tracts"]\
            .append(census_tracts[index]["GEOID10"])

    # Convert lists to pandas DataFrames & combine
    community_areas_df = pd.DataFrame.from_dict(community_areas_dict, orient='index')
    community_areas_df.reset_index(inplace=True)
    community_areas_df = community_areas_df.rename(columns = {'index':'Neighborhood'})
    community_areas_df.to_csv('community_areas.csv', index=True)
    
    return community_areas_df
