import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or "something only you know"

    CACHE_TYPE = "simple"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 59 * 60  # 59 minutes

    GALLERY_TITLE = os.environ.get('GALLERY_TITLE')
    GALLERY_SUBTITLE = os.environ.get('GALLERY_SUBTITLE')
    GALLERY_SHORT = os.environ.get('GALLERY_SHORT')
    GALLERY_BUTTON_PRIMARY = os.environ.get('GALLERY_BUTTON_PRIMARY')
    GALLERY_BUTTON_PRIMARY_URL = os.environ.get('GALLERY_BUTTON_PRIMARY_URL')
    GALLERY_BUTTON_SECONDARY = os.environ.get('GALLERY_BUTTON_SECONDARY')
    GALLERY_BUTTON_SECONDARY_URL = os.environ.get('GALLERY_BUTTON_SECONDARY_URL')
