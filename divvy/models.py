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

    # add buckets for new User
    def add_bucket_new_user(self, num_bucket):
        for i in range (1, num_bucket+1):
            new_queue = Queue(last_empty = None)
            db.session.add(new_queue)
            db.session.flush()
            new_bucket = Bucket(description = 'Bucket '+str(i) , owner = self.id, schedule = i, max_item = 10, queue = new_queue.id, delivery_method = 1)
            db.session.add(new_bucket)
            db.session.flush()
        db.session.commit()
        return 'Created {} buckets for user {}'.format(num_bucket, self)

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

    @staticmethod
    def all():
        return Bucket.query.all()

    @staticmethod
    def for_user_as_dict(id):
        return [bucket.as_dict() for bucket in Bucket.query.filter_by(owner=id)]

    # get all sources of a Bucket
    def sources(self):
        all_sources = Bucket_Sources.query.filter_by(bucket_id=self.id)
        result = []
        for source in all_sources:
            result.append(Source.query.get(source.source_id))
        return result

    def sources_object(self):
        return [source.as_dict() for source in self.sources()]

    def as_dict(self):
        return {'id': self.id,
                'description': self.description,
                'schedule': self.schedule,
                'sources': self.sources_object()}

    # add source to bucket
    def add_source(self, source_id):
        check_bucket_source = Bucket_Sources.query.filter_by(bucket_id = self.id, source_id = source_id).first()
        if check_bucket_source is None:
            new_bucket_source = Bucket_Sources(bucket_id = self.id, source_id = source_id)
            db.session.add(new_bucket_source)
            db.session.commit()
            return True
        else:
            return False

    # remove source fro bucket
    def remove_source(self, source_id):
        check_bucket_source = Bucket_Sources.query.filter_by(bucket_id = self.id, source_id = source_id).first()
        if check_bucket_source is not None:
            db.session.delete(check_bucket_source)
            db.session.commit()
            return True
        else:
            return False

    # flush this bucket's queue contents
    def flush_queue(self):
        contents_to_delete = Queue_Contents.query.filter_by(queue_id = self.queue, bucket_id = self.id)
        for queue_content in contents_to_delete:
            db.session.delete(queue_content)
        db.session.commit()
        return 'Bucket queue flushed'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    interval = db.Column(db.String(10), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_empty = db.Column(db.DateTime, default=None)

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
        self.last_empty=datetime.utcnow
        return "Queue {} flushed".format(self.id)

    # add content to queue, skip if content is already in the queue
    def add_content(self, content_id, bucket_id):
        existing_content = Queue_Contents.query.filter_by(queue_id=self.id, content_id=content_id).first()
        if existing_content is not None:
            return "Content {} is already in the queue".format(content_id)
        else:
            queue_content = Queue_Contents(queue_id = self.id, content_id = content_id, bucket_id = bucket_id)
            db.session.add(queue_content)
            db.session.commit()
            # query can be improved
            if Queue_Contents.query.filter_by(queue_id = self.id, bucket_id = bucket_id).count() > Bucket.query.get(bucket_id).max_item:
                return "Content {} added to queue {} and ".format(content_id, self.id) + self.prune_queue(bucket_id)
            else:
                return "Content {} added to queue {}".format(content_id, self.id)

    # prune contents from queue
    def prune_queue(self, bucket_id):
        max_item = Bucket.query.get(bucket_id).max_item
        size_of_queue = Queue_Contents.query.filter_by(queue_id = self.id, bucket_id = bucket_id).count()
        # this query returns a list of <Queue_Contnets, Content> records
        query = db.session.query(Queue_Contents, Content)\
            .filter(Queue_Contents.queue_id == self.id)\
            .filter(Queue_Contents.content_id == Content.id)\
            .filter(Queue_Contents.bucket_id == bucket_id)
        Queue_Contents_Content_query_result = query.order_by(Content.date_polled).limit(size_of_queue - max_item).all()
        queue_content_to_delete = []
        for queue_content_content in Queue_Contents_Content_query_result:
            queue_content_to_delete.append(queue_content_content[0])
        for queue_content in queue_content_to_delete:
            db.session.delete(queue_content)
        db.session.commit()
        return "Queue {} pruned for bucket {}".format(self.id, bucket_id)

    # get back contents for a bucket
    def get_bucket_contents(self, bucket_id):
        queue_content_bucket = Queue_Contents.query.filter_by(queue_id = self.id, bucket_id = bucket_id)
        result = []
        for queue_content in queue_content_bucket:
            result.append(Content.query.get(queue_content.content_id))
        return result
        
    # clear queue contents for a bucket
    def clear_bucket_queue_content(self, bucket_id):
        queue_content_bucket = Queue_Contents.query.filter_by(queue_id = self.id, bucket_id = bucket_id)
        for queue_content in queue_content_bucket:
            db.session.delete(queue_content)
        db.session.commit()
        return "Clear queue for bucket {}".format(bucket_id)
        
    @staticmethod
    def get_queue_from_bucket(bucket_schedule):
        query = db.session.query(Queue, Bucket)\
            .filter(Queue.id == Bucket.queue)\
            .filter(Bucket.schedule == bucket_schedule)
        Queue_Bucket_Result = query.all()
        queue_to_return = []
        for queue_bucket in Queue_Bucket_Result:
            queue_to_return.append(queue_bucket[0])
        return queue_to_return
        
    # get bucket object from queue
    def get_bucket(self):
        return Bucket.query.filter_by(queue = self.id).first()

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    last_polled = db.Column(db.DateTime, default=None)

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

    def type(self):
        return Source.query.get(self.source).type

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
    last_pubdate = db.Column(db.DateTime, default=None)

class Bucket_Sources(db.Model):
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id', ondelete='cascade'), primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)

class Source_Tags(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='cascade'), primary_key=True)

class Queue_Contents(db.Model):
    queue_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id', ondelete='cascade'), primary_key=True)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id', ondelete='cascade'), primary_key=True)
