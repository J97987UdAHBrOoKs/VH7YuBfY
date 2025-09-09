# 代码生成时间: 2025-09-09 21:25:36
import cherrypy
import unittest

# 自动化测试套件
class TestSuite(unittest.TestCase):
    """
    自动化测试套件，用于测试CherryPy应用程序
    """

    def test_index(self):
        """测试首页是否正常返回"""
        cherrypy.tree.mount(self.app, '/', {'/': {'tools.sessions.on': True}})
        response = self.app.get('/')
        self.assertEqual(response.status, 200)
        self.assertIn('Hello, World!', response.body)

    def test_not_found(self):
        """测试不存在的页面是否返回404"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status, 404)

# CherryPy配置
class HelloWorld(object):
    """简单的Hello World应用程序"""
    @cherrypy.expose
    def index(self):
        return 'Hello, World!'

    @cherrypy.expose
    def not_found(self):
        raise cherrypy.HTTPError(404)

# 运行测试
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSuite())
    runner = unittest.TextTestRunner()
    runner.run(suite)
