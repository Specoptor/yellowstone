import time

import requests
import os

import re
import json

from bs4 import BeautifulSoup

from api_caller import ApiCaller

caller = ApiCaller()

BASE_URL = "https://svc.mt.gov/msl/legacycadastralapi"


class CadastralAPI:
    """
    Utility class to handle API calls to the Cadastral API.
    """

    @staticmethod
    def get_counties():
        """
        Fetch the list of all counties.

        :return: List of counties from the API.
        """
        url = f"{BASE_URL}/search/getcountylist"
        response = caller.get(url)
        return response.json()

    @staticmethod
    def get_subdivisions(county_id):
        """
        Fetch subdivisions for a given county.

        :param county_id: ID of the county.
        :return: List of subdivisions for the specified county.
        """
        url = f"{BASE_URL}/search/getsubdivisionlist?countyid={county_id}"
        response = caller.get(url)
        return response.json()

    @staticmethod
    def get_properties_by_subdivision(subdivision_name, county_id):
        """
        Fetch properties for a given subdivision and county.

        :param subdivision_name: Name of the subdivision.
        :param county_id: ID of the county.
        :return: List of properties for the specified subdivision and county.
        """

        def clean_json_string(data_str):
            """
            Replace invalid escape sequences in a JSON string.

            :param data_str: The JSON string to clean.
            :return: Cleaned JSON string.
            """
            return re.sub(r'\\(?![/u"bfnrt])', r'\\\\', data_str)

        url = f"{BASE_URL}/search/searchbysubdivision?subdivision={subdivision_name}&countyid={county_id}"
        response = caller.get(url)

        # the code below is to handle the case when the API returns an empty response.
        # For some reason the response is empty sometimes, so we try to fetch the data again.
        # If the response is still empty after 5 tries, we raise an exception.
        if response.content == b'':
            for _ in range(5):
                response = caller.get(url)
                if response.content != b'':
                    break
            else:
                raise Exception("API call failed")

        decoded_response = response.content.decode("utf-8")
        formatted_response = clean_json_string(decoded_response)
        return json.loads(formatted_response)


class Subdivision:
    def __init__(self, name, county_name, county_id):
        """
        Initializes a Subdivision object.

        :param name: Name of the subdivision.
        :param county_name: Name of the county.
        :param county_id: ID of the county.
        """
        self.name = name
        self.county_name = county_name
        self.county_id = county_id
        self.properties_html = ""

    def fetch_properties(self):
        """
        Fetch property data HTML for the subdivision.

        :return: None
        """
        properties_data = CadastralAPI.get_properties_by_subdivision(self.name, self.county_id)
        # assuming that the properties_data variable is the HTML formatted string
        self.properties_html = properties_data

    def save_properties(self):
        """
        Save property data HTML for the subdivision to a JSON file.

        :return: None
        """
        directory = os.path.join("data", "counties", self.county_name, self.name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, "properties_list.json")
        save_to_json({"properties_html": self.properties_html}, filepath)

    def extract_and_save_properties(self, county_directory):
        """
        Extract property details from the HTML data and create directories using their geocodes.

        :param county_directory: The directory path where the county data is stored.
        :return: None
        """
        subdivision_directory = os.path.join(county_directory, self.name)

        extractor = PropertyExtractor(self.properties_html)
        properties = extractor.extract_properties()

        for prop in properties:
            geocode_dir = os.path.join(subdivision_directory, prop["Geocode"])
            if not os.path.exists(geocode_dir):
                os.makedirs(geocode_dir)
            with open(os.path.join(geocode_dir, 'property_data.json'), 'w') as file:
                json.dump(prop, file)


class County:
    def __init__(self, id, name):
        """
        Initializes a County object.

        :param id: ID of the county.
        :param name: Name of the county.
        """
        self.id = id
        self.name = name
        self.subdivisions = []

    def fetch_subdivisions(self):
        """
        Fetch and store subdivisions for the county.

        :return: None
        """
        subdivisions_data = CadastralAPI.get_subdivisions(self.id)
        for subdiv in subdivisions_data:
            if subdiv['Subdiv']:
                self.subdivisions.append(Subdivision(subdiv['Subdiv'], self.name, self.id))

    def save_subdivisions(self):
        """
        Save list of subdivisions for the county at its root directory.

        :return: None
        """
        directory = os.path.join("data", "counties", self.name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, "subdivision_list.json")
        save_to_json([subdiv.name for subdiv in self.subdivisions], filepath)


class PropertyHTML:
    def __init__(self, geocode, year=2023):
        """
        Initializes a Property object.

        :param geocode: The unique identifier for the property.
        :param year: The year of interest for fetching data, default is 2023.
        """
        self.geocode = geocode
        self.year = year
        self.summary_data = None
        self.owner_data = None
        self.appraisal_data = None
        self.market_land_data = None
        self.dwelling_data = None
        self.other_building_data = None
        self.commercial_data = None
        self.agricultural_data = None
        self.time_taken_summary = None
        self.time_taken_owner = None
        self.time_taken_appraisal = None
        self.time_taken_market_land = None
        self.time_taken_dwelling = None
        self.time_taken_other_building = None
        self.time_taken_commercial = None
        self.time_taken_agricultural = None

    def fetch_summary_data(self):
        """
        Fetch and store summary data for the property.

        :return: None
        """
        url = f"{BASE_URL}/summary/getsummarydata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_summary = elapsed
        self.summary_data = response.content.decode('utf-8')

    def fetch_owner_data(self):
        """
        Fetch and store owner data for the property.

        :return: None
        """
        url = f"{BASE_URL}/owner/getownerdata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_owner = elapsed
        self.owner_data = response.content.decode('utf-8')

    def fetch_appraisal_data(self):
        """
        Fetch and store appraisal data for the property.

        :return: None
        """
        url = f"{BASE_URL}/appraisal/getappraisaldata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_appraisal = elapsed
        self.appraisal_data = response.content.decode('utf-8')

    def fetch_market_land_data(self):
        """
        Fetch and store market land data for the property.

        :return: None
        """
        url = f"{BASE_URL}/marketland/getmarketlanddata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_market_land = elapsed
        self.market_land_data = response.content.decode('utf-8')

    def fetch_dwelling_data(self):
        """
        Fetch and store dwelling data for the property.

        :return: None
        """
        url = f"{BASE_URL}/dwelling/getdwellingdata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_dwelling = elapsed
        self.dwelling_data = response.content.decode('utf-8')

    def fetch_other_building_data(self):
        """
        Fetch and store other building data for the property.

        :return: None
        """
        url = f"{BASE_URL}/otherbuilding/getotherbuildingdata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_other_building = elapsed
        self.other_building_data = response.content.decode('utf-8')

    def fetch_commercial_data(self):
        """
        Fetch and store commercial data for the property.

        :return: None
        """
        url = f"{BASE_URL}/commercial/getcommercialdata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_commercial = elapsed
        self.commercial_data = response.content.decode('utf-8')

    def fetch_agricultural_data(self):
        """
        Fetch and store agricultural data for the property.

        :return: None
        """
        url = f"{BASE_URL}/agforest/getagforestdata?geocode={self.geocode}&year={self.year}"
        start = time.time()
        response = caller.get(url)
        elapsed = round(time.time() - start, 2)
        self.time_taken_agricultural = elapsed
        self.agricultural_data = response.content.decode('utf-8')

    def fetch_all_data(self):
        """
        Fetch and store all data types for the property.

        :return: None
        """
        self.fetch_summary_data()
        self.fetch_owner_data()
        self.fetch_appraisal_data()
        self.fetch_market_land_data()
        self.fetch_dwelling_data()
        self.fetch_other_building_data()
        self.fetch_commercial_data()
        self.fetch_agricultural_data()

    def time_taken(self):
        """
        Return the time taken for each API call.
        :return: a dictionary of time taken for each API call
        """
        return {"Geocode": self.geocode,
                "summary": self.time_taken_summary,
                "commercial": self.time_taken_commercial,
                "owner": self.time_taken_owner,
                "appraisal": self.time_taken_appraisal,
                "market_land": self.time_taken_market_land,
                "other_building": self.time_taken_other_building,
                "dwelling": self.time_taken_dwelling,
                "agricultural": self.time_taken_agricultural,
                }


def populate_directory_structure():
    """
    Populate the directory structure:
    1. Fetch all counties and save them.
    2. For each county, fetch all subdivisions, save them,
       and then fetch and save all properties for each subdivision.

    :return: None
    """

    def get_existing_subdivisions(county_directory):
        """
        Get a list of existing subdivisions for a given county from the subdivision_list.json file.

        :param county_directory: Path to the county directory.
        :return: List of existing subdivisions, or an empty list if the file doesn't exist.
        """
        subdivisions_filepath = os.path.join(county_directory, "subdivision_list.json")
        if os.path.exists(subdivisions_filepath):
            with open(subdivisions_filepath, 'r') as file:
                return json.load(file)
        return []

    # Initialize the CadastralAPI
    api = CadastralAPI()

    # Fetch all counties
    counties_content = api.get_counties()
    all_counties = [County(data['Id'], data['Name']) for data in counties_content]

    for county in all_counties:
        county_directory = os.path.join("data", "counties", county.name)
        existing_subdivisions = get_existing_subdivisions(county_directory)

        # Fetch and save subdivisions for the current county
        county.fetch_subdivisions()

        # Only save and fetch properties for new subdivisions
        new_subdivisions = [subdiv for subdiv in county.subdivisions if subdiv.name not in existing_subdivisions]
        county.subdivisions = new_subdivisions
        county.save_subdivisions()

        for subdivision in new_subdivisions:
            subdivision.fetch_properties()
            subdivision.save_properties()
            subdivision.extract_and_save_properties(county_directory)


def populate_directory_for_county(county_id, county_name):
    """
    Populate directories for a specific county.

    :param county_id: The ID of the county.
    :param county_name: The name of the county.
    :return: None
    """
    county = County(county_id, county_name)
    county_directory = os.path.join("data", "counties", county_name)
    county.fetch_subdivisions()
    county.save_subdivisions()

    for subdivision in county.subdivisions:
        subdivision.fetch_properties()
        subdivision.save_properties()
        subdivision.extract_and_save_properties(county_directory)


def populate_directory_for_subdivision(county_id, county_name, subdivision_name):
    """
    Populate directories for a specific subdivision within a given county.

    :param county_name: The name of the county.
    :param subdivision_name: The name of the subdivision.
    :return: None
    """
    county = County(county_id, county_name)
    subdivision = Subdivision(name=subdivision_name, county_id=county.id, county_name=county.name)
    county_directory = os.path.join("data", "counties", county_name)

    subdivision.fetch_properties()
    subdivision.save_properties()
    subdivision.extract_and_save_properties(county_directory)


def save_to_json(data, filepath):
    """
    Utility function to save data as JSON to the specified filepath.

    :param data: Data to be saved.
    :param filepath: Path where the data should be saved.
    """
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


class PropertyExtractor:
    def __init__(self, property_html):
        """
        Initializes a PropertyExtractor object.

        :param property_html: The HTML string containing property details.
        """
        self.soup = BeautifulSoup(property_html, 'html.parser')

    def extract_properties(self):
        """
        Extracts properties details from the HTML using anchors in the string.

        :return: List of dictionaries with property details.
        """
        property_divs = self.soup.find_all("div", class_=["searchResult", "searchResultAltRow"])

        properties = []

        for div in property_divs:
            title = div['title']

            # Extract information using known labels as anchors
            address_start = title.find("Address:") + len("Address:")
            address_end = title.find("Geocode:")
            geocode_start = address_end + len("Geocode:")
            geocode_end = title.find("Legal Description:")

            address = title[address_start:address_end].strip()
            geocode = title[geocode_start:geocode_end].strip()
            legal_description = title[geocode_end + len("Legal Description:"):].strip()

            owner_name = div.find("input")["value"]

            properties.append({
                "Owner Name": owner_name,
                "Geocode": geocode,
                "Address": address,
                "Legal Description": legal_description
            })

        return properties


if __name__ == "__main__":
    # populate_directory_structure()
    # populate_directory_for_county("03", "YELLOWSTONE")
    populate_directory_for_subdivision("03", "YELLOWSTONE", "YELLOWSTONE ADD")
