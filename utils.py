import re
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
