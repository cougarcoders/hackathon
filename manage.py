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
    todd = User(username='todd', email='haliphax@gmail.com', password='test', delivery_method=2)
    db.session.add(dpham)
    db.session.add(larry)
    db.session.add(todd)
    
    sourcetype_bucket = SourceType(description="Bucket")
    sourcetype_reminder = SourceType(description="Reminder")
    sourcetype_RSS = SourceType(description='RSS Feed')
    db.session.add(sourcetype_bucket)
    db.session.add(sourcetype_reminder)
    db.session.add(sourcetype_RSS)
    
    source1 = Source(description='Wired.com', type=3)
    source2 = Source(description='Engadget.com', type=3)
    source3 = Source(description='Stand up', type=2)
    source4 = Source(description='Motivate', type=2)
    source5 = Source(description='Food and Wine', type=3)
    source6 = Source(description='Health.com', type=3)
    source7 = Source(description='Womens Health and Fitness', type=3)
    source8 = Source(description='BBC News', type=3)
    source9 = Source(description='CNN News', type=3)
    source10 = Source(description='SciecneDaily.com', type=3)
    source11 = Source(description='Livescience.com', type=3)
    source12 = Source(description='FeedBurner.com', type=3)
    source13 = Source(description='Joke 1', type=2)
    source14 = Source(description='Joke 2', type=2)
    #source15 = Source(description='Random Wiki Article', type=3)
    db.session.add(source1)
    db.session.add(source2)
    db.session.add(source3)
    db.session.add(source4)
    db.session.add(source5)
    db.session.add(source6)
    db.session.add(source7)
    db.session.add(source8)
    db.session.add(source9)
    db.session.add(source10)
    db.session.add(source11)
    db.session.add(source12)
    db.session.add(source13)
    db.session.add(source14)
    #db.session.add(source15)
    
    RSS_source1 = SourceType_RSS(source=1, format=1, url="http://feeds.wired.com/wired/index")
    RSS_source2 = SourceType_RSS(source=2, format=1, url="http://www.engadget.com/rss.xml")
    RSS_source3 = SourceType_RSS(source=5, format=1, url="feed://www.foodandwine.com/feeds/latest_articles")
    RSS_source4 = SourceType_RSS(source=6, format=1, url="www.health.com/health/food-recipes/feed")
    RSS_source5 = SourceType_RSS(source=7, format=1, url="feed://www.womenshealthandfitness.com.au/component/obrss/diet-nutrition")
    RSS_source6 = SourceType_RSS(source=8, format=1, url="feed://feeds.bbci.co.uk/news/rss.xml")
    RSS_source7 = SourceType_RSS(source=9, format=1, url="http://rss.cnn.com/rss/cnn_topstories.rss")
    RSS_source8 = SourceType_RSS(source=10, format=1, url="https://www.sciencedaily.com/rss/top.xml")
    RSS_source9 = SourceType_RSS(source=11, format=1, url="feed://www.livescience.com/home/feed/site.xml")
    RSS_source10 = SourceType_RSS(source=12, format=1, url="http://feeds.feedburner.com/RandomFactsBlog?format=xml")
    db.session.add(RSS_source1)
    db.session.add(RSS_source2)
    db.session.add(RSS_source3)
    db.session.add(RSS_source4)
    db.session.add(RSS_source5)
    db.session.add(RSS_source6)
    db.session.add(RSS_source7)
    db.session.add(RSS_source8)
    db.session.add(RSS_source9)
    db.session.add(RSS_source10)
    
    
    reminder_source1 = SourceType_Reminder(source=3,message='Get up and do 10 squats')
    reminder_source2 = SourceType_Reminder(source=4,message='Keep it up. You are awesome!')
    reminder_source3 = SourceType_Reminder(source=13,message="I totally understand how batteries feel because Im rarely ever included in things either.")
    reminder_source4 = SourceType_Reminder(source=14,message='You kill vegetarian vampires with a steak to the heart.')
    db.session.add(reminder_source1)
    db.session.add(reminder_source2)
    db.session.add(reminder_source3)
    db.session.add(reminder_source4)
    
    queue1 = Queue(last_empty=None)
    queue2 = Queue(last_empty=None)
    queue3 = Queue(last_empty=None)
    queue4 = Queue(last_empty=None)
    db.session.add(queue1)
    db.session.add(queue2)
    db.session.add(queue3)
    db.session.add(queue4)
    
    schedule1 = Schedule(description="Run every 15 minutes", interval='minute', frequency=15)
    schedule2 = Schedule(description="Run every 30 minutes", interval='minute', frequency=30)
    schedule3 = Schedule(description="Run every hour", interval='hour', frequency=1)
    schedule4 = Schedule(description="Run every day", interval='day', frequency=1)
    
    pham_bucket1 = Bucket(description='Tech stuffs', owner=1, schedule=1, max_item=10, queue=1, delivery_method=1)
    pham_bucket2 = Bucket(description='Exercise stuffs', owner=1, schedule=1, max_item=3, queue=2, delivery_method=2)
    larry_bucket = Bucket(description='Tech stuffs', owner=2, schedule=1, max_item=5, queue=3, delivery_method=1)
    todd_bucket = Bucket(description='Tech things', owner=3, schedule=1, max_item=7, queue=4, delivery_method=2)
    db.session.add(pham_bucket1)
    db.session.add(pham_bucket2)
    db.session.add(larry_bucket)
    db.session.add(todd_bucket)
    
    content1 = Content(source=1, title=u"Even Einstein Didnt Think Gravitational Waves Existed", body='The body of this content', url="http://www.bit.ly/something", date_polled=None)
    content2 = Content(source=2, title=u'Why Use a Paintbrush When You Can Make Mind-Bending Art With Code', body='Body of this content, something real hairy', url="htt[://www.bit.ly/something", date_polled=None)
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
    source_tags = Source_Tags(source_id = 2, tag_id = 1)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 3, tag_id = 2)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 4, tag_id = 2)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 5, tag_id = 3)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 6, tag_id = 3)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 6, tag_id = 4)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 7, tag_id = 4)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 8, tag_id = 5)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 9, tag_id = 5)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 10, tag_id = 6)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 11, tag_id = 6)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 13, tag_id = 7)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 14, tag_id = 7)
    db.session.add(source_tags)
    source_tags = Source_Tags(source_id = 12, tag_id = 8)
    db.session.add(source_tags)
    #source_tags = Source_Tags(source_id = 15, tag_id = 8)
    #db.session.add(source_tags)
    
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
