from bs4 import BeautifulSoup

from data_extractor import PropertyHTML
from utils import extract_key_value_pairs, is_empty_response


class SummaryExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the SummaryExtractor with the provided HTML string. It is intended to extract
        the summary information from the summary html string.

        :param html_string: an html formatted string
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> dict[str, str]:
        """
        Extracts the relevant data points from the HTML string.

        :return: A dictionary containing the extracted data points.
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return {}

        data = {}

        for table in self.soup.find_all('table'):
            data.update(extract_key_value_pairs(table))

        return data


class OwnerExtractor:
    """
    A class to extract owner information from a given HTML string.
    """

    def __init__(self, html_string: str) -> None:
        """
        Initializes the OwnerExtractor with the provided HTML string.

        :param html_string (str): The HTML content to be parsed.
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> dict:
        """
        Extracts owner information, including the default information, ownership percentage,
        primary owner status, interest type, and last modified data.

        :return: A dictionary containing extracted owner information.
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return {}

        owner_data = {}
        owner_table = self.soup.find('table')
        if owner_table:
            owner_data.update(extract_key_value_pairs(owner_table))
        return owner_data


class AppraisalExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the AppraisalExtractor with the provided HTML string.

        :param html_string:
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()
        self.compute_year_on_year_difference()

    def extract_data(self) -> list[dict]:
        """
        Extracts the appraisal history from the HTML string.

        :return:
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return []

        rows = self.soup.select("table.subTable tr")[1:]  # Skipping header row
        appraisals = []

        for row in rows:
            columns = row.select("td")
            appraisal = {
                "Tax Year": int(columns[0].get_text(strip=True)),
                "Land Value": float(columns[1].get_text(strip=True)),
                "Building Value": float(columns[2].get_text(strip=True)),
                "Total Value": float(columns[3].get_text(strip=True)),
                "Method": columns[4].get_text(strip=True)
            }
            appraisals.append(appraisal)

        return appraisals

    def compute_year_on_year_difference(self) -> None:
        """
        Computes the year-on-year difference for each appraisal year, if a preceding year exists.

        It updates the appraisal data in place.
        :return:
        """
        if len(self.data) < 2:
            return

        for i in range(len(self.data) - 1):
            current_year = self.data[i]
            previous_year = self.data[i + 1]

            current_year["Land Value YoY"] = current_year["Land Value"] - previous_year["Land Value"]
            current_year["Building Value YoY"] = current_year["Building Value"] - previous_year["Building Value"]
            current_year["Total Value YoY"] = current_year["Total Value"] - previous_year["Total Value"]


class DwellingExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the DwellingExtractor with the provided HTML string.

        :param html_string:
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> dict:
        """
        Extracts the dwelling details from the HTML string.
        :return:
        """

        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return {}

        dwelling_data = {}

        # Extract key-value pairs
        tables = self.soup.find_all('table')
        for table in tables:
            dwelling_data.update(extract_key_value_pairs(table))

        return dwelling_data


class OtherBuildingExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the OtherBuildingExtractor with the provided HTML string.

        :param html_string:
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> list[dict]:
        """
        Extracts the building details from the HTML string.
        :return:
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return []

        building_data = []
        building_table = self.soup.find_all('table')
        for table in building_table:
            building_data.append(extract_key_value_pairs(table))

        return building_data


class MarketLandExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the MarketLandExtractor with the provided HTML string.

        :param html_string:
        """

        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> dict:
        """
        Extracts the market land details from the HTML string.

        :return:
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return {}

        market_land_data = {}
        market_land_tables = self.soup.find_all('table')
        for table in market_land_tables:
            market_land_data.update(extract_key_value_pairs(table))

        return market_land_data


class CommercialExtractor:
    def __init__(self, html_string: str) -> None:
        """
        Initializes the CommercialExtractor with the provided HTML string.

        :param html_string:
        """
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.data = self.extract_data()

    def extract_data(self) -> dict:
        """
        Extracts general building information, interior/exterior data,
        other building features, and elevator/escalator details.

        :return:
        """
        # Check for empty response
        if is_empty_response(self.soup.get_text()):
            return {}

        commercial_data = {}

        # Extract key-value pairs
        tables = self.soup.find_all('table')
        for table in tables:
            commercial_data.update(extract_key_value_pairs(table))

        return commercial_data