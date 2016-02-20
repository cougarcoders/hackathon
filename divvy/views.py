from flask import Flask, request, render_template, redirect, url_for
from forms import SignupForm
from models import User
from divvy import app, db

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.passowrd.data, phone=form.phone.data, salt=form.salt.data, delivery_method=form.delivery_method.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', form=form), 400
