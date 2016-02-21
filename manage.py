# -*- coding: utf-8 -*-
from divvy import app,db
from flask.ext.script import Manager, prompt_bool, Server
from divvy.models import *
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
server = Server(host='0.0.0.0', port=8000)
manager.add_command('runserver', server)

@manager.command
def initdb():
    db.create_all()
    email_delivery = Delivery(description='Delivery by Email')
    phone_delivery = Delivery(description='Delivery by Phone')
    db.session.add(email_delivery)
    db.session.add(phone_delivery)
    
    dpham = User(username='dpham', email='duongue@gmail.com', password='test', delivery_method=1)
    larry = User(username='larry', email='lgwells1@me.com', password='test', delivery_method=2)
    todd = User(username='todd', email='haliphax@gmail.com', password='test', delivery_method=1)
    db.session.add(dpham)
    db.session.add(larry)
    db.session.add(todd)
    
    sourcetype_bucket = SourceType(description="Bucket")
    sourcetype_reminder = SourceType(description="Reminder")
    sourcetype_RSS = SourceType(description='RSS Feed')
    db.session.add(sourcetype_bucket)
    db.session.add(sourcetype_reminder)
    db.session.add(sourcetype_RSS)
    
    source1 = Source(description='Wired.com', type=3, last_polled = None)
    source2 = Source(description='Wired.com Desin', type=3, last_polled = None)
    source3 = Source(description='Personal Reminder', type=2, last_polled = None)
    db.session.add(source1)
    db.session.add(source2)
    db.session.add(source3)
    
    RSS_source1 = SourceType_RSS(source=1, format=1, url="http://feeds.wired.com/wired/index", last_pubdate = None)
    RSS_source2 = SourceType_RSS(source=2, format=2, url="http://www.wired.com/category/design/feed/", last_pubdate = None)
    db.session.add(RSS_source1)
    db.session.add(RSS_source2)
    
    reminder_source = SourceType_Reminder(source=3,message='Get up and do 10 squats')
    db.session.add(reminder_source)
    
    queue1 = Queue(last_empty=None)
    queue2 = Queue(last_empty=None)
    queue3 = Queue(last_empty=None)
    queue4 = Queue(last_empty=None)
    db.session.add(queue1)
    db.session.add(queue2)
    db.session.add(queue3)
    db.session.add(queue4)
    
    pham_bucket1 = Bucket(description='Tech stuffs', owner=1, schedule=1, max_item=10, queue=1, delivery_method=1)
    pham_bucket2 = Bucket(description='Exercise stuffs', owner=1, schedule=2, max_item=3, queue=2, delivery_method=2)
    larry_bucket = Bucket(description='Tech stuffs', owner=2, schedule=3, max_item=5, queue=3, delivery_method=1)
    todd_bucket = Bucket(description='Tech things', owner=3, schedule=4, max_item=7, queue=4, delivery_method=2)
    db.session.add(pham_bucket1)
    db.session.add(pham_bucket2)
    db.session.add(larry_bucket)
    db.session.add(todd_bucket)
    
    content1 = Content(source=1, title=u"Even Einstein Didnt Think Gravitational Waves Existed", body='The body of this content', url="www.bit.ly/something", date_polled=None)
    content2 = Content(source=2, title=u'Why Use a Paintbrush When You Can Make Mind-Bending Art With Code', body='Body of this content, something real hairy', url="www.bit.ly/something", date_polled=None)
    content3 = Content(source=3, title=u'Get up and do 10 squats', body=None, url=None, date_polled=None)
    db.session.add(content1)
    db.session.add(content2)
    db.session.add(content3)
    
    tag1 = Tag(description='Technology')
    tag2 = Tag(description='Reminder')
    tag3 = Tag(description='Food')
    tag4 = Tag(description='Health')
    tag5 = Tag(description='News')
    tag6 = Tag(description='Science')
    tag7 = Tag(description='Entertainment')
    tag8 = Tag(description='Miscellaneous')
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)
    db.session.add(tag5)
    db.session.add(tag6)
    db.session.add(tag7)
    db.session.add(tag8)
    
    bucket_sources = Bucket_Sources(bucket_id = 1, source_id = 1)
    db.session.add(bucket_sources)
    bucket_sources = Bucket_Sources(bucket_id = 2, source_id = 2)
    db.session.add(bucket_sources)
    bucket_sources = Bucket_Sources(bucket_id = 3, source_id = 1)
    db.session.add(bucket_sources)
    bucket_sources = Bucket_Sources(bucket_id = 3, source_id = 3)
    db.session.add(bucket_sources)
    bucket_sources = Bucket_Sources(bucket_id = 4, source_id = 2)
    db.session.add(bucket_sources)
    
    source_tags = Source_Tags(source_id = 1, tag_id = 1)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 1, tag_id = 2)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 2, tag_id = 3)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 3, tag_id = 1)
    db.session.add(source_tags)
    
    queue_contents = Queue_Contents(queue_id = 1, content_id = 1, bucket_id = 1)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 1, content_id = 2, bucket_id = 1)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 1, content_id = 3, bucket_id = 1)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 2, content_id = 1, bucket_id = 2)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 2, content_id = 3, bucket_id = 2)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 3, content_id = 1, bucket_id = 3)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 3, content_id = 2, bucket_id = 3)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 3, content_id = 3, bucket_id = 3)
    db.session.add(queue_contents)
    queue_contents = Queue_Contents(queue_id = 4, content_id = 3, bucket_id = 4)
    db.session.add(queue_contents)
    
    db.session.commit()
    
    print 'Initialized the database'
    
@manager.command
def dropdb():
    if prompt_bool(
        "Drop db and lose all your data"):
        db.drop_all()
    print 'Dropped the database'

if __name__ == '__main__':
    manager.run()
