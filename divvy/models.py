from datetime import datetime
from divvy import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import random

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(20))
    salt = db.Column(db.String(20))
    delivery_method = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')
        
    @password.setter 
    def password(self, pwd):
        chars=[]
        for i in range(20):
            chars.append(random.choice(self.username))
        self.salt = "".join(chars)
        self.password_hash = generate_password_hash(pwd+self.salt)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password+self.salt)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
    
    def __repr__(self):
        return '<User %r>' % self.username
        
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200),nullable=False)
    
    def __repr__(self):
        return self.description
    
class Bucket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))
    schedule = db.Column(db.Integer, nullable=True)
    max_item = db.Column(db.Integer)
    queue = db.Column(db.Integer, db.ForeignKey('queue.id'), nullable=True)
    delivery_method = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    
    def __repr__(self):
        return self.description
        
class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_empty = db.Column(db.DateTime, default=datetime.utcnow)
    
class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    last_polled = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return self.description

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    
    @staticmethod
    def all():
        return Tag.query.all()
        
    def sources(self):
        all_sources = Source_Tags.query.filter_by(tag_id=self.id)
        result = []
        for source in all_sources:
            result.append(source.source_id)
        return result
    
    def __repr__(self):
        return self.description
        
class SourceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return self.description
        
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), nullable=False)
    title = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=True)
    url= db.Column(db.Text, nullable=True)
    date_polled = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return self.title
        
class SourceType_Reminder(db.Model):
    source = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    message = db.Column(db.Text, nullable=False)
    
    
class SourceType_Bucket(db.Model):
    source = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    bucket = db.Column(db.Integer, db.ForeignKey('bucket.id', ondelete='cascade'))
    
class SourceType_RSS(db.Model):
    source = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    format = db.Column(db.Integer, nullable=False)
    url = db.Column(db.Text, nullable=False)

class Bucket_Sources(db.Model):
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id', ondelete='cascade'), primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)

class Source_Tags(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='cascade'), primary_key=True)
    
class Queue_Contents(db.Model):
    queue_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id', ondelete='cascade'), primary_key=True)