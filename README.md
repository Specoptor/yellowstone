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
