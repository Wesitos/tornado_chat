from tornado.options import define

define("facebook_api_key", help="your Facebook application API key",
       default="--Api_key--")
define("facebook_secret", help="your Facebook application secret",
       default="--Api secret--")
define("cookie_secret", default=r"--- Generate Cookie Secre ---")
