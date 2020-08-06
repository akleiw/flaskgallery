from app import app, db, service, utils
from gphotospy.album import Album
from gphotospy.media import Media, MediaItem
from flask import redirect, render_template, request, url_for

from flask_login import login_user, logout_user, login_required, current_user

from app.models import Comment, User, load_user


@app.route("/comments/", methods=["GET", "POST"])
def index2():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())
    else:
        if current_user.is_authenticated:
            comment = Comment(
                content=request.form["contents"], commenter=current_user)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('index2'))


@app.route("/")
@app.route("/index")
def gallery():
    if request.method == "GET":
        return render_template("gallery.html", title='MP Gallery', albums=utils.get_albums())


@app.route("/a/<album_name>")
def album(album_name):
    media_manager = Media(service)
    album_id = utils.get_albums()[album_name].get('id')
    album_media_list = (MediaItem(m)
                        for m in media_manager.search_album(album_id))
    return render_template("album.html", title=album_name, media=album_media_list)


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
    return redirect(url_for('index2'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index2'))
