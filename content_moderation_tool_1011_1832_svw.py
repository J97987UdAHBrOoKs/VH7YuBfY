# 代码生成时间: 2025-10-11 18:32:42
import cherrypy
def moderate_content(content):
    """
    函数：内容审核
    参数：content（str） - 需要审核的内容
    返回：审核结果（str）
    """
    banned_words = ["illegal", "banned"]  # 定义禁止的关键词
    for word in banned_words:
        if word in content.lower():  # 检查内容中是否包含禁止的关键词
            return "Content contains banned words."
    return "Content is approved."

class ContentModerationTool:
    """
    类：内容审核工具
    """
    @cherrypy.expose
    def index(self):
        """
        主页路由，提供表单进行内容提交
        """
        return "<form action='/moderate' method='post'>Content: <input type='text' name='content'><input type='submit' value='Moderate'></form>"

    @cherrypy.expose
    def moderate(self, content=""):
        """
        审核路由，处理表单提交的内容
        参数：content（str） - 提交的内容
        返回：审核结果
        """
        result = moderate_content(content)
        return f"<h1>Moderation Result: {result}</h1>"

if __name__ == '__main__':
    cherrypy.quickstart(ContentModerationTool())