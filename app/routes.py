from app import app, db, service, gphotos, cache
from gphotospy.media import Media, MediaItem
from flask import redirect, render_template, request, url_for, abort
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


@app.route("/index")
def index_redirect():
    return redirect(url_for('gallery'))


@app.route("/")
def gallery():
    if request.method == "GET":
        app.logger.debug('gphotos.get_albums() called')
        return render_template("gallery.html", title='MP Gallery', albums=gphotos.get_albums())


@app.route("/a/<album_name>")
def album(album_name):
    album = gphotos.get_albums().get(album_name)
    if not album:
        abort(404)
    media_list = gphotos.get_media(album.get('id'))
    return render_template("album.html", title=album.get('title'), album=album, media=media_list)


@app.route("/reload_albums")
def reload_albums():
    """Delete and refresh cached albums from gphotos"""
    if request.method == "GET":
        cache.delete_memoized(gphotos.get_albums)
        cache.delete_memoized(gphotos.get_media)
        gphotos.get_albums()
        return "OK"


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
