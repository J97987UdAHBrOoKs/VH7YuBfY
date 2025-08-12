# 代码生成时间: 2025-08-12 16:29:10
import cherrypy
from cherrypy.lib.auth_basic import checkpasswd_hash
from cherrypy.lib.auth_digest import checkResponse
from cherrypy._cpcompat import map
from cherrypy._cptree import Application
from cherrypy.process.plugins import SimplePlugin
from cherrypy import _cptools

# A class to manage user credentials
class UserCredentials:
    def __init__(self):
        self.users = {'admin': 'admin', 'user': 'user'}

    def validate(self, username, password):
        return self.users.get(username) == password

# A tool to handle authentication
class AuthTool(SimplePlugin):
    def __init__(self, config):
        SimplePlugin.__init__(self, config)
        self.needs_auth = True
        self.credential = UserCredentials()
        self.locked = False

    def start(self):
        cherrypy.Toolmapper('before_request', self.check_auth)

    def check_auth(self, *args, **kwargs):
        if self.locked:
            return

        request = cherrypy.serving.request
        if 'auth' in request.headers:
            if 'Basic' == request.headers['auth'].split(' ')[0]:
                self.basic_auth(request)
            elif 'Digest' == request.headers['auth'].split(' ')[0]:
                self.digest_auth(request)
            else:
                raise cherrypy.HTTPError(400, 'Bad Request')
        else:
            self.needs_auth = True

    def basic_auth(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            raise cherrypy.HTTPError(401, 'Authentication required')
        auth_type, auth_info = auth.split(' ', 1)
        username, password = auth_info.decode('base64').split(':', 1)
        if not self.credential.validate(username, password):
            raise cherrypy.HTTPError(403, 'Forbidden')
        self.needs_auth = False

    def digest_auth(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            raise cherrypy.HTTPError(401, 'Authentication required')
        auth_type, auth_info = auth.split(' ', 1)
        auth_info = auth_info.decode('base64').split(',', 1)
        username, realm, nonce, uri, response = map(
            lambda x: x.strip(), map(str.strip, auth_info)
        )
        if not self.credential.validate(username, realm):
            raise cherrypy.HTTPError(403, 'Forbidden')
        if not checkResponse(username, realm, nonce, uri, response):
            raise cherrypy.HTTPError(403, 'Forbidden')
        self.needs_auth = False

# A decorator to check if the user is authenticated
def check_auth(func):
    def wrapper(*args, **kwargs):
        if AuthTool.needs_auth:
            raise cherrypy.HTTPError(401, 'Authentication required')
        return func(*args, **kwargs)
    return wrapper

# A simple test page
class Page:
    @cherrypy.expose
    @check_auth
    def index(self):
        return 'Welcome to the protected page!'

# Initialize the CherryPy application
if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
        },
        '/': {
            'tools.auth.on': True,
            'tools.auth.credential': UserCredentials(),
        },
    }

    cherrypy.quickstart(Page(), '/', config=conf)
