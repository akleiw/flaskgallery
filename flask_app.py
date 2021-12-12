import click

from app import app, db
from app.models import Album, Role, User


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Role": Role, "Album": Album}


@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
@click.argument("role")
def create_user(username, password, role):
    role = Role.query.filter_by(name=role).first()
    user = User(username=username)
    user.set_password(password)
    role.users.append(user)
    db.session.add(user)
    db.session.commit()


@app.cli.command("create-role")
@click.argument("role")
def create_role(role: str):
    db.session.add(Role(name=role))
    db.session.commit()


@app.cli.command("assign-all")
@click.argument("role")
def assign_role(role):
    """Assigns given role to all albums in gallery"""
    role = Role.query.filter_by(name=role).first()
    role.albums = Album.query.all()
    db.session.commit()


if __name__ == "__main__":
    app.run()
