import pandas as pd

def neighborhood_zoom():
    boundaries = pd.read_csv('comm_areas_map_params.csv')
    boundaries = boundaries.set_index("COMMUNITY")
    return boundaries

def scatter_data():

    parks = pd.read_csv('parks.csv')
    park_areas = pd.read_csv('CPD_Parks.csv')
    parks['acres'] = park_areas['ACRES']
    parks['type'] = "Park"

    lots = pd.read_csv('vacants.csv')
    lots['type'] = "Vacant Lot"

    both = pd.concat([parks, lots])
    both["name"].fillna("Vacant Lot", inplace=True)
    both["acres"].fillna(10.0, inplace=True)

    return both

