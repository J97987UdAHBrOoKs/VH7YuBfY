# 代码生成时间: 2025-10-13 21:20:43
import os
from cherrypy import quickstart, expose, Request, Response
from hashlib import md5
from collections import defaultdict

# 定义一个重复文件检测器类
class DuplicateFileDetector:

    def __init__(self):
        # 初始化文件指纹映射
        self.file_hashes = defaultdict(list)

    # 计算文件的MD5值
    def _get_file_hash(self, file_path):
        hash_md5 = md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            return None
        return hash_md5.hexdigest()

    # 添加文件到检测器，同时检测是否有重复
    @expose
    def add_file(self, file_path: str, *args, **kwargs):
        """
        添加文件到检测器并检查是否有重复文件存在。
        :param file_path: 文件路径
        :return: JSON响应，包含文件是否重复及其路径
        """
        file_hash = self._get_file_hash(file_path)
        if file_hash is None:
            return Response("File not found", status=404)

        # 如果文件哈希已存在，则表明发现重复文件
        if file_hash in self.file_hashes:
            return Response(
                f'Duplicate file detected: {self.file_hashes[file_hash]}',
                status=200,
                headers=[('Content-Type', 'application/json')]
            )
        else:
            self.file_hashes[file_hash].append(file_path)
            return Response(
                f'File added: {file_path}',
                status=201,
                headers=[('Content-Type', 'application/json')]
            )

    # 列出所有重复文件
    @expose
    def list_duplicates(self, *args, **kwargs):
        """
        列出所有重复文件的详细信息。
        :return: JSON响应，包含所有重复文件集合
        """
        duplicates = {
            hash: paths
            for hash, paths in self.file_hashes.items()
            if len(paths) > 1
        }
        return Response(
            json.dumps(duplicates),
            status=200,
            headers=[('Content-Type', 'application/json')]
        )

# 设置CherryPy服务器配置
config = {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
    'tools.response_headers.on': True,
    'tools.response_headers.headers': [('Content-Type', 'application/json')],
}

# 快速启动CherryPy服务器
quickstart(DuplicateFileDetector(), '/', config)
