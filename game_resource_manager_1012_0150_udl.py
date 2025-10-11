# 代码生成时间: 2025-10-12 01:50:35
import cherrypy

"""
Game Resource Manager

This program is a simple web application using CherryPy framework to manage game resources.
It demonstrates basic CRUD operations (Create, Read, Update, Delete) for game resources.
"""

# Define a class to manage game resources
class GameResourceManager:
    def __init__(self):
        # Initialize an empty list to store game resources
        self.resources = []

    def create_resource(self, resource_name):
        """
        Create a new game resource

        Args:
        resource_name (str): The name of the game resource to be created
        """
        try:
            # Check if the resource already exists
            if any(resource['name'] == resource_name for resource in self.resources):
                raise ValueError(f"Resource '{resource_name}' already exists.")

            # Create a new resource with a unique ID
            new_resource = {'id': len(self.resources) + 1, 'name': resource_name}
            self.resources.append(new_resource)
            return new_resource
        except Exception as e:
            # Handle any exceptions and return an error message
            return {'error': str(e)}

    def get_resource(self, resource_id):
        """
        Retrieve a game resource by its ID

        Args:
        resource_id (int): The ID of the game resource to be retrieved

        Returns:
        dict: The game resource with the specified ID or an error message if not found
        """
        try:
            # Find the resource with the specified ID
            resource = next((resource for resource in self.resources if resource['id'] == resource_id), None)
            if resource is not None:
                return resource
            else:
                raise ValueError(f"Resource with ID {resource_id} not found.")
        except Exception as e:
            # Handle any exceptions and return an error message
            return {'error': str(e)}

    def update_resource(self, resource_id, new_name):
        """
        Update an existing game resource

        Args:
        resource_id (int): The ID of the game resource to be updated
        new_name (str): The new name for the game resource

        Returns:
        dict: The updated game resource or an error message if not found
        """
        try:
            # Find the resource with the specified ID
            resource = next((resource for resource in self.resources if resource['id'] == resource_id), None)
            if resource is not None:
                resource['name'] = new_name
                return resource
            else:
                raise ValueError(f"Resource with ID {resource_id} not found.")
        except Exception as e:
            # Handle any exceptions and return an error message
            return {'error': str(e)}

    def delete_resource(self, resource_id):
        """
        Remove a game resource by its ID"""
        try:
            # Find the resource with the specified ID and remove it from the list
            resource = next((resource for resource in self.resources if resource['id'] == resource_id), None)
            if resource is not None:
                self.resources = [resource for resource in self.resources if resource['id'] != resource_id]
                return {'success': f"Resource with ID {resource_id} deleted."}
            else:
                raise ValueError(f"Resource with ID {resource_id} not found.")
        except Exception as e:
            # Handle any exceptions and return an error message
            return {'error': str(e)}

# Define a class to handle HTTP requests
class GameResourceService:
    def __init__(self):
        self.manager = GameResourceManager()

    @cherrypy.expose
    def index(self):
        """
        Home page of the game resource manager
        """
        return "Welcome to the Game Resource Manager"

    @cherrypy.expose
    def create(self, resource_name):
        """
        Create a new game resource"""
        return self.manager.create_resource(resource_name)

    @cherrypy.expose
    def get(self, resource_id):
        """
        Retrieve a game resource by its ID"""
        return self.manager.get_resource(int(resource_id))

    @cherrypy.expose
    def update(self, resource_id, new_name):
        """
        Update an existing game resource"""
        return self.manager.update_resource(int(resource_id), new_name)

    @cherrypy.expose
    def delete(self, resource_id):
        """
        Remove a game resource by its ID"""
        return self.manager.delete_resource(int(resource_id))

# Configure CherryPy and start the server
if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(GameResourceService(), config=conf)