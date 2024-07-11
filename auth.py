from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
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
        if form.validate():
            username = form.username.data
            if User.query.filter_by(name=username).first() != None:
                flash('This username is already taken', 'error')
                return redirect(url_for('auth.register'))
            password = form.password.data
            if password != form.repeat_password.data:
                flash('Passwords dont match.', 'error')
                return redirect(url_for('auth.register'))

            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(name=username, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('You are now logged in.', 'success')
                return redirect(url_for('main.index'))
            except  Exception as e:
                db.session.rollback()
                return ("Error while registering: " + str(e))
        else:
            if not form.username.validate():
                flash('Username is invalid', 'error')
                return redirect(url_for('auth.register'))
            else:
                flash('Password is invalid', 'error')
                return redirect(url_for('auth.register'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if form.validate():
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(name=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('You are now logged in.', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
