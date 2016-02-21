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
    Buckets = db.relationship('Bucket', backref='user', lazy='dynamic')
    
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
    
    @staticmethod
    def all():
        return Delivery.query.all()

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
        
    # get all sources of a Bucket
    def sources(self):
        all_sources = Bucket_Sources.query.filter_by(bucket_id=self.id)
        result = []
        for source in all_sources:
            result.append(Source.query.get(source.source_id))
        return result
        
class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_empty = db.Column(db.DateTime, default=datetime.utcnow)
    
    # return all contents that are currently in this queue
    def contents(self):
        all_contents = Queue_Contents.query.filter_by(queue_id=self.id)
        result = []
        for content in all_contents:
            result.append(Content.query.get(content.content_id))
        return result
        
    # empty the all the contents out of this queue
    def flush(self):
        all_contents = Queue_Contents.query.filter_by(queue_id=self.id)
        for content in all_contents:
            db.session.delete(content)
        db.session.commit()
        return "Queue flushed"
        
    # add content to queue, skip if content is already in the queue
    def add_content(self, content_id):
        existing_content = Queue_Contents.query.filter_by(queue_id=self.id, content_id=content_id).first()
        if existing_content is not None:
            return "Content is already in the queue"
        else:
            queue_content = Queue_Contents(queue_id = self.id, content_id = content_id)
            db.session.add(queue_content)
            db.session.commit()
            return "Content added"
    
class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    last_polled = db.Column(db.DateTime, default=datetime.utcnow)
    
    # get all exiting contents for this source
    def contents(self):
        all_contents = Content.query.filter_by(source=self.id)
        result = []
        for content in all_contents:
            result.append(Content.query.get(content.id))
        return result
    
    def __repr__(self):
        return self.description

    def as_dict(self):
        return {'id': self.id,
                'description': self.description}

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    
    @staticmethod
    def all():
        return Tag.query.all()

    @staticmethod
    def all_dict():
        return [tag.as_dict() for tag in Tag.all()]
        
    # return all sources_id associated with this tag
    def sources(self):
        all_sources = Source_Tags.query.filter_by(tag_id=self.id)
        result = []
        for source in all_sources:
            result.append(source.source_id)
        return result
        
    # return all source objects associated with this tag
    def sources_object(self):
        all_sources = Source_Tags.query.filter_by(tag_id=self.id)
        result = []
        for source in all_sources:
            result.append(Source.query.get(source.source_id))
        return result
    
    def __repr__(self):
        return self.description

    def as_dict(self):
        return {'id': self.id,
                'description': self.description,
                'sources': [x.as_dict() for x in self.sources_object()]}
        
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
