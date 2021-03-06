from app import app, db, service, gphotos, cache, Config
from app.forms import LoginForm, RegistrationForm
from flask import redirect, render_template, request, url_for, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from werkzeug.urls import url_parse


@app.route("/index")
def index_redirect():
    return redirect(url_for('gallery'))


@app.route("/")
def gallery():
    if request.method == "GET":
        app.logger.debug('gphotos.get_albums() called')
        return render_template("gallery.html", title=Config.GALLERY_TITLE, albums=gphotos.get_albums())


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/'
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect('/')
