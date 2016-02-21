# Larry Wells
# 02/20/2016

# Construct queues for each bucket/user

from divvy import db
from divvy.models import *
from divvy import rss_collector

# Return




if __name__ == '__main__':
    # Iterate over bucket rows
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





    





















    """
    Listofshit = rss_collector.buildContentObjects()
    for key,value in Listofshit.items():
        temp_feed = Content()
    """