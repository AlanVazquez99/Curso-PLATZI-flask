from flask import request, make_response, redirect, render_template, session, flash
from flask_login import login_required, current_user
import unittest

from app import create_app
from app import forms as form
from app import firestore_service as db

app = create_app()

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
@login_required
def hello():
    username = current_user.id
    todo_form = form.TodoForm()
    contex = {
        'user_ip': session.get('user_ip'),
        'todos': db.get_todos(username),
        'username': username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        description = todo_form.description.data
        db.todo_put(username, description)
        flash('Tarea agregada con exito')

    return render_template('hello.html', **contex)
