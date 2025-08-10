# 代码生成时间: 2025-08-10 12:04:05
import cherrypy
from jinja2 import Template
import json
import numpy as np
import pandas as pd

# 定义配置和路由
class InteractiveChartGenerator:
    def __init__(self):
        self.data = pd.DataFrame()

    @cherrypy.expose
    def index(self):
        # 渲染图表生成器的模板页面
        template_path = "templates/index.html"
        with open(template_path, 'r') as file:
            template = Template(file.read())
        return template.render()

    @cherrypy.expose
    def generate_chart(self, data):
        # 解析输入的数据
        try:
            data_json = json.loads(data)
            data_df = pd.DataFrame(data_json)
        except json.JSONDecodeError as e:
            return "Invalid JSON data provided."

        # 检查数据有效性
        if not data_df.empty and data_df.shape[1] == 2:
            # 生成图表的HTML代码
            chart_html = self.generate_chart_html(data_df)
            return chart_html
        else:
            return "Invalid data format. Data should have exactly two columns."

    def generate_chart_html(self, data_df):
        # 这里假设使用一个简单的JavaScript图表库，如Chart.js
        # 生成图表的HTML代码
        chart_html = "<canvas id='myChart'></canvas>"
        chart_script = "<script>"
        chart_script += "var ctx = document.getElementById('myChart').getContext('2d');"
        chart_script += "var chart = new Chart(ctx, {{"
        chart_script += "type: 'line',"
        chart_script += "data: {{"
        chart_script += "labels: {},".format(json.dumps(data_df.columns[0]))
        chart_script += "datasets: [{"
        chart_script += "label: 'Data',"
        chart_script += "data: {},".format(json.dumps(data_df.values.tolist()))
        chart_script += "backgroundColor: 'rgba(255, 99, 132, 0.2)',"
        chart_script += "borderColor: 'rgba(255, 99, 132, 1)',"
        chart_script += "borderWidth: 1"
        chart_script += "}]"
        chart_script += "}},"
        chart_script += "options: {{"
        chart_script += "scales: {{"
        chart_script += "y: {{ beginAtZero: true }}"
        chart_script += "}}"
        chart_script += "}}"
        chart_script += "}});"
        chart_script += "</script>"
        return chart_html + chart_script

# 配置CherryPy服务器
config = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static',
    },
}

if __name__ == '__main__':
    cherrypy.quickstart(InteractiveChartGenerator(), '/', config)