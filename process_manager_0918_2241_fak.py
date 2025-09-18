# 代码生成时间: 2025-09-18 22:41:01
import cherrypy
import psutil
import os
import signal

"""
Process Manager

This module provides a simple HTTP interface to manage system processes.
It allows listing processes, killing processes, and getting system information.
"""

class ProcessManager:
    def __init__(self):
        """Initialize the Process Manager."""
        pass

    @cherrypy.expose
    def list_processes(self):
        """List all running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    info = proc.info
                    if info['status'] != psutil.STATUS_ZOMBIE:
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return {"status": "success", "data": processes}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @cherrypy.expose
    def kill_process(self, pid):
        """Kill a process by its PID."""
        try:
            process = psutil.Process(int(pid))
            process.terminate()
            process.wait(timeout=1)
            if process.is_running():
                process.kill()
            return {"status": "success", "message": "Process killed successfully."}
        except (ValueError, psutil.NoSuchProcess):
            return {"status": "error", "message": "Invalid process ID."}
        except psutil.AccessDenied:
            return {"status": "error", "message": "Permission denied."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @cherrypy.expose
    def get_system_info(self):
        """Get system information."""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            mem_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            return {"status": "success", "data": {"cpu_usage": cpu_usage, "mem_usage": mem_usage, "disk_usage": disk_usage}}
        except Exception as e:
            return {"status": "error", "message": str(e)}


if __name__ == '__main__':
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        }
    }
    cherrypy.quickstart(ProcessManager(), config=config)