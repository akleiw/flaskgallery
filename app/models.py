# pylint: disable=no-member
import os
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


users_roles = db.Table(
    "users_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)

albums_roles = db.Table(
    "albums_roles",
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class User(UserMixin, db.Model):  # type: ignore
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    roles = db.relationship("Role", secondary=users_roles, backref=db.backref("users", lazy="dynamic"), lazy="dynamic")

    def is_admin(self) -> bool:
        return Role.get_admin_role() in self.roles  # pylint: disable=unsupported-membership-test

    def albums(self):
        if self.is_admin():
            return Album.query
        return (
            Album.query.join(albums_roles, (albums_roles.c.album_id == Album.id))
            .join(users_roles, (users_roles.c.role_id == albums_roles.c.role_id))
            .filter(users_roles.c.user_id == self.id)
        )

    def __repr__(self):
        return "<User {}>".format(self.username)


class Album(db.Model):  # type: ignore
    """Table for storing album metadata"""

    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    gphotos_id = db.Column(db.String(100), index=True)
    title = db.Column(db.String, index=True)
    url_title = db.Column(db.String, index=True)
    items_count = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime, index=True)

    def thumbnail_url(self):
        return os.path.join(app.static_url_path, app.config.get("THUMBNAIL_FOLDER"), self.gphotos_id + ".jpg")

    def __repr__(self):
        return "<Album {}>".format(self.title)


class Role(db.Model):  # type: ignore
    """docstring for Userrole"""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    albums = db.relationship(
        "Album", secondary=albums_roles, backref=db.backref("roles", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return "<Role {}>".format(self.name)

    @classmethod
    def get_public_role(cls):
        return cls.query.filter_by(name="public").first()

    @classmethod
    def get_admin_role(cls):
        return cls.query.filter_by(name="admin").first()
