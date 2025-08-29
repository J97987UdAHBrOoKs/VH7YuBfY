# 代码生成时间: 2025-08-29 13:49:06
import os
import shutil
import cherrypy
from cherrypy.lib.static import serve_file

class FileBackupSyncTool:
    """A CherryPy application that serves as a file backup and sync tool."""

    def __init__(self, source_dir, backup_dir):
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def sync(self):
        """Synchronizes the source directory with the backup directory."""
        for item in os.listdir(self.source_dir):
            source_item_path = os.path.join(self.source_dir, item)
            backup_item_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(source_item_path):
                if not os.path.exists(backup_item_path):
                    os.makedirs(backup_item_path)
                self.sync(backup_item_path)
            else:
                try:
                    shutil.copy2(source_item_path, backup_item_path)
                except Exception as e:
                    print(f"An error occurred while copying {item}: {e}")

    def backup(self):
        """Performs a complete backup of the source directory to the backup directory."""
        for item in os.listdir(self.source_dir):
            source_item_path = os.path.join(self.source_dir, item)
            backup_item_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(source_item_path):
                shutil.copytree(source_item_path, backup_item_path)
            else:
                try:
                    shutil.copy2(source_item_path, backup_item_path)
                except Exception as e:
                    print(f"An error occurred while copying {item}: {e}")

    @cherrypy.expose
    def index(self):
        "