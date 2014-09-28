import tornado.gen
from tornado.auth import FacebookGraphMixin
from tornado.options import define, options

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("fb_user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

class AuthLoginHandler(BaseHandler, FacebookGraphMixin):
  @tornado.gen.coroutine
  def get(self):
    my_url = (self.request.protocol + "://" + self.request.host +
                  "chat/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
    print "my-url = " + my_url
    if self.get_argument("code", False):
      user = yield self.get_authenticated_user(
        redirect_uri=my_url,
        client_id=options["facebook_api_key"],
        client_secret=options["facebook_secret"],
        code=self.get_argument("code"))
      self._on_auth(user)
    else:
      yield self.authorize_redirect(
        redirect_uri = my_url,
        client_id = options["facebook_api_key"],
        extra_params = {"scope": "read_stream,offline_access"})

  def _on_auth(self, user):
    if not user:
      raise tornado.web.HTTPError(500, "Facebook auth failed")
    print "Usuario Autenticado", user["name"]
    self.set_secure_cookie("fb_user", tornado.escape.json_encode(user))
    self.redirect("/")

class AuthLogoutHandler(BaseHandler):
  def get(self):
    self.clear_cookie("fb_user")
    print "Usuario Desautenticado"
    self.redirect(self.get_argument("next", "/chat"))
