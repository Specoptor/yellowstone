import json

import pandas as pd

from models import Property
from data_extractor import PropertyExtractor, CadastralAPI, County
from utils import flatten_json_to_df

county_list = CadastralAPI.get_counties()  # list of all counties in Montana

madison_county = County("25", "MADISON")
madison_county.fetch_subdivisions()
yellow_stone_subdivisions = [subdiv for subdiv in madison_county.subdivisions if 'yellowstone' in subdiv.name.lower()]

complete_property_data = []

# get all properties in each subdivision
for subdivision in yellow_stone_subdivisions:
    initial_property_data_list = []
    try:
        subdivision.fetch_properties()
        property_extractor = PropertyExtractor(subdivision.properties_html)
        initial_property_data_list = property_extractor.extract_properties()
        print(f"{len(initial_property_data_list)} properties successfully fetched from {subdivision.name}")
    except Exception as e:
        print(e)

    # get all api data for each property from initial data
    for idx, init_data in enumerate(initial_property_data_list):
        try:
            prop = Property(init_property_data=init_data)
            complete_property_data.append(prop.data)
            print(f"{idx+1} out of {len(initial_property_data_list)} properties successfully fetched")
        except:
            print("Error with property: ", init_data['Geocode'])

# The path where the flattened JSON will be saved
output_file_path = 'yellowstone_club_properties.json'

# Flattening the JSON data and converting to a list of dictionaries
flattened_data = [flatten_json_to_df(property_json)
                  for i, property_json in enumerate(complete_property_data) if property_json is not None]

# Writing the list of dictionaries to a JSON file
with open(output_file_path, 'w') as f:
    json.dump(flattened_data, f, indent=4)

df = pd.DataFrame(flattened_data)
df.to_csv('yellowstone_club_properties.csv', index=False)
