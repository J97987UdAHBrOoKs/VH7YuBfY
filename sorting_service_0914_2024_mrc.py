# 代码生成时间: 2025-09-14 20:24:41
import cherrypy
def get_args_by_name(args, name, type_func=float, default=None):
    """Helper function to extract an argument from the CherryPy request arguments."""
    try:
        return type_func(args[name])
    except (KeyError, ValueError):
        return default

class SortingService(object):
    """A CherryPy service that provides sorting capabilities."""
    @cherrypy.expose
    def index(self):
        """Landing page for the sorting service."""
        return "Welcome to the Sorting Service!"
    
    @cherrypy.expose
    def sort(self, algorithm='bubble', items=None):
        """Endpoint to sort a list of items using a specified algorithm."""
        if items is None:
            return "No items provided."
        
        items = [float(item) for item in items.split(',')]
        try:
            sorted_items = self._sort_items(algorithm, items)
            return f"Sorted items: {sorted_items}"
        except ValueError as e:
            return f"Error sorting items: {e}"
        
    def _sort_items(self, algorithm, items):
        """Sorts the given items using the specified algorithm."""
        if algorithm == 'bubble':
            return self._bubble_sort(items)
        elif algorithm == 'quick':
            return self._quick_sort(items)
        elif algorithm == 'merge':
            return self._merge_sort(items)
        else:
            raise ValueError(f"Unsupported sorting algorithm: {algorithm}")
    
    @staticmethod
    def _bubble_sort(items):
        """Implements the bubble sort algorithm."""
        n = len(items)
        for i in range(n):
            for j in range(0, n-i-1):
                if items[j] > items[j+1]:
                    items[j], items[j+1] = items[j+1], items[j]
        return items
    
    @staticmethod
    def _quick_sort(items):
        """Implements the quick sort algorithm."""
        if len(items) <= 1:
            return items
        else:
            pivot = items[0]
            less = [x for x in items[1:] if x <= pivot]
            greater = [x for x in items[1:] if x > pivot]
            return SortingService._quick_sort(less) + [pivot] + SortingService._quick_sort(greater)
    
    @staticmethod
    def _merge_sort(items):
        """Implements the merge sort algorithm."""
        if len(items) <= 1:
            return items
        else:
            mid = len(items) // 2
            left_half = SortingService._merge_sort(items[:mid])
            right_half = SortingService._merge_sort(items[mid:])
            returnSortingService._merge(left_half, right_half)
    
    @staticmethod
    def _merge(left, right):
        """Merges two sorted lists into a single sorted list."""
        sorted_list = []
        left_index, right_index = 0, 0
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                sorted_list.append(left[left_index])
                left_index += 1
            else:
                sorted_list.append(right[right_index])
                right_index += 1
        sorted_list.extend(left[left_index:])
        sorted_list.extend(right[right_index:])
        return sorted_list
    
if __name__ == '__main__':
    cherrypy.quickstart(SortingService())