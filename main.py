import json

from data_extractor import County, Subdivision, PropertyHTML, PropertyExtractor
from models import Property

county_name = "YELLOWSTONE"
county_id = "03"
subdivision_name = "CASPIAN POINTE ESTATES (10)"

# Create a County object
county = County(name=county_name, id=county_id)
county.fetch_subdivisions()

if __name__ == '__main__':
    # Create a Subdivision object
    subdivision = Subdivision(name=subdivision_name, county_id=county_id, county_name=county_name)
    subdivision.fetch_properties()

    property_extractor = PropertyExtractor(subdivision.properties_html)
    properties = property_extractor.extract_properties()
    properties_data_list = []
    for prop in properties:
        property_html_object = PropertyHTML(prop['Geocode'])
        property_html_object.fetch_all_data()
        property = Property()
        property.update_summary_data(property_html_object.summary_data)
        property.update_commercial_data(property_html_object.commercial_data)
        property.update_market_land_data(property_html_object.market_land_data)
        property.update_other_building_data(property_html_object.other_building_data)
        property.update_appraisal_history(property_html_object.appraisal_data)
        property.update_owner_details(property_html_object.owner_data)
        properties_data_list.append(property.json())

    with open('samples.json', 'w') as f:
        json.dump(properties_data_list, f, indent=4)

