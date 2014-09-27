import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.escape
import uimodules
from login import BaseHandler
import json

class WebSocketChatHandler(BaseHandler, WebSocketHandler):
    client_set= set()
    chat_cache = []
    cache_len = 10

    def open(self):
        print "WebSocket opened"
        # Agrega un cliente a la lista de clientes
        WebSocketChatHandler.client_set.add(self)

    def on_message(self, message):
        print "Mensaje Recibido"
        dict_message = json.loads(message)
        print message
        chat_template = uimodules.ChatMessage(self)
        user = self.get_current_user()
        if user:
            if dict_message["type"] == "message":
                chat_text = dict_message["text"]
                chat ={ "type": "message",
                        "user": user,
                        "rendered_text": chat_template.render(user,chat_text),
                        "text": chat_text,
                    }
                self.send_chat(chat)
        else:
            pass

    def on_close(self):
        print "WebSocket closed"
        # Elimina el cliente de la lista de clientes
        WebSocketChatHandler.client_set.remove(self)


    @classmethod
    def send_chat(cls, chat):
        print "Mandando mensaje a clientes"
        for client in cls.client_set:
            try:
                client.write_message(chat)
            except:
                print "Error mandando mensaje"
        
        chat.pop("rendered_text")
        cls.chat_cache.append(chat)
        if len(cls.chat_cache) > cls.cache_len:
            print "Truncando cache"
            cls.chat_cache = cls.chat_cache[-cls.cache_len:]

        
