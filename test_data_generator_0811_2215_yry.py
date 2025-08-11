# 代码生成时间: 2025-08-11 22:15:04
import cherrypy
import random
import string

# 测试数据生成器类
class TestDataGenerator:
    """
    生成随机测试数据
    """
    def generate_random_string(self, length=10):
        """
        生成指定长度的随机字符串
        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_number(self, min_value=1, max_value=100):
        """
        生成指定范围内的随机整数
        """
        return random.randint(min_value, max_value)

    def generate_random_datetime(self):
        """
        生成当前时间前后10年内的随机日期时间
        "