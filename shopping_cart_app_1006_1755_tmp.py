# 代码生成时间: 2025-10-06 17:55:44
import cherrypy

# 购物车类
class ShoppingCart:
    def __init__(self):
        # 初始化购物车为空字典
        self.cart = {}

    def add_item(self, item_id, quantity):
        """添加商品到购物车"""
        if item_id in self.cart:
            self.cart[item_id] += quantity
        else:
            self.cart[item_id] = quantity
        return True

    def remove_item(self, item_id, quantity):
        """从购物车移除商品"""
        if item_id in self.cart:
            if self.cart[item_id] <= quantity:
                del self.cart[item_id]
            else:
                self.cart[item_id] -= quantity
            return True
        else:
            return False

    def get_cart(self):
        """获取当前购物车内容"""
        return self.cart

# CherryPy暴露的购物车服务类
class ShoppingCartService:
    def __init__(self):
        self.cart = ShoppingCart()

    @cherrypy.expose
    def add_to_cart(self, item_id, quantity):
        """添加商品到购物车接口"""
        try:
            if self.cart.add_item(item_id, int(quantity)):
                return {"status": "success", "message": "Item added to cart"}
            else:
                return {"status": "error", "message": "Item not added to cart"}
        except ValueError:
            return {"status": "error", "message": "Invalid quantity"}

    @cherrypy.expose
    def remove_from_cart(self, item_id, quantity):
        """从购物车移除商品接口"""
        if self.cart.remove_item(item_id, int(quantity)):
            return {"status": "success", "message": "Item removed from cart"}
        else:
            return {"status": "error", "message": "Item not found in cart"}

    @cherrypy.expose
    def view_cart(self):
        """查看购物车内容接口"""
        return self.cart.get_cart()

# CherryPy配置和启动
def start_server():
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(ShoppingCartService(), '/', conf)

if __name__ == '__main__':
    start_server()