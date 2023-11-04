import re
import pandas as pd
from bs4 import Tag


def extract_key_value_pairs(table: Tag) -> dict:
    """
    Extract key-value pairs from the provided table Tag.

    :param table: The table BeautifulSoup Tag.
    :return: A dictionary with the extracted key-value pairs.
    """
    data = {}
    rows = table.find_all('tr')
    for row in rows:
        key_elements = row.find_all(class_='key')
        value_elements = row.find_all(class_='value')

        for key_element, value_element in zip(key_elements, value_elements):
            key_text = key_element.get_text().strip()
            value_text = value_element.get_text().strip()
            data[key_text] = value_text

    return data


def decode_html(encoded_string: str) -> str:
    """
    decode the raw html string received from http response to a clean html string.
    :param encoded_string: raw html string
    :return: clean html string
    """
    # Decoding unicode escape sequences
    decoded_string = bytes(encoded_string, "utf-8").decode("unicode_escape")

    # Replacing control characters
    clean_html = decoded_string.replace("\r", "").replace("\n", "").replace("\t", "")

    return clean_html


def is_empty_response(html_string: str) -> bool:
    """
    Check if the HTML string indicates an empty response.

    :param html_string: The input HTML string.
    :return: True if it's an empty response, False otherwise.
    """
    return bool(re.search(r"No .+ info exists for this parcel", html_string))


def flatten_json_to_df(data):
    """Flatten the nested JSON structure and return a DataFrame."""
    # Using pandas to flatten the JSON
    df_initial = pd.json_normalize(data.get('initial', {})).add_suffix('_initial')
    df_summary = pd.json_normalize(data.get('summary', {})).add_suffix('_summary')
    df_owner = pd.json_normalize(data.get('owner', {})).add_suffix('_owner')
    df_dwelling = pd.json_normalize(data.get('dwelling', {})).add_suffix('_dwelling')
    df_other_building = pd.json_normalize(data.get('other_building', [])).add_suffix('_other_building')
    df_commercial = pd.json_normalize(data.get('commercial', {})).add_suffix('_commercial')
    df_market_land = pd.json_normalize(data.get('market_land', {})).add_suffix('_market_land')

    # Handle appraisal data that may contain multiple years
    df_appraisal = pd.json_normalize(data.get('appraisal', []))
    df_appraisal = df_appraisal.sort_values(by='Tax Year', ascending=False)
    # Make sure we only have up to 3 years of data, and create YOY columns
    if len(df_appraisal) > 3:
        df_appraisal = df_appraisal.iloc[:3]
    yoy_columns = ['Land Value', 'Building Value', 'Total Value']
    for i in range(len(df_appraisal) - 1):
        for col in yoy_columns:
            df_appraisal[f'YOY {col} ({df_appraisal.iloc[i + 1]["Tax Year"]}-{df_appraisal.iloc[i]["Tax Year"]})'] = \
                df_appraisal.iloc[i][col] - df_appraisal.iloc[i + 1][col]
    # Drop the original columns as we now have YOY columns
    df_appraisal.drop(yoy_columns, axis=1, inplace=True)

    # Concatenating all the dataframes
    dfs = [df_initial, df_summary, df_owner, df_dwelling, df_other_building, df_commercial, df_market_land]
    df_combined = pd.concat(dfs, axis=1).join(df_appraisal)

    # Convert the DataFrame into a list of dictionaries
    records = df_combined.to_dict('records')
    return records[0]
