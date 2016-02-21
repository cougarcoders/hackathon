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
    
    source1 = Source(description='Wired.com', type=sourcetype_RSS, last_polled = None)
    source2 = Source(description='Wired.com Desin', type=sourcetype_RSS3, last_polled = None)
    source3 = Source(description='Personal Reminder', type=sourcetype_reminder, last_polled = None)
    db.session.add(source1)
    db.session.add(source2)
    db.session.add(source3)
    
    RSS_source1 = SourceType_RSS(source=source1, format=1, url='http://feeds.wired.com/wired/index')
    RSS_source2 = SourceType_RSS(source=source2, format=2, url='http://www.wired.com/category/design/feed/')
    db.session.add(RSS_source1)
    db.session.add(RSS_source2)
    
    reminder_source = SourceType_Reminder(source=source3,message='Get up and do 10 squats')
    db.session.add(reminder_source)
    
    queue1 = Queue(last_empty=None)
    queue2 = Queue(last_empty=None)
    queue3 = Queue(last_empty=None)
    queue4 = Queue(last_empty=None)
    db.session.add(queue1)
    db.session.add(queue2)
    db.session.add(queue3)
    db.session.add(queue4)
    
    pham_bucket1 = Bucket(description='Tech stuffs', owner=dpham, schedule=1, max_item=10, queue=queue1, delivery_method=email_delivery1)
    pham_bucket2 = Bucket(description='Exercise stuffs', owner=dpham, schedule=2, max_time=3, queue=queue2, deliver_method=phone_delivery)
    larry_bucket = Bucket(description='Tech stuffs', owner=larry, schedule=3, max_item=5, queue=queue3, delivery_method=email_delivery)
    todd_bucket = Bucket(description='Tech things', owner=todd, schedule=4, max_item=7, queue=queue4, delivery_method=phone_delivery)
    db.session.add(pham_bucket1)
    db.session.add(pham_bucket2)
    db.session.add(larry_bucket)
    db.session.add(todd_bucket)
    
    content1 = Content(source=source1, title=r"Even Einstein Didn’t Think Gravitational Waves Existed", body='The body of this content', url="http://feeds.wired.com/c/35185/f/661370/s/4db9ee31/sc/28/l/0L0Swired0N0C20A160C0A20Ceven0Eeinstein0Edidnt0Ethink0Egravitational0Ewaves0Eexisted0C/story01.htm", date_polled=None))
    content2 = Content(source=source2, title='Why Use a Paintbrush When You Can Make Mind-Bending Art With Code?', body='Body of this content, something real hairy', url="http://www.wired.com/2016/02/why-use-a-paintbrush-when-you-can-make-mind-bending-art-with-code/", date_polled=None)
    content3 = Content(source=source3, title='Get up and do 10 squats', body=None, url=None, date_polled=None)
    db.session.add(content1)
    db.session.add(content2)
    db.session.add(content3)
    
    tag1 = Tag(description='Technology')
    tag2 = Tag(description='Reminder')
    tag3 = Tag(description='Food')
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    
    bucket_sources = Bucket_Sources(bucket_id = pham_bucket1, source_id = source1)
    db.session.add(bucket_sources)
    
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
