# Larry Wells
# 02/20/2016

# Construct queues for each bucket/user

from divvy import db
from divvy.models import *
from divvy import rss_collector
from datetime import datetime
import time
import re
# Return




if __name__ == '__main__':
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
    
    for i in SourceType.query.all():
        print(str(i.id) + str(i.description))

    # Loop through buckets
    # foeach bucket loop through sources
    # foreach source, pull contents
    # iterate through contents, look at bucket schedule and then compare with last polled
    # 
    def fetch_content(fetch_schedule):
        print("Fetch Content Called\n")
        for b in Bucket.query.filter_by(schedule = fetch_schedule).all():
            b_list = b.sources()
            for source in b_list:
                content_list = source.contents()
                for c in content_list:
                    delivery_interval = b.schedule
                    print("\nSched Interval: " + str(delivery_interval))
                    print ("dt polled: " + str(c.date_polled))
                    print("dt now: " + str(datetime.now()))
                    time_difference = (datetime.now() - c.date_polled)
                    time_difference = (time_difference.days * 24 * 60) + (time_difference.seconds /60)
                    print("min diff: " + str(time_difference))
                    if time_difference >= delivery_interval:
                        print("**Time over schedule, fetch new content**")
                        print("Source Type: " + str(source.type))
                        for src_type in SourceType.query.filter_by(id = source.type).all():
                            print("*Source ID Match Found*")
                            # IF RSS FEED
                            if (src_type.id == 3):
                                print("Type = RSS")
                                for src_type_rss in SourceType_RSS.query.filter_by(source = source.id).all():
                                    print(src_type_rss.url)
                            # IF Reminder
                            elif(src_type.id == 2):
                                print("Type = Reminder")
                            # ELSE Bucket
                            else:
                                print("Type = Bucket")





    # DEBUG Shiz
    fetch_content(3)
"""
    rssSourceFileName = "divvy/rss_sources.txt"
    
    def readRSSSourceFile():
        rssSourceList = []
        # Open file as read only
        sourceFile = open(rssSourceFileName,"r")
        for line in sourceFile:
            rssSourceList.append(line)
        return rssSourceList

    for u in User.query.yield_per(1):
        print("User ID: " + str(u.id))
        for b in Bucket.query.all():
            if u.id == b.id:
                for b_source in Bucket_Sources.query.all():
                    if b_source.bucket_id == b.id:
                        print("found source id")
                        for s in Source.query.all():
                            if s.id == b_source.source_id:
                                print(s.id)
                                print(s.description)
                                print(s.type)
                                print(s.last_polled)
                                for st_rss in SourceType_RSS.query.all():
                                    if st_rss.source == s.id:
                                        print(st_rss.format)
                                        print(st_rss.url)

    Listofshit = []
    Listofshit = rss_collector.buildContentObjects(readRSSSourceFile())
    for key,value in Listofshit.items():
        print("***********************************")
        print("              NEW FEED             ")
        print("***********************************")
        print("Title: " + value.title)
        print("Body: " + re.sub('<[^>]*>','',value.body))
        print("URL: " + value.url)
        print("Date: " + str(value.date))
        print("\n\n")

"""
