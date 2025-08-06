# 代码生成时间: 2025-08-06 23:37:15
import cherrypy
import psutil
import platform
import os
from cherrypy.lib.static import serve_file

"""
System Performance Monitor using CherryPy

This module provides a simple web interface to monitor system performance metrics.
"""

class SystemPerformanceMonitor:
    """
    Class for handling system performance monitoring.
    """

    exposed = True

    @cherrypy.expose
    def index(self):
        """
        Serve the index page.
        """
        return serve_file('reources/index.html', dir=os.getcwd())

    @cherrypy.expose
    def cpu_usage(self):
        """
        Get CPU usage as a percentage.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return {
                'cpu_usage': cpu_usage
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    @cherrypy.expose
    def memory_usage(self):
        """
        Get memory usage statistics.
        """
        try:
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    @cherrypy.expose
    def disk_usage(self):
        """
        Get disk usage statistics.
        """
        try:
            partitions = psutil.disk_partitions()
            disk_usage = {}
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.device] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            return disk_usage
        except Exception as e:
            return {
                'error': str(e)
            }

    @cherrypy.expose
    def system_info(self):
        """
        Get system information.
        """
        try:
            info = {
                'platform': platform.platform(),
                'os': platform.system(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count()
            }
            return info
        except Exception as e:
            return {
                'error': str(e)
            }

# Configure and start the CherryPy server
if __name__ == '__main__':
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
            'tools.sessions.on': True
        }
    }
    cherrypy.quickstart(SystemPerformanceMonitor(), '/', config=config)