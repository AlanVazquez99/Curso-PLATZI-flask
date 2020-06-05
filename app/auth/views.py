from . import auth
from flask import render_template, session, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


from app.forms import LoginForm
from app import firestore_service as db
from app.models import UserData, UserModel


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_document = db.get_user(username)
        
        if user_document.to_dict() is not None:
            password_from_db = user_document.to_dict()['password']
            
            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo', 'info')
                redirect(url_for('hello'))
                
            else:
                flash('La informacion proporcionada no concide')
        
        else:
            flash('El usuario ingrsado no existe')
        
        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))
    

@auth.route('sigup', methods=['GET', 'POST'])
def sigup():
    sigup_form = LoginForm()
    context = {
        'sigup_form' : sigup_form
    }

    if sigup_form.validate_on_submit():
        username = sigup_form.username.data
        password = sigup_form.password.data
        user_document = db.get_user(username)

        if user_document.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            db.user_put(user_data)
            user = UserModel(user_data)
            
            login_user(user)
            flash('Bienvenido', 'info')
            return redirect( url_for('hello') )

        else:
            flash('El usuario ingresado ya existe')

    return render_template('sigup.html', **context)
