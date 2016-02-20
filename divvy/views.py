from flask import Flask, request
from forms import SignupForm
from models import User
from divvy import app, db
from httplib2 import httplib2

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.passowrd.data, phone=form.phone.data, salt=form.salt.data, delivery_method=form.delivery_method.data)
        db.session.add(user)
        db.session.commit()
        return http.client.responses[http.client.OK] 
    return http.client.responses[http.client.BAD_REQUEST] 