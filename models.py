from datetime import datetime
from divvy import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    salt = db.Column(db.String(20))
    delivery_method = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    
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