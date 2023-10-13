from bs4 import BeautifulSoup
from utils import extract_key_value_pairs, decode_html


class Property:
    """
    Represents a property with various attributes extracted from multiple types of HTML formatted strings.
    """

    def __init__(self, html_string: str = None) -> None:
        """
        Initializes a Property object with optional initial parsing.

        :param html_string: Optional initial HTML string for parsing.
        """
        self.soup = BeautifulSoup(html_string, 'html.parser') if html_string else None

        # Property attributes
        self.geocode = None
        self.legal_description = None
        self.total_market_land = None
        self.last_modified = None
        self.property_address = None
        self.sub_category = None
        self.subdivision = None
        self.owners = []
        self.land_value = None
        self.building_value = None
        self.yoY_difference = None
        self.building_details = []
        self.other_building_details = []
        self.market_land_details = []

        # If an initial HTML string is provided, conduct an initial extraction of data.
        if self.soup:
            self._initial_extraction()

    def _initial_extraction(self) -> None:
        """Conducts initial data extraction if an HTML string is provided during object initialization."""
        self.geocode = self._extract_data_by_key("Geocode:")
        self.legal_description = self._extract_data_by_search_term("Legal Description:")
        self.total_market_land = self._extract_data_by_search_term("Total Market Land")
        self.last_modified = self._extract_data_by_key("Last Modified:")
        self.property_address = self._extract_data_by_key("Property Address:")
        self.sub_category = self._extract_data_by_key("Subcategory:")
        self.subdivision = self._extract_data_by_key("Subdivision:")
        self.owners = self._extract_owner_details()

    def update_html(self, html_string: str) -> None:
        """
        Updates the BeautifulSoup object with a new HTML string.

        :param html_string: New HTML string for parsing.
        """
        clean_html = decode_html(html_string)
        self.soup = BeautifulSoup(clean_html, 'html.parser')

    def _extract_data_by_key(self, key: str) -> str | None:
        """
        Extracts data from the HTML content based on a specific key.

        :param key: The key/label used to locate the data in the HTML content.
        :return: Extracted data corresponding to the key or None if not found.
        """
        if not self.soup:
            return None
        key_span = self.soup.find('span', text=key)
        if key_span:
            value_span = key_span.find_next_sibling('span', class_='value')
            if value_span:
                return value_span.text.strip()
        return None

    def _extract_data_by_search_term(self, term: str) -> str | None:
        """
        Extracts data from the HTML content based on a search term.

        :param term: The term used to locate the data in the HTML content.
        :return: Extracted data corresponding to the term or None if not found.
        """
        if not self.soup:
            return None
        term_element = self.soup.find(string=lambda text: term.lower() in text.lower())
        if term_element:
            value_span = term_element.find_next('span', class_='value')
            if value_span:
                return value_span.text.strip()
        return None

    def _extract_owner_details(self) -> list[dict[str, str]]:
        """
        Extracts owner details from the HTML content.

        :return: A list of dictionaries containing owner details.
        """
        if not self.soup:
            return []
        owner_details = []
        party_sections = self.soup.find_all('td', class_='darkHeader')
        for section in party_sections:
            owner_info = {}
            rows = section.find_all_next('tr', limit=6)
            for row in rows[1:]:
                key_element = row.find('span', class_='key')
                value_element = row.find('span', class_='value')
                if key_element and value_element:
                    owner_info[key_element.text.strip()] = value_element.text.strip()
            if owner_info:
                owner_details.append(owner_info)
        return owner_details

    def update_owner_details(self, html_string) -> None:
        """
        Parses owner details from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing owner details.
        """
        self.update_html(html_string)
        self.owners = self._extract_owner_details()

    def update_appraisal_history(self, html_string: str) -> None:
        """
        Parses appraisal history from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing appraisal history.
        """
        self.update_html(html_string)
        rows = self.soup.find_all('tr')[1:]
        current_year_data = rows[0].find_all('td')
        self.land_value = int(current_year_data[1].text)
        self.building_value = int(current_year_data[2].text)
        total_value_2023 = int(current_year_data[3].text)
        if len(rows) > 1:
            total_value_2022 = int(rows[1].find_all('td')[3].text)
            self.yoY_difference = total_value_2023 - total_value_2022

    def update_summary_data(self, html_string: str) -> None:
        """
        Parses summary data from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing summary data.
        """
        self.update_html(html_string)
        self.geocode = self._extract_data_by_key("Geocode:")
        self.legal_description = self._extract_data_by_search_term("Legal Description:")
        self.total_market_land = self._extract_data_by_search_term("Total Market Land")
        self.last_modified = self._extract_data_by_key("Last Modified:")
        self.property_address = self._extract_data_by_key("Property Address:")
        self.sub_category = self._extract_data_by_key("Subcategory:")
        self.subdivision = self._extract_data_by_key("Subdivision:")

    def update_commercial_data(self, html_string: str) -> None:
        """
        Parses commercial building details from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing commercial building details.
        """
        self.update_html(html_string)
        building_rows = self.soup.find_all('tr')
        self.building_details = []
        for row in building_rows:
            columns = row.find_all('td')
            building_info = extract_key_value_pairs(columns)
            self.building_details.append(building_info)

    def update_other_building_data(self, html_string: str) -> None:
        """
        Parses other building or yard improvement details from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing other building or yard improvement details.
        """
        self.update_html(html_string)
        building_rows = self.soup.find_all('tr')[1:]
        self.other_building_details = []
        for row in building_rows:
            columns = row.find_all('td')
            other_building_info = extract_key_value_pairs(columns)
            self.other_building_details.append(other_building_info)

    def update_market_land_data(self, html_string: str) -> None:
        """
        Parses market land data from the provided HTML string and updates the relevant attributes.

        :param html_string: HTML string containing market land data.
        """
        self.update_html(html_string)
        land_rows = self.soup.find_all('tr')[1:]
        self.market_land_details = []
        for row in land_rows:
            columns = row.find_all('td')
            land_info = extract_key_value_pairs(columns)
            self.market_land_details.append(land_info)

    def json(self) -> dict[str, str | int | list[dict[str, str]] | None]:
        """
        Returns a dictionary representation of the Property object. It excludes the soup attribute.

        :return: a dictionary representation of the Property object.
        """
        attributes = {}
        for key, value in self.__dict__.items():
            if key != "soup":
                attributes[key] = value
        return attributes
