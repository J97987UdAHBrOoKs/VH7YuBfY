# 代码生成时间: 2025-08-01 23:17:29
import cherrypy
def add(a, b):
    """Add two numbers."""
    try:
        return a + b
    except TypeError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def subtract(a, b):
    """Subtract two numbers."""
    try:
        return a - b
    except TypeError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def multiply(a, b):
    """Multiply two numbers."""
    try:
        return a * b
    except TypeError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def divide(a, b):
    """Divide two numbers."""
    try:
        if b == 0: raise ZeroDivisionError('Cannot divide by zero')
        return a / b
    except ZeroDivisionError as e:
        raise cherrypy.HTTPError(400, 'Invalid operation: ' + str(e))
    except TypeError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def power(a, b):
    """Raise a number to the power of another."""
    try:
        return a ** b
    except TypeError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def sqrt(a):
    """Calculate the square root of a number."""
    try:
        import math
        return math.sqrt(a)
    except ValueError as e:
        raise cherrypy.HTTPError(400, 'Invalid input: ' + str(e))

def setup_routes():
    """Setup CherryPy routes for the calculator."""
    cherrypy.tree.mount(add, '/math/add', {'a':0, 'b':0})
    cherrypy.tree.mount(subtract, '/math/subtract', {'a':0, 'b':0})
    cherrypy.tree.mount(multiply, '/math/multiply', {'a':0, 'b':0})
    cherrypy.tree.mount(divide, '/math/divide', {'a':0, 'b':0})
    cherrypy.tree.mount(power, '/math/power', {'a':0, 'b':0})
    cherrypy.tree.mount(sqrt, '/math/sqrt', {'a':0})
def start_server():
    """Start the CherryPy server."""
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    setup_routes()
    cherrypy.quickstart()
def main():
    """Main entry point of the program."""
    try:
        start_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:\
        print(f'An error occurred: {str(e)}')
if __name__ == '__main__': main()