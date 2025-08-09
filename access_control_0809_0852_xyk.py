# 代码生成时间: 2025-08-09 08:52:29
import cherrypy
from cherrypy.lib import auth_digest

# 访问权限控制装饰器
class AccessControl:
    def __init__(self, realm, users):
        self.realm = realm
        self.users = users

    def check_credentials(self, username, password):
        """检查用户名和密码是否正确"""
        return username in self.users and self.users[username] == password

    def __call__(self, *args, **kwargs):
        """装饰器逻辑，用于检查用户是否具有访问权限"""
        auth = cherrypy.request.headers.get('Authorization')
        if auth:
            token, credentials = authDigest.parse(auth)
            if token == 'Digest':
                username, password = auth_digest.check_response(
                    credentials, cherrypy.request.method, cherrypy.request.path_info
                )
                if self.check_credentials(username, password):
                    return kwargs['func'](*args, **kwargs)
        raise cherrypy.HTTPError(401, 'Access denied')

# 用户字典
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# 实例化访问控制对象
access_control = AccessControl('My Realm', users)

# 简单的HTTP服务
class HttpService:
    @cherrypy.expose
    @access_control
    def index(self):
        """主页接口"""
        return 'Welcome to the secure page!'

# 启动CherryPy服务
if __name__ == '__main__':
    cherrypy.quickstart(HttpService())
