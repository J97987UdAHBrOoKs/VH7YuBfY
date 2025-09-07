# 代码生成时间: 2025-09-07 13:11:34
import cherrypy
# 改进用户体验

class SortingService:
    """
    A CherryPy service that provides sorting algorithms.
    """

    def __init__(self):
        """Initialize the sorting service."""
        pass

    @cherrypy.expose
    def bubble_sort(self, array):
        """
        Perform bubble sort on the given array and return the sorted array.

        :param array: A list of integers to be sorted.
# 扩展功能模块
        :return: A sorted list of integers.
        :raises ValueError: If the input is not a list or contains non-integer values.
# 改进用户体验
        """
        if not isinstance(array, list) or not all(isinstance(x, int) for x in array):
            raise ValueError("Input must be a list of integers.")

        sorted_array = array.copy()
        n = len(sorted_array)
        for i in range(n):
            for j in range(0, n-i-1):
                if sorted_array[j] > sorted_array[j+1]:
                    sorted_array[j], sorted_array[j+1] = sorted_array[j+1], sorted_array[j]
        return sorted_array

    @cherrypy.expose
# 改进用户体验
    def quick_sort(self, array):
        """
        Perform quick sort on the given array and return the sorted array.

        :param array: A list of integers to be sorted.
        :return: A sorted list of integers.
        :raises ValueError: If the input is not a list or contains non-integer values.
        """
        if not isinstance(array, list) or not all(isinstance(x, int) for x in array):
# 扩展功能模块
            raise ValueError("Input must be a list of integers.")
# 优化算法效率

        def _quick_sort_helper(arr):
# 添加错误处理
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
# NOTE: 重要实现细节
            right = [x for x in arr if x > pivot]
            return _quick_sort_helper(left) + middle + _quick_sort_helper(right)

        return _quick_sort_helper(array)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
        },
    }
# NOTE: 重要实现细节
    cherrypy.quickstart(SortingService(), '/', config=conf)