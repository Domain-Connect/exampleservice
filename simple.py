from bottle import route, run, Bottle, default_app

app = default_app()

@route('/hello')
def hello():
    return "Hello World!"

#app.run(host='localhost', port=8080)
