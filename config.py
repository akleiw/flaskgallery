
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="pilarski",
        password="passformysql",
        hostname="pilarski.mysql.pythonanywhere-services.com",
        databasename="pilarski$comments",
    )


    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    SECRET_KEY = "something only you know"