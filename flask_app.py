
# A very simple Flask Hello World app for you to get started with...

from app import app, db
from app.models import User, Role, Album


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role' : Role, 'Album' : Album}


if __name__ == '__main__':
    app.run()
