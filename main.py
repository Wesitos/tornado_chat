import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options, parse_command_line
from login import BaseHandler, AuthLoginHandler, AuthLogoutHandler
import secret
import uimodules
from chat import WebSocketChatHandler
import os.path

define("port", default=8888, help="run on the given port", type=int)

class IndexRedirectHandler(BaseHandler):
    def get(self):
        self.redirect("/chat/index.html")

class IndexHandler(BaseHandler):
    def get(self):
        chat_list = WebSocketChatHandler.chat_cache
        self.render("index.html", message_list=chat_list)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/chat/?", IndexRedirectHandler),
            (r"/chat/index.html", IndexHandler),
            (r"/chat/login", AuthLoginHandler),
            (r"/chat/websocket", WebSocketChatHandler),
            (r"/chat/logout", AuthLogoutHandler),
        ]
        settings = {
            "cookie_secret": options["cookie_secret"],
            "login_url": r"/chat/login",
            "xsrf_cookies": True,
            "facebook_api_key": options.facebook_api_key,
            "facebook_secret": options.facebook_secret,
            "debug": True,
            "ui_modules": uimodules,
            "static_path":os.path.join(os.path.dirname(__file__), "public"),
            "static_url_prefix": "/chat/static/",
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "autoescape": None,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def deploy_server():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    deploy_server()
