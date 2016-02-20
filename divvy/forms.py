from flask_wtf import Form 
from wtforms.fields import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError

from models import User

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(3,80), Regexp('^[A-Za-z0-9_]{3,}$', message = 'Usernames consist of numbers, letters, and underscores.')])
    email = StringField('Email', validators=[DataRequired(), Length(1,120), Email()])
    phone = IntegerField('Phone', validators=[Length(10)])
    password = PasswordField('Password', validators=[DataRequired()])
    salt = StringField('Salt')
    delivery_method = StringField('Delivery Method')
