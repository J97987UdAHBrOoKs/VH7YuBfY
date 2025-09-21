# 代码生成时间: 2025-09-22 06:02:47
import cherrypy
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from cherrypy.lib.static import serve_file

# 配置CherryPy
class ExcelGenerator:
    def __init__(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    def generate_excel(self, data):
        "