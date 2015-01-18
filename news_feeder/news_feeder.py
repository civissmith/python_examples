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
import urllib.request as ur

def  get_washpost():
  #page = ur.urlopen('http://www.washingtonpost.com/business/technology')
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
  #page = ur.urlopen( "http://www.reuters.com/news/science" )
  page = ur.urlopen("http://www.reuters.com/news/us")
  data = page.readlines()
  lines = [ each.decode('utf-8').replace('\r','') for each in data ]
  html = open('page.html', 'w')
  for line in lines:
    html.write(line)

  html.close()

if __name__ == "__main__":
  get_reuters()
