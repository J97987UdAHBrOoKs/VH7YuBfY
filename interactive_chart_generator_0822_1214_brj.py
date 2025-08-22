# 代码生成时间: 2025-08-22 12:14:19
import cherrypy
def index():
    # 返回一个HTML页面，带有表单让用户输入数据
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Interactive Chart Generator</title>
    </head>
    <body>
        <h1>Interactive Chart Generator</h1>
        <form action="generate_chart" method="post">
            <label for="data">Enter data (comma-separated values):</label><br>
            <textarea id="data" name="data" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Generate Chart">
        </form>
    </body>
    </html>
    """

def generate_chart(data=None):
    # 处理表单提交的数据，生成图表
    if data is None or data.strip() == "":
        return "Please enter data."
    try:
        # 假设我们将数据转换为一个列表，并使用matplotlib生成图表
        import matplotlib.pyplot as plt
        import io
        
        # 将输入的数据转换为浮点数列表
        data_list = [float(value) for value in data.split(",")]
        
        # 创建一个图表
        plt.figure()
        plt.plot(data_list)
        plt.title("Interactive Chart")
        plt.xlabel("Index")
        plt.ylabel("Value")
        
        # 保存图表到一个内存的字节流中
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # 设置响应头，返回图表
        cherrypy.response.headers['Content-Type'] = 'image/png'
        return buf.read()
    except ValueError:
        return "Invalid data. Please enter comma-separated numeric values."
if __name__ == '__main__':
    # 设置CherryPy服务器配置
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                           'server.socket_port': 8080})
    # 定义CherryPy路由
    cherrypy.quickstart({'/': index, '/generate_chart': generate_chart})