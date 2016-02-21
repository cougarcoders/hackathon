from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from forms import SignupForm, LoginForm
from models import User
from divvy import app, db, login_manager

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, delivery_method="1")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('app'))
        # message for wrong password goes here
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html')

@login_required
@app.route('/app', methods=['GET'])
def app():
    return render_template('app.html')
