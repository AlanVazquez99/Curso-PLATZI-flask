from flask import request, make_response, redirect, render_template, session, flash
import unittest

from app.forms import LoginForm
from app import create_app

app = create_app()

todos = ['TODO 1', 'TODO 2', 'TODO 3']



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def error_not_found(error):
    return render_template('./errors/404.html', error=error)


@app.errorhandler(500)
def error_server(error):
    return render_template('./errors/500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    login_form = LoginForm()
    contex = {
        'user_ip': session.get('user_ip'),
        'todos': todos,
        'login_form': login_form,
        'username': session.get('username'),
    }

    if login_form.validate_on_submit():
        session['username'] = login_form.username.data
        flash('El usuario se ha registrado con éxito', 'info')
        return redirect('/')

    return render_template('hello.html', **contex)
