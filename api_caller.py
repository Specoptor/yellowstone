import requests
from requests.exceptions import Timeout, ConnectionError
from decorators import timer

class ApiCaller:
    def __init__(self, timeout: int = 250) -> None:
        """
        Initializes an ApiCaller object.

        :param timeout: Time in seconds to wait for the server response. Defaults to 10 seconds.
        """
        self.session = requests.Session()
        self.timeout = timeout

    @timer
    def get(self, url: str) -> requests.Response | None:
        """
        Sends a GET request to the given URL and returns the response object.

        :param url: The URL to send the request to.
        :param params: Additional parameters to send with the request.
        :return: The response object.
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response
        except Timeout:
            print(f"Request to {url} timed out.")
            return None
        except ConnectionError:
            print(f"Connection error occurred while connecting to {url}.")
            return None
        except requests.RequestException as e:
            print(f"An error occurred while requesting {url}. Error: {e}")
            return None
