# list of all counties
county_list = "https://svc.mt.gov/msl/legacycadastralapi/search/getcountylist"

# list of all subdivisions in a given county
# Example uses county id 03
subdivision_list = "https://svc.mt.gov/msl/legacycadastralapi/search/getsubdivisionlist?countyid=03"

# list of properties in a given subdivision of a given county
# Example uses county id 03 and subdivision 23rd street subd (17)
search_by_subdivision = "https://svc.mt.gov/msl/legacycadastralapi/search/searchbysubdivision?subdivision=23rd%20street%20subd%20(17)&countyid=03"

# get summary data
# Example uses geocode 03103332110110000 and year 2023
summary_data = "https://svc.mt.gov/msl/legacycadastralapi/summary/getsummarydata?geocode=03103332110110000&year=2023"

# get owner data
# Example uses geocode 03103332110110000 and year 2023
owner_data = "https://svc.mt.gov/msl/legacycadastralapi/owner/getownerdata?geocode=03103332110110000&year=2023"

# get appraisal data
# Example uses geocode 03103332110110000 and year 2023
appraisal_data = "https://svc.mt.gov/msl/legacycadastralapi/appraisal/getappraisaldata?geocode=03103332110110000&year=2023"

# get market land data
# Example uses geocode 03103332110110000 and year 2023
market_land_data = "https://svc.mt.gov/msl/legacycadastralapi/marketland/getmarketlanddata?geocode=03103332110110000&year=2023"

# get dwelling data
# Example uses geocode 03103332110110000 and year 2023
dwelling_data = "https://svc.mt.gov/msl/legacycadastralapi/dwelling/getdwellingdata?geocode=03103332110110000&year=2023"

# get other building data
# Example uses geocode 03103332110110000 and year 2023
other_building_data = "https://svc.mt.gov/msl/legacycadastralapi/otherbuilding/getotherbuildingdata?geocode=03103332110110000&year=2023"

# get commercial data
# Example uses geocode 03103332110110000 and year 2023
commercial_data = "https://svc.mt.gov/msl/legacycadastralapi/commercial/getcommercialdata?geocode=03103332110110000&year=2023"

# get agricultural data
# Example uses geocode 03103332110110000 and year 2023
agricultural_data = "https://svc.mt.gov/msl/legacycadastralapi/agforest/getagforestdata?geocode=03103332110110000&year=2023"
