from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# help gunicorn redirect 'http' to 'https'
app.wsgi_app = ProxyFix(app.wsgi_app)

from website import views, admin_views, config
from website.config import cors

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SERVER_NAME"] = config.SERVER_NAME

cors.init_app(app)