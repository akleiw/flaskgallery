from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import Config, app, cache, db, gphotos, log, service
from app.forms import LoginForm, RegistrationForm
from app.models import Album, User


@app.route("/index")
def index_redirect():
    return redirect(url_for("gallery"))


@app.route("/")
def gallery():
    if request.method == "GET":
        log.debug("gphotos.get_albums() called")
        return render_template("gallery.html", title=Config.GALLERY_TITLE, albums=gphotos.get_albums())


@app.route("/a/<album_name>")
def album(album_name):
    album = Album.query.filter_by(url_title=album_name).first()
    if not album:
        abort(404)
    media_list = gphotos.get_media(album.gphotos_id)
    return render_template("album.html", title=album.title, album=album, media=media_list)


@app.route("/reload_albums")
def reload_albums():
    """Delete and refresh cached albums from gphotos"""
    if request.method == "GET":
        gphotos.cache_albums()
        cache.delete_memoized(gphotos.get_media)
        return "OK"


@app.route("/manage_albums")
@login_required
def manage_albums():
    if not current_user.is_admin():
        abort(403)
    return render_template("gallery.html", title=Config.GALLERY_TITLE, albums=gphotos.get_albums())


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = "/"
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect("/")
