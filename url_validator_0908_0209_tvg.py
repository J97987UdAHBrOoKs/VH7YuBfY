# 代码生成时间: 2025-09-08 02:09:58
import cherrypy
import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException

"""
A CherryPy application for validating the validity of URLs.
It checks whether a given URL is reachable and properly formatted.
"""

class URLValidator:
    """
    A class responsible for validating URLs.
    """
    def check_url(self, url):
        """
        Checks if the URL is valid and reachable.
        :param url: The URL to be validated.
        :return: A boolean indicating the validity of the URL.
        """
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        except RequestException as e:
            # Log the exception (e.g., using logging module)
            # For simplicity, just print the error message
            print(f"Error occurred while checking URL: {e}")
            return False

    @cherrypy.expose
    def validate(self, url):
        """
        A CherryPy endpoint that validates a URL.
        :param url: The URL to be validated, passed as a query parameter.
        :return: A JSON response indicating the validity of the URL.
        """
        is_valid = self.check_url(url)
        return {
            "url": url,
            "is_valid": is_valid
        }

if __name__ == '__main__':
    config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.quickstart(URLValidator(), '/', config)