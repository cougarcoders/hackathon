# Larry Wells
# 02/20/2016

# Construct queues for each bucket/user

from divvy import db
from divvy.models import *
from divvy import rss_collector
from datetime import datetime
import send_content
#import datetime
import time
import re
# Return




#if __name__ == '__main__':
if True:
    # Iterate over bucket rows
   

    #pham_bucket = Bucket.query.filter_by(owner = 1).first()
    #pham_queue = Queue.query.filter_by(id = pham_bucket.queue).first()
    #print(pham_queue.add_content(1))

    #larry_bucket = Bucket.query.filter_by(owner = 2).first()
    #larry_queue = Queue.query.filter_by(id = larry_bucket.queue).first()
    #print(larry_queue.flush())

    #new_content = Content(source = 1,title = 'something', body = 'here here', url = 'dkfjd', date_polled = None)
    #db.session.add(new_content)
    #print(new_content.id)
    #db.session.flush()
    #print(new_content.id)
    #db.session.commit()

    """
    sourceData = Source.query.first()
    print(sourceData.last_polled)
    print(sourceData.last_polled - datetime.timedelta(minutes=60))
    sourceData.last_polled = sourceData.last_polled - datetime.timedelta(minutes=720)
    db.session.flush()
    db.session.commit()
    
    """
    print("*** Source Type Key ***")
    for i in SourceType.query.all():
        print(str(i.id) + " | " + str(i.description))
    print("***********************\n")    

    def get_content(bucket_schedule):
        print("*** Fetch Content Called ***")
        #get buckets
        b_list = Bucket.query.filter_by(schedule= bucket_schedule).all()
        for b in b_list:
        #for b in Bucket.query.filter_by(schedule = bucket_schedule).all():
            bucket_sources_list = b.sources()
            bucket_queue = Queue.query.filter_by(id = b.queue).first()
            print("Found Queue")
            for src in bucket_sources_list:
                #If src.last_polled less than queue last empty then get fresh content
                if src.last_polled is None or (bucket_queue.last_empty is not None and src.last_polled < bucket_queue.last_empty):
                    print("************************************")
                    print("Source is old, gathering new content")
                    print("Source Type: " + str(src.type))
                    if src.type == 3:
                        print("Type is RSS")
                        print("Source ID: " + str(src.id))
                        for src_type_rss in SourceType_RSS.query.filter_by(source = src.id).all():
                            print(src_type_rss.source)
                            print(src_type_rss.url)
                            print("Getting New RSS Data")
                            tempList = []
                            tempList = rss_collector.buildContentObjects([src_type_rss.url])
                            print("Adding New Content to Database, be patient\n")
                            for key,value in tempList.items():
                                if bucket_queue.last_empty is None or value.date > bucket_queue.last_empty:
                                    new_content = Content(source = src.id,\
                                        title = value.title, \
                                        body = re.sub('<[^>]*>','',value.body), \
                                        url = value.url, \
                                        date_polled = None)
                                    db.session.add(new_content)
                                    db.session.flush()
                                    #flush lets me see content.id
                                    bucket_queue.add_content(new_content.id, b.id)
                            db.session.commit()
                    elif src.type == 2:
                        print("Type is Reminder")
                        for src_type_reminder in SourceType_Reminder.query.filter_by(source = src.id).all():
                            new_content_reminder = Content(source = src.id,\
                                title = src_type_reminder.message,\
                                body = None,\
                                url = None,\
                                date_polled = None)
                            db.session.add(new_content_reminder)
                            db.session.flush()
                            bucket_queue.add_content(new_content_reminder.id,b.id)
                        db.session.commit()
                    else:
                        print("Type is Bucket")
                    #update src.last_polled to datetime.now
                    src.last_polled = datetime.utcnow()
                    db.session.commit()
                # Check if last queue empty is older than source
                else:
                    print("bucket queue < src last polled")
                    # Add content to queue
                    for src_content in src.contents():
                        if bucket_queue.last_empty is None or src_content.date_polled > bucket_queue.last_empty:
                            bucket_queue.add_content(src_content.id, b.id)
                    db.session.commit()
                    """
                    print("Source Type: " + str(src.type))
                    if src.type == 3:
                        print("Type is RSS")
                        print("Source ID: " + str(src.id))
                        for src_type_rss in SourceType_RSS.query.filter_by(source = src.id).all():
                            print(src_type_rss.source)
                            print(src_type_rss.url)
                            bucket_queue.add_content(new_content.id, b.id)
                            db.session.commit()
                    elif src.type == 2:
                        print("Type is Reminder")
                    else:
                        print("Type is Bucket")
                    #update src.last_polled to datetime.now
                    src.last_polled = datetime.utcnow()
                    db.session.commit()
                    """



                    


    # get_content testing call - can delete - LW
    #get_content(3)
    def divvy_queue(bucket_schedule):
        print("*** Divvy Content Called ***")
        # get buckets
        """
        for b in Bucket.query.filter_by(schedule = bucket_schedule).all():
            # Get user contact info
            user_email = ''
            user_phone = ''
            for u in User.query.filter_by(id = b.owner).all():
                print("Getting user contact info")
                if b.delivery_method == 1:
                    user_email = u.email
                    print(user_email)
                else:
                    user_phone = u.phone
                    print(user_phone)
        """
        # Get queue from bucket schedule
        print("Getting Queue")
        for q in Queue.get_queue_from_bucket(bucket_schedule):
            bucket = q.get_bucket()
            u = User.query.filter_by(id = bucket.owner).first()
            print("Getting user contact info")
            if bucket.delivery_method == 1:
                user_email = u.email
                print(user_email)
            else:
                user_phone = u.phone
                print(user_phone)

            print("Getting Contents")
            tempConQue = q.contents()
            for q_content in tempConQue:
                print(q_content.type())
                if q_content.type() == 2:
                    if bucket.delivery_method == 1:
                        print("Sending Email - Reminder\n")
                        print("email:" + str(user_email))
                        print("title: " + str(q_content.title))
                        send_content.send_email_message(user_email,q_content.title,'','')
                    elif bucket.delivery_method == 2:
                        print("sending sms - Reminder\n")
                        print("phone: " + str(user_phone))
                        print("title: " + str(q_content.title))
                        send_content.send_sms_message(user_phone, q_content.title, '')
                    else: #is type bucket do nothing
                        print("Oops! It is Bucket, we currently do not suppose buckets.")
                elif q_content.type() == 3:   
                    if bucket.delivery_method == 1:
                        print("Sending email\n")
                        print("email: " + str(user_email))
                        print("title: " + str(q_content.title))
                        print("body: " + str(q_content.body))
                        print("url: " + str(q_content.url))
                        send_content.send_email_message(user_email, q_content.title, q_content.body, q_content.url)
                    else:
                        print("sending sms\n")
                        print("phone: " + str(user_phone))
                        print("title: " + str(q_content.title))
                        print("url: " + str(q_content.url))
                        send_content.send_sms_message(user_phone, q_content.title, q_content.url)
                else:
                    print("Oops! It is Bucket, we currently do not suppose buckets.")
                # Flush Queue
            print(q.flush())

                    
    # DEBUG call function for testing
    #divvy_queue(4)
