import logging
import os

from config import Config
from flask import Flask
from flask.logging import create_logger
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from gphotospy import authorize

app = Flask(__name__)
app.config.from_object(Config)

log = create_logger(app)

moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(THIS_FOLDER, "gphotos.json")

service = authorize.init(CLIENT_SECRET)

app.config["ALBUM_THUMB_PATH"] = os.path.join(app.static_folder, app.config.get("THUMBNAIL_FOLDER"))
os.makedirs(app.config["ALBUM_THUMB_PATH"], exist_ok=True)

log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


from app import errors, gphotos, models, routes
