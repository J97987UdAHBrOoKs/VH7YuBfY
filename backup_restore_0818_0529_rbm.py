# 代码生成时间: 2025-08-18 05:29:17
import cherrypy
import shutil
import os
import json
from datetime import datetime

# 配置CherryPy服务器的访问路径
class BackupRestoreService:
    def __init__(self):
        self.backup_dir = "./backups/"  # 备份文件夹路径
        self.data_dir = "./data/"       # 数据文件夹路径
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    # 创建数据备份
    @cherrypy.expose
    def create_backup(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_file_name = f"{self.backup_dir}backup_{timestamp}.zip"
            shutil.make_archive(backup_file_name[:-4], 'zip', self.data_dir)
            return json.dumps({'status': 'success', 'message': 'Backup created successfully'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    # 恢复数据备份
    @cherrypy.expose
    def restore_backup(self, backup_file):
        try:
            if not os.path.exists(os.path.join(self.backup_dir, backup_file)):
                return json.dumps({'status': 'error', 'message': 'Backup file does not exist'})
            shutil.unpack_archive(os.path.join(self.backup_dir, backup_file), self.data_dir)
            return json.dumps({'status': 'success', 'message': 'Data restored successfully'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

# 配置CherryPy服务器
def start_server():
    conf = {
        '/': {
            'tools.sessions.on': True,
        },
    }
    cherrypy.quickstart(BackupRestoreService(), config=conf)

# 启动服务器
if __name__ == '__main__':
    start_server()