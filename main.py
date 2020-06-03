from flask import Flask, request, make_response, redirect, render_template, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['TODO 1', 'TODO 2', 'TODO 3']


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    SubmitField = SubmitField('Enviar')


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
