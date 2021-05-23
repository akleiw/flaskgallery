

import click
from app import app, db
from app.models import User, Role, Album


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Album': Album}


@app.cli.command("create-admin")
@click.argument("password")
def create_admin(password):
    admin_role = Role.query.filter_by(name='admin').first()
    admin = admin_role.users.first() or User(username='admin')
    admin.set_password(password)
    admin_role.users.append(admin)
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    app.run()
