# 代码生成时间: 2025-08-15 06:27:27
import cherrypy
# 优化算法效率

# 排序算法模块
class SortingService:
    def bubble_sort(self, arr):
# 扩展功能模块
        """ 冒泡排序算法 """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def insertion_sort(self, arr):
        "