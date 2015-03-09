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
#
################################################################################
import re
import urllib.request as ur
################################################################################
#                                 Page Readers                                 #
################################################################################

def  get_washpost():
  
   page = ur.urlopen('http://www.washingtonpost.com/national')
   data = page.readlines()

   lines = [ each.decode('utf-8') for each in data ]

   html = open('page.html', 'w')
   for line in lines:

       # With Washington Post, the 'h2 class' tags on the sub-pages have the
       # links to the stories. Paths can be absolute (http://) or relative
       # (/business).
       # If the link is relative, prepend 'http://www.washingtonpost.com'.
       if "h2 class" in line.lower():
           html.write(line)
   html.close()

def get_reuters():
   # With Reuters, 'topStory' or 'feature' divisions mark articles.
   page = ur.urlopen("http://www.reuters.com/news/us")
   data = page.readlines()
   lines = [ each.decode('utf-8').replace('\r','') for each in data ]
   html = open('page.html', 'w')
   for line in lines:
       if "topStory" in line or "feature" in line:
           html.write(line)
   html.close()


def get_dailymail():

   # Daily Mail: "articletext" denotes article block with description.
   raw_page = read_web_page("http://www.dailymail.co.uk/ushome/index.html")

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

               address = "http://www.dailymail.co.uk"
               address += address_found.group(1).replace('" class="js-link-clickable','') 
               print( address )

               if paragraph_found.group(1):
                   print( paragraph_found.group(1).replace('<span class="tag-new">NEW</span>','' )) 
               if paragraph_found.group(2):
                   print( paragraph_found.group(2).replace('<span class="tag-new">NEW</span>','' )) 
               print()

################################################################################
#                              Utility Functions                               #
################################################################################
def condense_data( data ):
   """
   Takes a web page's data, decodes it, strips it and returns it as a
   single string.
   """
   # Combine every line into a single string.
   search_string = ""
   for line in data:
       search_string += line.decode("utf-8").strip()

   return search_string


def read_web_page( url ):
   """
   Reads the web page data and returns it uncooked.
   """
   page = ur.urlopen( url )
   data = page.readlines()

   # The data is expected to be UTF-8 encoded web data.
   return data

if __name__ == "__main__":
   get_dailymail()
