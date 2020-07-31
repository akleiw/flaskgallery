from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from gphotospy import authorize
from gphotospy.album import Album
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "something only you know"
login_manager = LoginManager()
login_manager.init_app(app)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(THIS_FOLDER, "gphotos.json")

service = authorize.init(CLIENT_SECRET)
album_manager = Album(service)
albums = {a.get('title'): a for a in album_manager.list()}


from app import routes
from app import models