from tornado.web import UIModule


class ChatMessage(UIModule):
    def render(self,user, text):
        user_img = user["picture"]["data"]["url"]
        user_name = user["name"]
        return self.render_string(
            "chat_message.html",
            text=text,
            img=user_img,
            name=user_name)

class UserInput(UIModule):
    def render(self,user):
        user_img = user["picture"]["data"]["url"]
        user_name = user["name"]
        return self.render_string(
            "user_input.html",
            img=user_img,
            name=user_name)
    def javascript_files(self):
        return ["main.js"]
