# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.auth.forms import LoginForm, RegisterForm

# Import module models (i.e. User)
from app.auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

from app import login_manager, login_user, login_required, logout_user, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@auth.route('/')
def index():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(username=form.username.data).first()
            if existing_user is None:
                username = form.username.data
                debt = 0.0
                own = 0.0
                hashpass = generate_password_hash(form.password.data, method='sha256')
                user = User(username=username, password=hashpass, own=own, debt=debt)
                user.save()
                login_user(user)
                return redirect(url_for('auth.dashboard'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated == True:
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('auth.dashboard'))
    return render_template('auth/login.html', form=form)


@auth.route('/dashboard')
@login_required
def dashboard():
    users = []
    for u in User.objects(username=current_user.username):
        users.append({"credit": u.own, "debt": u.debt, "username":u.username})

    return render_template('auth/dashboard.html', users=users, name=current_user.username)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
