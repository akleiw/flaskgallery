from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


from app import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


users_groups = db.Table(
    'users_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

albums_groups = db.Table(
    'albums_groups',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    groups = db.relationship(
        'Group', secondary=users_groups,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    gphotos_id = db.Column(db.String(100), index=True)


class Group(db.Model):
    """docstring for UserGroup"""
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    albums = db.relationship(
        'Album', secondary=albums_groups,
        backref=db.backref('groups', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<Group {}>'.format(self.name)
