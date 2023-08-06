import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
import json
from json import JSONDecodeError


class HTTPSConnection:
    def __init__(self, endpoint, headers):
        """
        Creating the sessions and formatting the responses for communication to the API
        :param endpoint: {str} Target API endpoint
        :param headers: {str} Authorization headers
        """
        if None not in (endpoint, headers):
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers

    def get(self, url):
        """
        Get requests sent to target API
        :param url: {str} Target endpoint
        :return: JSON payload containing the API response
        """
        try:
            session = requests.Session()
            adapter = HTTPAdapter()
            session.mount("https://", adapter)
            response = session.get(url, verify=True, headers=self.headers)
            session.close()
            response.raise_for_status()
            if response.encoding is None:
                response.encoding = "utf-8"
            elif response is not None:
                return response.json()
            else:
                return {
                    "error": "error details not found",
                    "error_code": 422,
                    "error_message": "unknown error",
                }
        except Timeout as timeout_err:
            raise TimeoutError(
                json.dumps(
                    {
                        "httpStatus": 408,
                        "message": f"Timeout error ${timeout_err.strerror}",
                    }
                )
            ) from timeout_err
        except ConnectionError as connect_err:
            raise ConnectionError(
                json.dumps(
                    {
                        "httpStatus": 503,
                        "message": f"Service error ${connect_err.strerror}",
                    }
                )
            ) from connect_err
        except JSONDecodeError as connection_err:
            raise TypeError(
                json.dumps({"httpStatus": 503, "message": "Decoding JSON has failed."})
            ) from connection_err
        except HTTPError as http_err:
            raise HTTPError(http_err)
