from app import app, db, service, albums
from gphotospy.album import Album
from gphotospy.media import Media
from flask import redirect, render_template, request, url_for

from flask_login import login_user, logout_user, login_required, current_user

from app.models import Comment, User, load_user


@app.route("/comments/", methods=["GET", "POST"])
def index2():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())
    else:
        if current_user.is_authenticated:
            comment = Comment(content=request.form["contents"], commenter=current_user)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('index2'))

@app.route("/")
@app.route("/index")
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