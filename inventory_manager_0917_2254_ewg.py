# 代码生成时间: 2025-09-17 22:54:29
import cherrypy
import json
from cherrypy.lib import sessions
from cherrypy._cptools import SessionObject, default_toolbox
from cherrypy.process.plugins import SimplePlugin

# 定义库存系统中的物品类
class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

# 库存管理系统类
class InventoryManager:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        """添加物品到库存"""
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
        else:
            self.items[item.name] = item

    def remove_item(self, item_name, quantity):
        """从库存中移除物品"""
        if item_name in self.items and self.items[item_name].quantity >= quantity:
            self.items[item_name].quantity -= quantity
            if self.items[item_name].quantity <= 0:
                del self.items[item_name]
        else:
            raise ValueError("Not enough quantity or item does not exist.")

    def get_item_quantity(self, item_name):
        """获取物品的库存数量"""
        if item_name in self.items:
            return self.items[item_name].quantity
        else:
            raise KeyError("Item does not exist.")

    def get_all_items(self):
        """获取所有物品的库存信息"""
        return self.items

# CherryPy 配置和路由
class InventoryApp:
    @cherrypy.expose
    def index(self):
        return "Welcome to the Inventory Management System!"

    @cherrypy.expose
    def add(self, item_name, quantity):
        try:
            item = Item(item_name, int(quantity))
            inventory.add_item(item)
            return json.dumps({'status': 'success', 'message': 'Item added successfully.'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    @cherrypy.expose
    def remove(self, item_name, quantity):
        try:
            inventory.remove_item(item_name, int(quantity))
            return json.dumps({'status': 'success', 'message': 'Item removed successfully.'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    @cherrypy.expose
    def quantity(self, item_name):
        try:
            quantity = inventory.get_item_quantity(item_name)
            return json.dumps({'status': 'success', 'data': {'quantity': quantity}})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    @cherrypy.expose
    def inventory(self):
        return json.dumps(inventory.get_all_items())

# 初始化库存管理器实例
inventory = InventoryManager()

if __name__ == '__main__':
    # 配置 CherryPy 服务
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080,
                             'engine.autoreload.on': False})
    # 启动 CherryPy 服务
    cherrypy.quickstart(InventoryApp())