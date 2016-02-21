from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from forms import SignupForm, LoginForm
from models import User, Tag
from divvy import app, db, login_manager

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
        # message for wrong password goes here
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html')

@app.context_processor
def inject_tag():
    return dict(all_tags=Tag.all)

@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('main.html')
