# 代码生成时间: 2025-09-06 00:27:35
import cherrypy
import json
import os
import shutil
import zipfile
from datetime import datetime

# 定义备份和恢复的目录路径
BACKUP_DIR = "./backups"

class DataBackupRestore:
    def __init__(self):
        # 确保备份目录存在
        os.makedirs(BACKUP_DIR, exist_ok=True)

    @cherrypy.expose
    def backup(self, **kwargs):
        """执行数据备份"""
        try:
            # 获取当前时间戳作为备份文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_filename = f"backup_{timestamp}.zip"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            
            # 打包压缩备份文件
            with zipfile.ZipFile(backup_path, 'w') as zipf:
                # 这里假设需要备份的目录为data/
                data_dir = "./data/"
                for root, dirs, files in os.walk(data_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, data_dir))
            
            return json.dumps({"status": "success", "filename": backup_filename})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    @cherrypy.expose
    def restore(self, filename=None, **kwargs):
        """执行数据恢复"""
        if not filename:
            return json.dumps({"status": "error", "error": "No filename provided"})
        try:
            backup_path = os.path.join(BACKUP_DIR, filename)
            if not os.path.exists(backup_path):
                return json.dumps({"status": "error", "error": "Backup file not found"})
            
            # 解压备份文件
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall("./data/")
            
            return json.dumps({"status": "success", "message": "Data restored successfully"})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

if __name__ == '__main__':
    # 设置CherryPy配置
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080})

    # 安装和启动DataBackupRestore服务
    cherrypy.quickstart(DataBackupRestore())