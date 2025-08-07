# 代码生成时间: 2025-08-07 11:36:54
import cherrypy
import random
import string

"""
Test Data Generator Service
This service generates random test data using CherryPy framework.
It's designed to be easy to understand, maintain and extend.
"""

class TestDataGenerator:
    """
    This class provides methods to generate random test data.
    """
    @cherrypy.expose
    def generate_random_string(self, length=10):
        """
        Generate a random string of a given length.
        :param length: The length of the string to generate.
        :return: A random string of the specified length.
        """
        try:
            if length <= 0:
                raise ValueError("Length must be greater than 0.")
            # Generate a random string of the specified length
            return ''.join(random.choice(string.ascii_letters) for _ in range(length))
        except ValueError as e:
            # Handle errors and return a meaningful error message
            return str(e)

    @cherrypy.expose
    def generate_random_number(self, min_value=1, max_value=100):
        """
        Generate a random number within a given range.
        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :return: A random number within the specified range.
        """
        try:
            if min_value >= max_value:
                raise ValueError("Minimum value must be less than maximum value.")
            # Generate a random number within the specified range
            return random.randint(min_value, max_value)
        except ValueError as e:
            # Handle errors and return a meaningful error message
            return str(e)

    @cherrypy.expose
    def generate_random_email(self):
        """
        Generate a random email address.
        :return: A random email address.
        """
        try:
            # Generate a random email address
            return '%s@%s.com' % (
                ''.join(random.choice(string.ascii_lowercase) for _ in range(10)),
                ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            )
        except Exception as e:
            # Handle errors and return a meaningful error message
            return str(e)

if __name__ == '__main__':
    # Set up the CherryPy configuration
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080})
    # Mount the Test Data Generator service
    cherrypy.quickstart(TestDataGenerator())