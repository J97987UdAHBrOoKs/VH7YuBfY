# 代码生成时间: 2025-08-19 02:37:04
import cherrypy

# 排序算法实现
class SortingApp:
    def __init__(self):
        self.methods = {'sort': ['POST']}  # 限制方法

    # 快速排序算法实现
    @staticmethod
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return SortingApp.quick_sort(left) + middle + SortingApp.quick_sort(right)

    # 排序接口
    @cherrypy.expose
    def sort(self, numbers):
        """
        对输入的数字进行排序
        
        参数:
        numbers -- 一个数字列表，用逗号分隔
        
        返回:
        排序后的数字列表
        """
        try:
            # 将输入字符串转换为整数列表
            numbers = list(map(int, numbers.split(',')))
            # 使用快速排序算法进行排序
            sorted_numbers = SortingApp.quick_sort(numbers)
            return ",".join(map(str, sorted_numbers))
        except ValueError:
            # 处理非数字输入
            return "Error: 输入包含非数字字符"
        except Exception as e:
            # 处理其他异常
            return f"Error: {str(e)}"

# CherryPy配置
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080})
    cherrypy.quickstart(SortingApp())