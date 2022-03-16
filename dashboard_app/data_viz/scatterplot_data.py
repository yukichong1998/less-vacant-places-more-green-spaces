import pandas as pd

def neighborhood_zoom():
    boundaries = pd.read_csv('data_prep/data/comm_areas_map_params.csv')
    boundaries = boundaries.set_index("COMMUNITY")
    return boundaries

def scatter_data():

    parks = pd.read_csv('data_prep/data/parks.csv')
    parks['type'] = "Park"
    

    lots = pd.read_csv('data_prep/data/vacants.csv')
    lots['type'] = "Vacant Lot"

    both = pd.concat([parks, lots])
    both.columns = ['name', 'latitude', 'longitude', 'normalized_size', 'community_area_name', 'Land Use']
    both["name"].fillna("Vacant Lot", inplace=True)
    both['normalized_size'].fillna(both['normalized_size'].mean(), inplace=True)
 

    return both

