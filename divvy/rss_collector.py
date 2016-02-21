# Larry Wells
# 02/20/2016

# RSS Feed Object Class 
# Continually build list of RSS source URLs from RSSSources.txt
# Foreach RSS Feed, create Content Object and store in database

import re
import feedparser
import shorten_url
import datetime
import time

# RSS Feed Content Class
class RSSContent(object):
    def __init__(self, title, body, url, date):
        self.title = title
        self.body = body
        self.url = url
        self.date = date



# Variables
rssSourceFileName = "divvy/rss_sources.txt"


# Build new rss source list from RSSSources.txt
def readRSSSourceFile():
    rssSourceList = []
    # Open file as read only
    sourceFile = open(rssSourceFileName,"r")
    for line in sourceFile:
        rssSourceList.append(line)
    return rssSourceList

# Fetch each feed from passed list of URLs and construct dictionary of RSSContent objects
def buildContentObjects(sources_list):
    rssContentObjectDict = {}
    rssSourcesList = sources_list
    # foreach URL in rssSourcesList fetch data
    indexer = 0 #Used as the key for dictionary
    for feedURL in rssSourcesList:
        # foreach rss feed in feedURL - RSS feeds can have many articles from source
        feedData = feedparser.parse(feedURL)
        for rssFeed in feedData.entries:
            #Check for null entries
            if len(rssFeed['title']) > 0:
                rssContentObjectDict[indexer] = RSSContent(rssFeed['title'].encode("utf_8"),\
                    rssFeed['description'].encode("utf_8"),\
                    rssFeed['link'].encode("utf_8"),\
                    format_date_to_utc(rssFeed['published_parsed']))
                indexer += 1
    return  rssContentObjectDict

# Format unicode date to UTC
def format_date_to_utc(date_time):
    # * expands list or dict into seperate args(new to me!)
    return datetime.datetime(*date_time[:6])


# Insert RSSContent objects into database
def insert_feeds_into_database():
    feeds_dict = buildContentObjects()
    for key,value in feeds_dict.items():
        print("nothing here yet")
        


# DEBUG Tools
def debugPrintContentObjects():
    print(len(buildContentObjects()))
    for key,value in buildContentObjects().items():
        print("***********************************")
        print("              NEW FEED             ")
        print("***********************************")
        print("Title: " + value.title)
        print("Body: " + re.sub('<[^>]*>','',value.body))
        print("URL: " + value.url)
        print("Date: " + str(value.date))
        print("\n\n")


