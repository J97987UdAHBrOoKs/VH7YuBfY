# 代码生成时间: 2025-09-15 00:09:10
import os
from cherrypy import CherryPy, tools
from PIL import Image
import sys

# 图片尺寸批量调整器
class ImageResizer:
    def __init__(self, width, height):
        """初始化函数，设置目标尺寸"""
        self.width = width
        self.height = height

    def resize_image(self, input_path, output_path):
        """调整图片尺寸并保存到指定路径"""
        try:
            with Image.open(input_path) as img:
                img = img.resize((self.width, self.height), Image.ANTIALIAS)
                img.save(output_path)
                return True
        except IOError as e:
            print(f"Error resizing image {input_path}: {e}")
            return False

    def process_directory(self, directory):
        """处理目录中的所有图片"""
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                input_path = os.path.join(directory, filename)
                output_path = os.path.join(directory, 'resized_' + filename)
                self.resize_image(input_path, output_path)

# CherryPy 配置
class Root:
    @cherrypy.expose
    def index(self):
        "