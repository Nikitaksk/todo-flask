from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager
from forms import LoginForm, RegisterForm
from models import User
from app import db, bcrypt

auth = Blueprint('auth', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        username = form.username.data
        if User.query.filter_by(name=username).first() != None:
            flash('This username is already taken', 'danger')
            return redirect(url_for('auth.register'))
        elif len(username) > 20:
            flash('Username is too long', 'danger')
            return redirect(url_for('auth.register'))
        elif len(username) < 6:
            flash('Username is too short', 'danger')
            return redirect(url_for('auth.register'))
        password = form.password.data
        if (len(password) < 6):
            flash('Password is too short', 'danger')
            return redirect(url_for('auth.register'))
        elif len(password) > 20:
            flash('Password is too long', 'danger')
            return redirect(url_for('auth.register'))
        repeat_password = form.repeat_password.data
        if repeat_password != password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(name=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Welcome to DoDo', 'success')
            return redirect(url_for('main.index'))
        except  Exception as e:
            # db.session.rollback()
            flash('Something went wrong', 'danger')
            return redirect(url_for('auth.register'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = form.username.data
        password = form.password.data
        db_user = User.query.filter_by(name=username).first()
        if db_user == None:
            flash('Invalid username', 'danger')
            return redirect(url_for('auth.login'))

        if bcrypt.check_password_hash(db_user.password, password):
            login_user(db_user, remember=True)
            flash('You are now logged in.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
