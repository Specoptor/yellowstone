from bs4 import BeautifulSoup


def extract_key_value_pairs(soup_objects: list[BeautifulSoup]) -> dict[str, str]:
    """
    Extracts key-value pairs from a list of BeautifulSoup objects.
    :param soup_objects:
    :return:
    """
    data = {}
    for obj in soup_objects:
        if len(obj.contents) == 2 and \
                obj.contents[0].attrs['class'] == ['key'] and \
                obj.contents[1].attrs['class'] == ['value']:
            key = obj.find('span', class_='key').text.strip(':')
            value = obj.find('span', class_='value').text
            data[key] = value
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