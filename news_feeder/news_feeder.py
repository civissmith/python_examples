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

def get_washington_post():
   """
   Download info from the Washington Post.
   """
   address = "http://www.washingtonpost.com/national" 
   #address = "http://www.washingtonpost.com/business/technology" 
   raw_page = read_web_page( address )

   web_page = condense_data( raw_page )

   # Search for the articles.
   #<h2 class="no-left"> </h2> - Article and paragraph data.
   #<span class="blog-headline"> </span><br/> - Blog top story
   links_found = re.findall( '<h2 class="(no-left|headline )">(.*?)</h2>', web_page )

   links = [ each[1] for each in links_found ]
   for link in links:
       content_found   = re.search( '<a href="(.*?)">(.*)</a>', link )

       if content_found:
           url = content_found.group(1)
           if "http" not in url[:5]:
               url = address + url
           paragraph = content_found.group(2)

           # Cleanup the character encodings
           paragraph = paragraph.replace('&ldquo;','"')
           paragraph = paragraph.replace('&rdquo;','"')
           paragraph = paragraph.replace("&lsquo;","'")
           paragraph = paragraph.replace("&rsquo;","'")
           paragraph = paragraph.replace("&mdash;","-")
           paragraph = paragraph.replace("&nbsp;"," ")
           paragraph = paragraph.replace("&amp;","&")

           print( url )
           print( paragraph )
           print( )

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
   get_washington_post()
