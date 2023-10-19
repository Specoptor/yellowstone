import json

from models import Property
from data_extractor import PropertyExtractor, CadastralAPI, County

county_list = CadastralAPI.get_counties()  # list of all counties in Montana4

madison_county = County("25", "MADISON")
madison_county.fetch_subdivisions()
yellow_stone_subdivisions = [subdiv for subdiv in madison_county.subdivisions if 'yellowstone' in subdiv.name.lower()]

complete_property_data = []

# get all properties in each subdivision
for subdivision in yellow_stone_subdivisions:
    subdivision.fetch_properties()
    property_extractor = PropertyExtractor(subdivision.properties_html)
    initial_property_data_list = property_extractor.extract_properties()

    # get all api data for each property from initial data
    for init_data in initial_property_data_list:
        prop = Property(init_property_data=init_data)
        complete_property_data.append(prop.data)

with open('yellowstone_club_properties.json', 'w') as f:
    json.dump(complete_property_data, f, indent=4)
