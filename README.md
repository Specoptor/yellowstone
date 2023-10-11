
### API Response Time Analysis

#### 1. Introduction
This notebook aims to analyze and visualize the response times of various API calls. By understanding the performance characteristics of these APIs, we can identify bottlenecks, optimize response times, and ensure efficient service for end-users.

#### 2. Data Acquisition
The data for this analysis comes from a JSON file that contains property objects. Each object has:
- A `Geocode` for identifying the property.
- Several keys representing different API calls.
- Values associated with these keys which are the response times for those API calls.

To load the data into the notebook:
```python
import json

# Load the JSON data from the file
with open("path_to_file", "r") as file:
    data = json.load(file)
```

#### 3. Data Exploration and Visualization

After loading the data, the notebook takes the following steps to visualize it:

##### 3.1 Box Plot
The box plot provides a visual summary of the distribution of response times for each API call. It helps in identifying the central tendency, variability, and presence of outliers in the data.

```python
import matplotlib.pyplot as plt

# Create a box plot
plt.boxplot(data)
```

##### 3.2 Histograms
Histograms offer insights into the frequency distribution of response times for each API call. They are essential for understanding the shape and spread of each distribution.

```python
data.hist()
```

##### 3.3 Density Plots
Density plots give a smoothed representation of the distribution of response times for each API call. They help in identifying where the bulk of response times are concentrated.

```python
data.plot(kind='density')
```

##### 3.4 Violin Plots
Violin plots combine aspects of box plots and density plots. They offer a deeper insight into the distribution of response times for each API call.

```python
import seaborn as sns

sns.violinplot(data=data)
```

##### 3.5 Cumulative Distribution Function (CDF) Plots
CDF plots show the probability that a response time will be less than or equal to a particular value. They are useful for understanding the percentage of calls that finish within a certain timeframe.

```python
data.hist(cumulative=True, density=1)
```

#### 4. Conclusion
Through the visualizations in this notebook, we gain a comprehensive understanding of the performance characteristics of various API calls. These insights are valuable for optimizing the performance of the APIs and ensuring a smooth user experience.

___

# Montana Cadastral Data Extractor

This project provides a set of tools to fetch, organize, and store property data from the Montana Cadastral API. It
organizes data in a directory structure based on counties, subdivisions, and individual properties identified by their
geocodes.

___

## Module Documentation

### api_caller.py

This module handles API interactions, managing API calls to fetch data. It ensures proper error handling and efficient
parsing of API responses.

### data_extractor.py

This module offers utilities for data extraction and organization. It defines classes and methods to facilitate the
parsing of property data fetched from the Montana Cadastral API.

### decorators.py

This module defines decorators that can be used across the project. These decorators provide utility functions enhancing
or modifying the behavior of other functions or methods.

### main.py

A demonstration script showing how to utilize the data extraction tools provided in this project. Refer to the earlier
section for a detailed breakdown.

### models.py

Defines the `Property` class representing individual property data. The class provides methods for parsing and updating
its attributes from various HTML formatted strings.

### requirements.txt

A list of dependencies that need to be installed for the successful execution of the project.

### svc_endpoints.py

A collection of endpoints that facilitate communication with the Montana Cadastral API.

### samples.json & samples_timer.json

Sample output files generated by the `main.py` script, providing a snapshot of the kind of data the project can extract
and organize.

---

## Classes in data_extractor.py

- **CadastralAPI**: Main API handler to communicate with the Montana Cadastral API.
- **County**: Represents a county and its associated subdivisions.
- **Subdivision**: Represents a subdivision within a county and its associated properties.
- **PropertyExtractor**: Utility to parse property data from HTML strings.
- **PropertyHTML**: Utility to parse property data from HTML strings.

___

## Directory Structure by calling populate_directory_structure()

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

___

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

___

## Error Handling

The project includes basic error handling for API responses and directory operations. Need for robust error handling is
required.

___

## Dependencies

- Python 3.x
- `requests`: For making API calls.
- `BeautifulSoup` from `bs4`: For parsing HTML strings.

Install dependencies using:

```
pip install requests beautifulsoup4
```

___

## Future Work

- Validate the data passed to the Property class
- Add remaining attributes to the Property class
- Identify which datapoints have been acquired and remain to be acquired.
- Implement a more robust error handling mechanism
- Analyze performance of the API calls and identify the bottleneck

---

## Property Class in models.py

The `Property` class is designed to represent a real estate property and extract relevant attributes from multiple types
of HTML formatted strings.

---

## Features:

1. **Initialize with Optional HTML**: The class can be initialized with an optional HTML string to begin initial data
   extraction.
2. **Dynamic Attribute Updating**: Attributes of a property object can be updated dynamically by feeding different types
   of HTML formatted strings.
3. **Comprehensive Data Extraction**: The class is equipped to extract a wide range of property attributes such as
   geocode, legal description, owner details, building details, appraisal history, and more.

## Usage:

### Initialization

You can create a new property object by initializing the `Property` class. Optionally, you can provide an initial HTML
string for data extraction:

```python
property_obj = Property(html_string=initial_html_data)
```

### Updating Attributes

After initialization, you can dynamically update the property attributes by feeding it different types of HTML formatted
strings:

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

## Main Execution - main.py

The `main.py` script is a demonstration of how to utilize the data extraction tools provided in this project.

1. **Initialization**: It sets constants for a county's name and ID, as well as a subdivision's name.
2. **County Object Creation**: It creates a `County` object and fetches its subdivisions.
3. **Subdivision Object Creation and Property Extraction**:
    - A `Subdivision` object is initialized for a specified subdivision within a county.
    - The subdivision object fetches properties associated with it.
    - A `PropertyExtractor` object extracts property details.
    - Each property's data is fetched, and a `Property` object is updated with that data.
4. **Output**: Extracted property data is written to a JSON file named `samples.json`.

To execute the script, simply run:

```bash
python main.py
```

---

## Service Endpoints - svc_endpoints.py

The `svc_endpoints.py` file provides a list of API endpoints for the Montana Cadastral API. These endpoints can be used
to fetch data from the API by passing the geocode of property and the year for which the data is required.

1. **County List**: Fetches a list of all counties.
2. **Subdivision List**: Fetches all subdivisions within a specific county.
3. **Search by Subdivision**: Retrieves properties within a particular subdivision of a county.
4. **Summary Data**: Gets summary data for a property using its geocode and year.
5. **Owner Data**: Retrieves owner information for a property.
6. **Agriculture Data**: Retrieves agriculture data for a property.
7. **Commercial Data**: Retrieves commercial data for a property.
8. **Other Building Data**: Retrieves other building data for a property.
9. **Market Land Data**: Retrieves market land data for a property.
10. **Appraisal Data**: Retrieves appraisal history for a property.
11. **Dwelling Data**: Retrieves dwelling data for a property.

---