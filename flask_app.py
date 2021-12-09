import click

from app import app, db
from app.models import Album, Role, User


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Role": Role, "Album": Album}


@app.cli.command("create-admin")
@click.argument("password")
def create_admin(password):
    admin_role = Role.query.filter_by(name="admin").first()
    admin = admin_role.users.first() or User(username="admin")
    admin.set_password(password)
    admin_role.users.append(admin)
    db.session.add(admin)
    db.session.commit()


@app.cli.command("assign-role")
@click.argument("role_name")
def assign_role(role_name):
    """Assigns given role to all albums in gallery"""
    role = Role.query.filter_by(name=role_name).first()
    role.albums = Album.query.all()
    db.session.commit()


if __name__ == "__main__":
    app.run()
