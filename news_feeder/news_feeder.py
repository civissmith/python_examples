#!/usr/bin/python3 -B
################################################################################
# @Title: news_feeder.py
#
# @Author: Phil Smith
#
# @Date: Sat, 17-Jan-15 06:39PM
#
# @Project: Python Examples
#
# @Purpose: Downloads news articles.
#
# # To-Do List:
# TODO 1.) Parameterize the 'address' variables for each function.
# TODO 2.) Add support to grab interesting articles and capture their story.
# TODO 3.) Break down functions more. Each 'get_' function does the same thing
#          so they can be made more generic.
#
################################################################################
import re
import urllib.request as ur
from bs4 import BeautifulSoup

################################################################################
#                                 Page Readers                                 #
################################################################################

def get_washington_post():
   """
   Download info from the Washington Post.
   """
   print("*** News from The Washington Post ***")

   # The 'national' page has it's own formatting for some dumb reason.
   # This implementation works only for the odd duck.
   address = "http://www.washingtonpost.com/national" 

   #address = "http://www.washingtonpost.com/business/technology" 

   page_bs = read_web_page( address )

   # Search for the articles.
   stories = page_bs.findAll('div', {'class':re.compile('story-body.*')}) 

   for story in stories:
     headline = story.find('div', {'class','story-headline'})
     desc     = story.find('div', {'class','story-description'})
     if headline and desc:
        print("Link: "+headline.h3.a.attrs['href'])
        print(headline.h3.a.get_text())
        print(desc.get_text())
     print() 
   print("*** End of News from The Washington Post ***")


def get_reuters():
   """
   Download info from Reuters.
   """
   # With Reuters, 'topStory' or 'feature' divisions mark articles.
   #address = "http://www.reuters.com/news/us"
   address = "http://www.reuters.com/news/technology"
   raw_page = read_web_page( address )
   web_page = condense_data( raw_page )

   # Search for the articles.
   # <div class="topStory"> </p> - Article and paragraph data.
   # <div class="feature"><h2> </p> - Article and paragraph data. Without <h2>, regex will
   #                                  grab videos and screw up.
   top_story_found = re.findall( r'<div class="topStory">(.*?)</p>', web_page )
   feature_found   = re.findall( r'<div class="feature"><h2>(.*?)</p>', web_page )

   if top_story_found or feature_found:
       for link in list(top_story_found + feature_found):
           # Separate the address and the description paragraph.
           address_found   = re.search(r'<a href="(.*?)"\s+>', link)
           paragraph_found = re.search(r'<p>(.*)', link)
           if address_found and paragraph_found:
               url = address
               url += address_found.group(1) 
               paragraph = paragraph_found.group(1)
               print( url )
               print( paragraph )
               print( )


def get_dailymail():
   """
   Download info from the Daily Mail.
   """

   # Daily Mail: "articletext" denotes article block with description.
   address = "http://www.dailymail.co.uk"
   raw_page = read_web_page( address )

   web_page = condense_data( raw_page )

   # Search for the articles.
   links_found = re.findall( r'<div class="articletext">(.*?)</div>', web_page )
   if links_found:
       for link in links_found:
           # Print the link and the description paragraph.
           # <a href=""/> - link address
           # <p class="refresh"></p> or <p></p> - description
           address_found   = re.search(r'<a href="(.*?)">', link)
           paragraph_found = re.search(r'<p class="refresh">(.*?)</p>|<p>(.*?)</p>', link)

           # Only save links with descriptions.
           if address_found and paragraph_found:

               url = "http://www.dailymail.co.uk"
               url += address_found.group(1).replace('" class="js-link-clickable','') 
               print( url )

               if paragraph_found.group(1):
                   print( paragraph_found.group(1).replace('<span class="tag-new">NEW</span>','' )) 
               if paragraph_found.group(2):
                   print( paragraph_found.group(2).replace('<span class="tag-new">NEW</span>','' )) 
               print()


def get_krqe13():
   """
   Download info from KRQE.
   """

   print("*** News from KRQE-13 ***")
   # Search for the articles.
   address = "http://krqe.com"

   # Get a BeautifulSoup object of the page
   page_bs = read_web_page( address )

   articles = page_bs.findAll('article', {'id':re.compile('post-\d+')})
   for art in articles:
      summaries = art.findAll('div', {'class':'entry-summary'})
      if summaries:
         print("Link: "+art.a.attrs['href'])
         for summary in summaries:
            print(summary.get_text().strip())
         print()

   print("*** End of News from KRQE-13 ***")

################################################################################
#                              Utility Functions                               #
################################################################################

def read_web_page( url ):
   """
   Reads the web page data and returns it uncooked.
   """
   # TODO: page = ... can time out: TimeoutError is raised.
   page = ur.urlopen( url )
   data = BeautifulSoup(page)

   # The data returned is now a BeautifulSoup object
   return data

if __name__ == "__main__":
    get_krqe13()
    get_washington_post()
#   get_reuters()
#   get_dailymail()
