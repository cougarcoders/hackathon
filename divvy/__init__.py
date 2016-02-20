import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'divvy.db')
app.config['DEBUG'] = True
app.secret_key = os.getenv('SECRET_KEY', 'changemeplease')
db = SQLAlchemy(app)
__all__ = ["db", "app"]

import views
import models
