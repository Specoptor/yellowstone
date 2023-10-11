# Cadastral Data Directory Populator

This project provides a set of tools to fetch, organize, and store property data from the Montana Cadastral API. It organizes data in a directory structure based on counties, subdivisions, and individual properties identified by their geocodes.

## Project Structure

- **CadastralAPI**: Main API handler to communicate with the Montana Cadastral API.
- **County**: Represents a county and its associated subdivisions.
- **Subdivision**: Represents a subdivision within a county and its associated properties.
- **PropertyExtractor**: Utility to parse property data from HTML strings.

## Directory Structure

The data is stored in a nested directory structure:

```
data/
|-- counties/
    |-- [County Name]/
        |-- subdivision_list.json
        |-- [Subdivision Name]/
            |-- property_data.html
            |-- [Geocode]/
                |-- property_data.json
```

## Usage

1. To fetch and store data for all counties, subdivisions, and properties:

```python
from data_extractor import populate_directory_structure
populate_directory_structure()
```

2. To fetch and store data for a specific county:

```python
from data_extractor import populate_directory_for_county
populate_directory_for_county(county_id="03", county_name="YELLOWSTONE")
```

3. To fetch and store data for a specific subdivision within a county:

```python
from data_extractor import populate_directory_for_subdivision
populate_directory_for_subdivision(county_id="03", county_name="YELLOWSTONE", subdivision_name="49ER CONDO PHASE II")
```

## Error Handling

The project includes basic error handling for API responses and directory operations. If a specific API call fails, the program will skip that entry and move on to the next one.

## Dependencies

- Python 3.x
- `requests`: For making API calls.
- `BeautifulSoup` from `bs4`: For parsing HTML strings.

Install dependencies using:

```
pip install requests beautifulsoup4
```

## Future Work

- Integrate the Property Class with data extractor module to extract data from HTML strings.
- add pytests
- generate the csv file
- Add support for more detailed error handling.
- Integrate with a database for more structured data storage and querying.

Of course! Here's a README for the `Property` class:

---

# Property Class in models.py

The `Property` class is designed to represent a real estate property and extract relevant attributes from multiple types of HTML formatted strings.

## Features:

1. **Initialize with Optional HTML**: The class can be initialized with an optional HTML string to begin initial data extraction.
2. **Dynamic Attribute Updating**: Attributes of a property object can be updated dynamically by feeding different types of HTML formatted strings.
3. **Comprehensive Data Extraction**: The class is equipped to extract a wide range of property attributes such as geocode, legal description, owner details, building details, appraisal history, and more.

## Usage:

### Initialization

You can create a new property object by initializing the `Property` class. Optionally, you can provide an initial HTML string for data extraction:

```python
property_obj = Property(html_string=initial_html_data)
```

### Updating Attributes

After initialization, you can dynamically update the property attributes by feeding it different types of HTML formatted strings:

```python
property_obj.update_summary_data(summary_html_data)
property_obj.update_owner_details(owner_html_data)
property_obj.update_commercial_data(commercial_html_data)
property_obj.update_other_building_data(other_building_html_data)
property_obj.update_market_land_data(market_land_html_data)
property_obj.update_appraisal_history(appraisal_html_data)
```

### Accessing Attributes

Once the data has been parsed, you can access the property's attributes:

```python
print(property_obj.geocode)
print(property_obj.legal_description)
print(property_obj.owners)
# ... and so on for other attributes.
```

## Attributes:

The class extracts and stores the following attributes:

- `geocode`: Geographical code of the property.
- `legal_description`: Legal description of the property.
- `total_market_land`: Total market value of the land.
- `last_modified`: Date when the property details were last modified.
- `property_address`: Address of the property.
- `sub_category`: Subcategory of the property.
- `subdivision`: Subdivision details.
- `owners`: List of property owners and their details.
- `land_value`: Current year's land value.
- `building_value`: Current year's building value.
- `yoY_difference`: Year-on-Year difference in total property value.
- `building_details`: Details of the commercial buildings on the property.
- `other_building_details`: Details of other buildings or yard improvements.
- `market_land_details`: Details of the market land.

## Dependencies:

- **BeautifulSoup4**: The class uses BeautifulSoup for parsing HTML data.

---