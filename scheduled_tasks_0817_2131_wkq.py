# 代码生成时间: 2025-08-17 21:31:50
import cherrypy
from cherrypy.process import plugins, servers
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from datetime import datetime

# 配置日志
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ScheduledTasks(object):
    """定时任务调度器"""
    def __init__(self):
        # 初始化CherryPy引擎
        self.engine = cherrypy.engine
        # 创建调度器
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
    def add_job(self, func, trigger, args, kwargs, id=None, name=None, replace_existing=False):
        """添加任务到调度器"""
        job = self.scheduler.add_job(func, trigger, args=args, kwargs=kwargs, id=id, name=name, replace_existing=replace_existing)
        logger.info(f"Added job {job.id}")
        return job
    
    def remove_job(self, job_id):
        """从调度器移除任务"""
        self.scheduler.remove_job(job_id)
        logger.info(f"Removed job {job_id}")
    
    def run(self):
        """启动CherryPy服务器"""
        self.engine.start()
        try:
            self.engine.block()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.engine.exit()
    
    @cherrypy.expose
    def index(self):
        "