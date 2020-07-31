from app import app

@app.route('/index2')
def index2():
    return "Hello, World!"