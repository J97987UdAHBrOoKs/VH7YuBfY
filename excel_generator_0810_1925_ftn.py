# 代码生成时间: 2025-08-10 19:25:30
import cherrypy
import xlsxwriter
from io import BytesIO
from cherrypy.lib.static import serve_file

# 定义一个类来处理Excel文件生成
class ExcelGenerator:
    def generate_excel(self, data):
        # 确保传入的数据是一个列表
        if not isinstance(data, list):
            raise ValueError('Data must be a list of data to write into the Excel file.')

        # 创建一个BytesIO流用于存储Excel文件数据
        output = BytesIO()
        try:
            # 创建一个Excel文件
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            # 写入数据到Excel文件
            for row_num, row_data in enumerate(data):
                for col_num, value in enumerate(row_data):
                    worksheet.write(row_num, col_num, value)
            # 关闭Excel文件
            workbook.close()
        except Exception as e:
            raise Exception(f'Failed to generate Excel file: {e}')
        finally:
            # 将BytesIO流的位置移动到开头，以便可以从开始读取
            output.seek(0)
        return output

    # CherryPy暴露的端点，用于下载生成的Excel文件
    @cherrypy.expose
    def download(self, data=None):
        if data is None:
            raise cherrypy.HTTPError(400, 'Missing data parameter.')
        try:
            # 生成Excel文件
            excel_file = self.generate_excel(data)
        except ValueError as ve:
            raise cherrypy.HTTPError(400, str(ve))
        except Exception as e:
            raise cherrypy.HTTPError(500, str(e))

        # 设置响应头，告诉浏览器这是一个文件下载
        cherrypy.response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename=generated_excel.xlsx'
        return serve_file(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# 设置CherryPy服务器配置
config = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    },
    '/': {
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
    },
}

# 启动CherryPy服务器
if __name__ == '__main__':
    cherrypy.quickstart(ExcelGenerator(), config=config)
