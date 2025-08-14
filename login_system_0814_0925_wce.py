# 代码生成时间: 2025-08-14 09:25:31
import cherrypy
import hashlib
import json

# 模拟的用户数据库
USER_DB = {
    "user1": {"password": "5ebe2293f56e9f1a3f9a1b3a7030bf4f"},  # 密码是'password123'的MD5哈希值
}
a
def check_password(stored_password, provided_password):
    """
    Check if the provided password matches the stored password.
    """
    # 将用户提供的密码进行MD5哈希
    return hashlib.md5(provided_password.encode()).hexdigest() == stored_password

a
def login(user, password):
    """
    User login verification.
    """
    if user in USER_DB:
        if check_password(USER_DB[user]['password'], password):
            return json.dumps({'status': 'success', 'message': 'Login successful'})
        else:
            raise cherrypy.HTTPError(401, 'Incorrect password')
    else:
        raise cherrypy.HTTPError(404, 'User not found')
a
def error_page(status, message, traceback, version):
    """
    Error page handler.
    """
    return json.dumps({'status': 'error', 'message': message})
a
def main():
    """
    Main function to start the CherryPy server.
    """
    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
        },
        '/login': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]},
        '/error_page': error_page
    }
    cherrypy.quickstart(LoginApp(), '/', config=conf)
a
c
def login_handler(self, user, password):
    """
    Login handler.
    """
    return login(user, password)
a
c
c
def logout_handler(self):
    """
    Logout handler.
    """
    return json.dumps({'status': 'success', 'message': 'Logged out successfully'})
a
c
cclass LoginApp(object):
    """
    Login application with login and logout endpoints.
    """
    @cherrypy.expose
    def login(self, user, password):
        """
        Login endpoint.
        """
        return login_handler(user, password)
    """
    @cherrypy.expose
    def logout(self):
        """
        Logout endpoint.
        """
        return logout_handler()

a
aif __name__ == '__main__':
    main()