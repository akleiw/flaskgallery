
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from gphotospy import authorize
from gphotospy.album import Album
from gphotospy.media import Media

import os
from app import app

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(THIS_FOLDER, "gphotos.json")


db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "something only you know"
login_manager = LoginManager()
login_manager.init_app(app)

service = authorize.init(CLIENT_SECRET)
album_manager = Album(service)
albums = {a.get('title'): a for a in album_manager.list()}



class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username = user_id).first()

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)


@app.route("/comments", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())
    else:
        if current_user.is_authenticated:
            comment = Comment(content=request.form["contents"], commenter=current_user)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('index'))

@app.route("/")
def gallery():
    if request.method == "GET":
        album_manager = Album(service)
        albums = {a.get('title'): a for a in album_manager.list()}
        return render_template("gallery.html", albums=albums.values())

@app.route("/a/<album_name>")
def album(album_name):
    media_manager = Media(service)
    album_id = albums[album_name].get('id')
    album_media_list = list(media_manager.search_album(album_id))
    return render_template("album.html", title=album_name, photos = album_media_list)



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
