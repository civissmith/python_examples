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

   address = "http://www.washingtonpost.com/national" 
   #address = "http://www.washingtonpost.com/business/technology" 
   raw_page = read_web_page( address )

   web_page = condense_data( raw_page )

   # Search for the articles.
   #<h2 class="no-left"> </h2> - Article and paragraph data.
   #<span class="blog-headline"> </span><br/> - Blog top story
   links_found = re.findall( '<h2 class="(no-left|headline )">(.*?)</h2>', web_page )

   # Assemble the headline and normal links into a single list.
   links = [ each[1] for each in links_found ]
   for link in links:
       content_found   = re.search( '<a href="(.*?)">(.*)</a>', link )

       if content_found:
           url = content_found.group(1)
           if "http" not in url[:5]:
               url = address + url
           dirty_paragraph = content_found.group(2)

           # Cleanup the character encodings
           paragraph = deHTMLify( dirty_paragraph, mode="names" )

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


def get_krqe13():
   """
   Download info from KRQE.
   """

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


################################################################################
#                              Utility Functions                               #
################################################################################
def deHTMLify( text, mode ):
   """
   Cleans up the HTML ASCII codes from the given text and returns a clean string.
   """
   html_dec_codes = {
                      '8211' : "-",
                      '8212' : "--",
                      '8216' : "'",
                      '8217' : "'",
                      '8220' : '"',
                      '8221' : '"',
                    }
   html_codes = {
                  'ldquo': '"',
                  'rdquo': '"',
                  'lsquo': "'",
                  'rsquo': "'",
                  'mdash': "-",
                  'nbsp' : " ",
                  'amp'  : "&",
               }

   if mode == "hex":
       for code in html_dec_codes:
           char = html_dec_codes[code]
           text = text.replace( "&#%s;" % code, char )
       return text

   if mode == "names":
       for code in html_codes:
           char = html_codes[code]
           text = text.replace( "&%s;" % code, char )
       return text

# TODO: Fill out dictionaries to map these codes.
# Source: http://www.htmlhelp.com/reference/html40/entities/special.html
#  Character  Entity  Decimal   Hex   Rendering in Your Browser
#                                     Entity  Decimal   Hex
#  quotation mark = APL quote  &quot;  &#34;   &#x22;  "   "   "
#  ampersand   &amp;   &#38;   &#x26;  &   &   &
#  less-than sign  &lt;  &#60;   &#x3C;  <   <   <
#  greater-than sign   &gt;  &#62;   &#x3E;  >   >   >
#  Latin capital ligature OE   &OElig;   &#338;  &#x152;   Œ   Œ   Œ
#  Latin small ligature oe   &oelig;   &#339;  &#x153;   œ   œ   œ
#  Latin capital letter S with caron   &Scaron;  &#352;  &#x160;   Š   Š   Š
#  Latin small letter s with caron   &scaron;  &#353;  &#x161;   š   š   š
#  Latin capital letter Y with diaeresis   &Yuml;  &#376;  &#x178;   Ÿ   Ÿ   Ÿ
#  modifier letter circumflex accent   &circ;  &#710;  &#x2C6;   ˆ   ˆ   ˆ
#  small tilde   &tilde;   &#732;  &#x2DC;   ˜   ˜   ˜
#  en space  &ensp;  &#8194;   &#x2002;           
#  em space  &emsp;  &#8195;   &#x2003;           
#  thin space  &thinsp;  &#8201;   &#x2009;           
#  zero width non-joiner   &zwnj;  &#8204;   &#x200C;  ‌  ‌  ‌
#  zero width joiner   &zwj;   &#8205;   &#x200D;  ‍  ‍  ‍
#  left-to-right mark  &lrm;   &#8206;   &#x200E;  ‎  ‎  ‎
#  right-to-left mark  &rlm;   &#8207;   &#x200F;  ‏  ‏  ‏
#  en dash   &ndash;   &#8211;   &#x2013;  –   –   –
#  em dash   &mdash;   &#8212;   &#x2014;  —   —   —
#  left single quotation mark  &lsquo;   &#8216;   &#x2018;  ‘   ‘   ‘
#  right single quotation mark   &rsquo;   &#8217;   &#x2019;  ’   ’   ’
#  single low-9 quotation mark   &sbquo;   &#8218;   &#x201A;  ‚   ‚   ‚
#  left double quotation mark  &ldquo;   &#8220;   &#x201C;  “   “   “
#  right double quotation mark   &rdquo;   &#8221;   &#x201D;  ”   ”   ”
#  double low-9 quotation mark   &bdquo;   &#8222;   &#x201E;  „   „   „
#  dagger  &dagger;  &#8224;   &#x2020;  †   †   †
#  double dagger   &Dagger;  &#8225;   &#x2021;  ‡   ‡   ‡
#  per mille sign  &permil;  &#8240;   &#x2030;  ‰   ‰   ‰
#  single left-pointing angle quotation mark   &lsaquo;  &#8249;   &#x2039;  ‹   ‹   ‹
#  single right-pointing angle quotation mark  &rsaquo;  &#8250;   &#x203A;  ›   ›   ›
#  euro sign   &euro;  &#8364;   &#x20AC;  €   €   €


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
   data = BeautifulSoup(page)

   # The data returned is now a BeautifulSoup object
   return data

if __name__ == "__main__":
    get_krqe13()
#   get_washington_post()
#   get_reuters()
#   get_dailymail()
