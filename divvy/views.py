from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from forms import SignupForm, LoginForm, ProfileForm
from models import User, Tag
from divvy import app, db, login_manager
import json

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, delivery_method="1")
        db.session.add(user)
        db.session.commit()
        user.add_bucket_new_user(4) # add 4 buckets to new user
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main'))
        form.username.errors = ('Invalid credentials.',)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    messages = ()
    form = ProfileForm()
    if not form.email.data:
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.delivery_method.data = current_user.delivery_method
    if form.validate_on_submit():
        user = User.get_by_username(current_user.username)
        if current_user.email != form.email.data:
            user.email = form.email.data
        if current_user.phone != form.phone.data:
            user.phone = form.phone.data
        if current_user.delivery_method != form.delivery_method.data:
            user.delivery_method = form.delivery_method.data
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        messages = ('Your profile has been updated.',)
    return render_template('profile.html', form=form, messages=messages)

@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('main.html')

@app.route('/tags', methods=['GET'])
@login_required
def tags():
    return json.dumps(Tag.all_dict())
