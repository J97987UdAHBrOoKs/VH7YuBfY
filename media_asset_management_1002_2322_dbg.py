# 代码生成时间: 2025-10-02 23:22:02
import cherrypy
import os
import json
from cherrypy.lib.static import serve_file

# 定义媒体资产管理应用的配置
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'tools.sessions.on': True,
        'tools.sessions.timeout': 60,  # 1 minute
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), 'static'),
    },
}

class MediaAssetManagement:
    """
    媒体资产管理CherryPy服务类。
    """
    @cherrypy.expose
    def index(self):
        """
        首页视图，返回媒体资产列表。
        """
        try:
            asset_list = self.get_asset_list()
            return json.dumps(asset_list)
        except Exception as e:
            return json.dumps({'error': str(e)})

    def get_asset_list(self):
        """
        获取媒体资产列表。
        """
        # 假设媒体资产存储在'static/assets'目录下
        assets_dir = os.path.join(os.path.dirname(__file__), 'static', 'assets')
        asset_list = []
        for filename in os.listdir(assets_dir):
            asset_list.append({'filename': filename, 'size': os.path.getsize(os.path.join(assets_dir, filename))})
        return asset_list

    @cherrypy.expose
    def upload(self, file=None):
        """
        上传媒体资产。
        """
        if file is None or file.file is None:
            return json.dumps({'error': 'No file uploaded'})
        try:
            file_path = self.save_file(file.file)
            return json.dumps({'success': 'File uploaded successfully', 'path': file_path})
        except Exception as e:
            return json.dumps({'error': str(e)})

    def save_file(self, file_obj):
        """
        保存上传的文件。
        """
        assets_dir = os.path.join(os.path.dirname(__file__), 'static', 'assets')
        filename = file_obj.filename
        save_path = os.path.join(assets_dir, filename)
        with open(save_path, 'wb') as f:
            f.write(file_obj.file.read())
        return save_path


def start_server():
    """
    启动CherryPy服务器。
    """
    media_asset_app = MediaAssetManagement()
    cherrypy.quickstart(media_asset_app, config=config)

if __name__ == '__main__':
    start_server()
