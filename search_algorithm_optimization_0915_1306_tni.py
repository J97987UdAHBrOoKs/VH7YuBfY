# 代码生成时间: 2025-09-15 13:06:05
import cherrypy
def linear_search(arr, target):
    """Perform a linear search on the array for the target value.
    Args:
        arr (list): The array of elements to search within.
        target (any): The value to search for.
    Returns:
        int: The index of the target value if found, otherwise -1."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    """Perform a binary search on the sorted array for the target value.
    Args:
        arr (list): The sorted array of elements to search within.
        target (any): The value to search for.
    Returns:
        int: The index of the target value if found, otherwise -1."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

class SearchApp:
    """A CherryPy application for searching algorithms."""
    @cherrypy.expose
    def index(self):
        """Return the index page for the search application."""
        return "Welcome to the Search Algorithm Optimization Application!"

    @cherrypy.expose
    def linear_search(self, arr, target):
        """Handle a request to perform a linear search.
        Args:
            arr (list): A JSON-encoded list of elements to search within.
            target (any): The value to search for.
        Returns:
            str: A JSON-encoded response indicating the result of the search."""
        try:
            arr = json.loads(arr)
            target = json.loads(target)
            index = linear_search(arr, target)
            return json.dumps({'index': index})
        except Exception as e:
            return json.dumps({'error': str(e)})

    @cherrypy.expose
    def binary_search(self, arr, target):
        """Handle a request to perform a binary search.
        Args:
            arr (list): A JSON-encoded list of elements to search within.
            target (any): The value to search for.
        Returns:
            str: A JSON-encoded response indicating the result of the search."""
        try:
            arr = json.loads(arr)
            target = json.loads(target)
            index = binary_search(arr, target)
            return json.dumps({'index': index})
        except Exception as e:
            return json.dumps({'error': str(e)})

if __name__ == '__main__':
    # Configure the CherryPy server to run on port 8080
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(SearchApp())