
# A very simple Flask Hello World app for you to get started with...

from app import app, db
from app.models import User, Group


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Group' : Group}


if __name__ == '__main__':
    app.run()
