from flask import Flask, request, make_response, redirect, render_template, abort

app = Flask(__name__)

todos = ['TODO 1', 'TODO 2', 'TODO 3']


@app.errorhandler(404)
def error_not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def error_server(error):
    return render_template('./errors/500.html', error=error)


@app.route('/errors/500')
def error_500():
    abort(500)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    contex = {
        'user_ip': user_ip,
        'todos': todos
    }

    return render_template('hello.html', **contex)
