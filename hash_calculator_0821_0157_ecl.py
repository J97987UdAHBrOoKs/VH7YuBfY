# 代码生成时间: 2025-08-21 01:57:53
import cherrypy
def calculate_hash(data, method='sha256'):    """
    计算给定数据的哈希值。
    
    参数:
    - data (str): 要计算哈希值的数据。
    - method (str): 哈希算法方法，默认为 'sha256'。支持的算法包括 'md5', 'sha1', 'sha256', 'sha512'。
    
    返回:
    - str: 计算得到的哈希值。
    """    
    import hashlib
    try:
        hash_function = getattr(hashlib, method)()
        hash_function.update(data.encode('utf-8'))
        return hash_function.hexdigest()
    except AttributeError:
        raise ValueError(f'不支持的哈希算法：{method}')    
    
class HashCalculator:    """
    哈希值计算工具。
    """    
    @cherrypy.expose
    def index(self):
        """
        根目录页面，提供哈希计算的表单。
        """
        return """            
        <html>
        <body>
        <h1>哈希值计算工具</h1>
        <form action="/hash_calculate" method="post">
        数据：<input type="text" name="data" value="" />
        选择哈希算法：<select name="method">
        <option value="md5">MD5</option>
        <option value="sha1">SHA1</option>
        <option value="sha256" selected>SHA256</option>
        <option value="sha512">SHA512</option>
        </select>
        <input type="submit" value="计算哈希值" />
        </form>
        </body>
        </html>
        """            
    @cherrypy.expose
    def calculate(self, data='', method='sha256'):
        """
        计算并返回哈希值。
        
        参数:
        - data (str): 要计算哈希值的数据。
        - method (str): 哈希算法方法，默认为 'sha256'。
        
        返回:
        - str: 计算得到的哈希值。
        """        
        if not data:
            raise cherrypy.HTTPError(400, '缺少必要的参数：data')
        try:
            return calculate_hash(data, method)
        except ValueError as e:
            raise cherrypy.HTTPError(400, str(e))
    
if __name__ == '__main__':    
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',    # 监听所有地址
            'server.socket_port': 8080,        # 监听8080端口
        }
    }
    cherrypy.quickstart(HashCalculator(), '/', config=conf)