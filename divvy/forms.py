from flask_wtf import Form
from flask_login import current_user
from wtforms.fields import IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError

from models import User, Delivery

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(3,80), Regexp('^[A-Za-z0-9_]{3,}$', message = 'Usernames consist of numbers, letters, and underscores.')])
    email = StringField('Email', validators=[DataRequired(), Length(1,120), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class ProfileForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,120), Email()])
    phone = StringField('Phone Number', validators=[Regexp('^$|^[0-9]{10}$', message='Phone number must be 10 digits only.')])
    delivery_method = SelectField('Delivery Method', coerce=int, choices=[(x.id, x.description) for x in Delivery.all()])
    password = PasswordField('Password', validators=[EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password')

    def validate(self):
        Form.validate(self)
        if (not self.phone.data
                and self.delivery_method.data == Delivery.query.filter_by(description='Delivery by Phone').first().id):
            self.delivery_method.errors = ('You must provide a phone number to use this method.',)
            return False
        return True

