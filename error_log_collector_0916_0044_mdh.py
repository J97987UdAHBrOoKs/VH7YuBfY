# 代码生成时间: 2025-09-16 00:44:31
import cherrypy
from cherrypy.lib import log
import threading
import json
import os
from datetime import datetime

# 定义日志文件路径
LOG_DIR = "logs"
LOG_FILE = "error.log"

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 定义一个线程安全的日志记录器
class ThreadSafeLogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = threading.Lock()

    def log(self, message):
        with self.lock:
            with open(self.file_path, "a") as file:
                file.write(message + "
")

# 实例化日志记录器
logger = ThreadSafeLogger(os.path.join(LOG_DIR, LOG_FILE))

class ErrorLogCollector:
    """错误日志收集器服务"""

    @cherrypy.expose
    def submit_error_log(self, error_data):
        """提交错误日志"""
        try:
            # 解析错误数据
            error_data = json.loads(error_data)
            # 获取当前时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 构造日志消息
            log_message = f"[{timestamp}] {json.dumps(error_data)}"
            # 记录日志
            logger.log(log_message)
            return "{"status": "success"}"
        except Exception as e:
            # 处理异常并记录
            log_message = f"Error processing error log: {str(e)}"
            logger.log(log_message)
            raise cherrypy.HTTPError(500, "Failed to process error log")

if __name__ == '__main__':
    # 配置CherryPy服务器
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080,
                             'log.access_file': os.path.join(LOG_DIR, 'access.log'),
                             'log.error_file': os.path.join(LOG_DIR, 'error.log')
                             })
    # 启动CherryPy服务器
    cherrypy.quickstart(ErrorLogCollector())