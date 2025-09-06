# 代码生成时间: 2025-09-07 01:59:04
import cherrypy
from urllib.parse import urlparse
import requests

"""
URL Validator service using CherryPy framework.
This service validates the validity of a given URL.
"""

class URLValidator:
    def validate_url(self, url):
        """
        Validate the URL by checking if it is reachable and has a valid scheme.
        Args:
            url (str): The URL to be validated.
        Returns:
            dict: A dictionary with the result of the validation.
        """
        try:
            # Parse the URL to check if it has a valid scheme
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return {"valid": False, "reason": "Invalid URL scheme or network location."}
            
            # Try to reach the URL to check its validity
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return {"valid": True, "message": "URL is valid and reachable."}
            else:
                return {"valid": False, "message": f"URL is not reachable. HTTP status code: {response.status_code}."}
        except requests.RequestException as e:
            return {"valid": False, "message": str(e)}
        except Exception as e:
            return {"valid": False, "message": f"An unexpected error occurred: {str(e)}."}


def main():
    """
    Main function to start the CherryPy server.
    """
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        }
    }
    cherrypy.quickstart(URLValidator(), '/', config=conf)

if __name__ == '__main__':
    main()

# CherryPy exposes the validate_url method at the /validate endpoint.
# For example, to validate a URL, you can access: http://localhost:8080/validate?url=<URL_TO_VALIDATE>
