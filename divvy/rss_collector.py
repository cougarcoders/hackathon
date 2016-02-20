# Larry Wells
# 02/20/2016

# RSS Feed Object Class 
# Continually build list of RSS source URLs from RSSSources.txt
# Foreach RSS Feed, create Content Object and store in database


import feedparser
import time
import schedule
import RSSContent


# RSS Feed Content Class
class RSSContent(object):
    def __init__(self, title, body, url, date):
        self.title = title
        self.body = body
        self.url = url
        self.date = date



# Variables
rssSourceFileName = "rss_sources.txt"


# Build new rss source list from RSSSources.txt
def readRSSSourceFile():
    rssSourceList = []
    # Open file as read only
    sourceFile = open(rssSourceFileName,"r")
    for line in sourceFile:
        #print(line)    DEBUG ONLY
        rssSourcesList.append(line)
    return rssSourceList

# Fetch each feed from URL and construct dictionary of RSSContent objects
def buildContentObjects():
    rssContentObjectDict = {}
    rssSourcesList = readRSSSourceFile()
    # foreach URL in rssSourcesList fetch data
    indexer = 0 #Used as the key for dictionary
    for feedURL in rssSourcesList:
        #print("Source URL = " + feedURL)
        # foreach rss feed in feedURL - RSS feeds can have many articles from source
        feedData = feedparser.parse(feedURL)
        for rssFeed in feedData.entries:
            #print("RSS Feed: " + rssFeed['title'].encode("utf_8"))
            if len(rssFeed['title']) > 0:
                rssContentObjectDict[indexer] = RSSContent(rssFeed['title'].encode("utf_8"),rssFeed['description'].encode("utf_8"),rssFeed['link'].encode("utf_8"),rssFeed['published'])
                #print(rssContentObjectDict[indexer])
                indexer += 1
    #print("Objects Created: " + str(indexer))
    return  rssContentObjectDict

def debugPrintContentObjects():
    for dkey,value in buildContentObjects().items():
        print(value.title)





