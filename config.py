import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    #     username="pilarski",
    #     password="passformysql",
    #     hostname="pilarski.mysql.pythonanywhere-services.com",
    #     databasename="pilarski$comments",
    # )

    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    SECRET_KEY = "something only you know"
