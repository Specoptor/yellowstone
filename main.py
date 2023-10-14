import json

from models import Property
from data_extractor import Subdivision, PropertyExtractor

subdivision = Subdivision("YELLOWSTONE ADD", "YELLOWSTONE", "03")
subdivision.fetch_properties()

property_extractor = PropertyExtractor(subdivision.properties_html)
initial_property_data_list = property_extractor.extract_properties()

complete_property_data = []

for init_data in initial_property_data_list:
    prop = Property(init_property_data=init_data)
    complete_property_data.append(prop.data)

with open('samples_2.json', 'w') as f:
    json.dump(complete_property_data, f, indent=4)

