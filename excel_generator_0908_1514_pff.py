# 代码生成时间: 2025-09-08 15:14:28
import cherrypy
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException

# 定义Excel生成器类
def generate_excel(data):
    """根据提供的数据生成Excel文件"""
    wb = Workbook()
    ws = wb.active
    for row_index, row in enumerate(data, 1):
        for col_index, value in enumerate(row, 1):
            ws.cell(row=row_index, column=col_index).value = value
    return wb


# 定义CherryPy暴露的接口
def expose_excel(data):
    """生成并返回Excel文件"""
    try:
        wb = generate_excel(data)
        wb.save('generated_excel.xlsx')
        return 'Excel file generated successfully.'
    except InvalidFileException as e:
        return f'Error: {e}'
    except Exception as e:
        return f'An unexpected error occurred: {e}'


# 设置CherryPy服务器配置
class ExcelApp:
    """CherryPy应用类"""
    @cherrypy.expose
    def index(self, **params):
        """首页"""
        return 'Welcome to the Excel Generator service.'

    @cherrypy.expose
    def generate(self, **params):
        """生成Excel文件"""
        # 假设params是一个字典，包含生成Excel所需的所有数据
        # 例如：params={'data': [[1, 2], [3, 4]]}
        if 'data' not in params or not params['data']:
            return 'No data provided for Excel generation.'

        data = params['data']
        return expose_excel(data)


if __name__ == '__main__':
    # 启动CherryPy服务器
    cherrypy.quickstart(ExcelApp())
