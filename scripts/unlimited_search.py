# -*- coding: utf-8 -*-
#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import codecs

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


DEVELOPER_KEY = "AIzaSyBmqNvAJzcLf-bz9X66XwcL3z6GfVgM534"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

videos = []
ids = []

# Youtube API can return from 0 to 50 videos in one search
search_step = 50

# Amount of videos to crawl
amount = 500

# Search phrase
keyword = "Євромайдан"


def youtube_search(pageToken):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified keywoed.
  # The pageToken parameter identifies a specific page in the result set that should be returned. In an API response
  search_response = youtube.search().list(
    pageToken=pageToken,
    q=keyword,
    part="id,snippet",
    maxResults=search_step
  ).execute()


  # Add each result to the appropriate list

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      print (search_result["snippet"]["title"])
      ids.append(search_result["id"]["videoId"])
  return search_response.get("nextPageToken", [])

def write_results():
    with codecs.open('videos.txt', 'w', "utf-8") as outfile:
        for name in videos:
            outfile.write(name + u"\n")
    with open('ids.txt', 'w') as outfile:
        for name in ids:
            outfile.write(name + '\n')

if __name__ == "__main__":
    pageToken = ''
    for i in range(int(amount/search_step)):
        pageToken = youtube_search(pageToken)
    write_results()

