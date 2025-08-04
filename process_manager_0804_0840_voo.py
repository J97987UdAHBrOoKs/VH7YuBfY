# 代码生成时间: 2025-08-04 08:40:15
import cherrypy
import psutil
import subprocess
import sys
import json

def get_processes():
    """获取当前所有进程信息
    
    返回一个包含进程信息的列表
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            process_info = proc.info
            processes.append({"pid": process_info['pid'], "name": process_info['name'], "create_time": process_info['create_time']})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  # 忽略无法访问的进程
            pass
    return processes

def kill_process(pid):  # 终止进程
    """终止指定的进程
    
    参数:
    - pid: 进程ID
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()  # 发送终止信号
        proc.wait()  # 等待进程终止
        return {"status": "success", "message": f"Process {pid} terminated successfully"}
    except psutil.NoSuchProcess:
        return {"status": "error", "message": f"No process with pid {pid} found"}
    except psutil.AccessDenied:
        return {"status": "error", "message": f"Access denied to process {pid}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def start_process(command):  # 启动新进程
    """启动新的进程
    
    参数:
    - command: 要执行的命令
    """
    try:
        subprocess.Popen(command, shell=True)
        return {"status": "success", "message": f"Process started with command: {command}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def expose(func):  # 装饰器，用于暴露函数为CherryPy的HTTP端点
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
    wrapper.exposed = True
    return wrapper

def start():  # 启动CherryPy服务器
    class ProcessManager:
        @expose
        @cherrypy.expose
        def get_processes(self):
            return get_processes()

        @expose
        @cherrypy.expose
        def kill_process(self, pid):
            return kill_process(int(pid))

        @expose
        @cherrypy.expose
        def start_process(self, command):
            return start_process(command)

    cherrypy.quickstart(ProcessManager())

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'start':
        start()
    else:
        print("Usage: python process_manager.py start")

if __name__ == '__main__':
    main()