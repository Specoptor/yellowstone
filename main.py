import json

import requests
from requests import RequestException

from data_extractor import County, Subdivision, PropertyHTML, PropertyExtractor
from models import Property

county_name = "YELLOWSTONE"
county_id = "03"
subdivision_name = "THORN TREE SUB (10)"

def make_request_with_retry(url):
    MAX_RETRIES = 5
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=300)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            if response.content != b'':
                return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    raise Exception(f"API call failed after {MAX_RETRIES} retries")

if __name__ == '__main__':
    # Create a County object
    county = County(name=county_name, id=county_id)
    try:
        county.fetch_subdivisions()
    except RequestException as e:
        print(f"Error fetching subdivisions for {county_name}: {e}")


    # Create a Subdivision object
    subdivision = Subdivision(name=subdivision_name, county_id=county_id, county_name=county_name)
    try:
        subdivision.fetch_properties()
    except RequestException as e:
        print(f"Error fetching properties for {subdivision_name} in {county_name}: {e}")


    property_extractor = PropertyExtractor(subdivision.properties_html)
    properties = property_extractor.extract_properties()
    properties_data_list = []

    for prop in properties:
        geocode = prop['Geocode']
        property_html_object = PropertyHTML(geocode)
        try:
            property_html_object.fetch_all_data()
        except RequestException as e:
            print(f"Error fetching data for property with geocode {geocode}: {e}")
            continue  # Skip this property and move to the next one

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