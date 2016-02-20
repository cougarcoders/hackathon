from flask import Flask, request, render_template
from forms import SignupForm
from models import User
from divvy import app, db

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.passowrd.data, phone=form.phone.data, salt=form.salt.data, delivery_method=form.delivery_method.data)
        db.session.add(user)
        db.session.commit()
        return
    return None, 400 