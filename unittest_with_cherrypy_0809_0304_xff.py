# 代码生成时间: 2025-08-09 03:04:01
import cherrypy
import unittest
from cherrypy.test import helper

# The CherryPy Application
class MyApp:
    @cherrypy.expose
    def index(self):
        return 'Hello, World!'

    @cherrypy.expose
    def add(self, a, b):
        try:
            return int(a) + int(b)
        except ValueError:
            return 'Invalid input'

# Unit Test for the CherryPy Application
class MyAppTest(unittest.TestCase, helper.CPWebCase):
    def test_index(self):
        self.getPage('/')
        self.assertStatus('200 OK')
        self.assertBody('Hello, World!')

    def test_add(self):
        self.getPage('/add?a=5&b=3')
        self.assertStatus('200 OK')
        self.assertBody('8')

    def test_add_invalid_input(self):
        self.getPage('/add?a=abc&b=3')
        self.assertStatus('200 OK')
        self.assertBody('Invalid input')

if __name__ == '__main__':
    # Start the CherryPy server
    cherrypy.quickstart(MyApp())
    # Run the unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
