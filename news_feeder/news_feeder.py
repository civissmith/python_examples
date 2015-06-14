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
   print("*** News from Reuters ***")

   address = "http://www.reuters.com/news/us"
   #address = "http://www.reuters.com/news/technology"

   page_bs = read_web_page( address )


   # TODO: Add support for topStory tags. On some pages they are
   #       id=topStory, others are class=topStory
   #       NOTE:
   #       foo = page_bs.findAll('div', {'class':'topStory', 'id':'topStory'})
   #       does not capture them.
   #

   # Just collect the feature articles.
   features    = page_bs.findAll('div', {'class':'feature'})

   for feature in features:
      print(address + feature.h2.a.attrs['href'])
      print(feature.h2.a.get_text())
      try:
         print(feature.p.get_text())
      except AttributeError as e:
         pass
      print()
   print("*** End of News from Reuters ***")

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
    get_reuters()
