from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from gphotospy import authorize
from config import Config
import os
import logging


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(THIS_FOLDER, "gphotos.json")

service = authorize.init(CLIENT_SECRET)

app.config['ALBUM_THUMB_PATH'] = os.path.join(app.static_folder, app.config.get('THUMBNAIL_FOLDER'))
os.makedirs(app.config['ALBUM_THUMB_PATH'], exist_ok=True)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)


from app import routes
from app import models
from app import gphotos
from app import errors
