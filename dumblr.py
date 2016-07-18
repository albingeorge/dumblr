#!/usr/bin/env python

# Usage: dumblr.py <site name> <type>
# Example: dumblr.py makingmoments photo

import urllib2
import xmltodict
import sys
import requests
import os
import re


def get_url(site, media_type, start = 0):
    url = "http://" + site + ".tumblr.com/api/read?type=" + media_type + "&num=50&start=" + str(start)
    # print site  + str(start)
    return url

def get_data(url):
    file = urllib2.urlopen(url)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data

def get_urls(data, media_type):
    urls = []
    if isinstance(data["tumblr"]["posts"]["post"], list):
        posts = data["tumblr"]["posts"]["post"]
    else:
        posts = [data["tumblr"]["posts"]["post"]]
    for post in posts:
        if media_type == "photo":
            urls.append(post["photo-url"][0]["#text"])
        elif media_type == "video":
            video_data = post["video-player"][0]
            if video_data:
                match = re.search(r'src\=\"(.*?)\"', video_data)
                if match:
                    url = match.groups()[0]
                    urls.append(url + ".mp4")

    return urls

def save_files(site, urls):
    HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    session = requests.session()
    for url in urls:
        ignored, filename = url.rsplit('/', 1)

        # print os.path.join(site, filename)
        filename = os.path.join(site, filename)
        if os.path.exists(filename):
            continue
        with file(filename, 'wb') as outfile:
            response = session.get(url, headers=HEADERS)
            if not response.ok:
                break
            outfile.write(response.content)

def download(site, media_type):
    total = 0
    total_pages = 0
    posts_retrieved = 0
    start = 0

    page = 0

    while True:
        page = page + 1
        url = get_url(site, media_type, start)
        print url
        start = start + 50
        data = get_data(url)
        if total == 0:
            total = int(data["tumblr"]["posts"]["@total"])
            total_pages = int(total/50) + 1
            print "Total pages: " + str(total_pages)
        if page > total_pages:
            break

        print "Downloading " + media_type + "s from page: " + str(page)
        urls = get_urls(data, media_type)

        save_files(site, urls)
        posts_retrieved = posts_retrieved + len(urls)
    print "Completed download of all " + media_type + "s for " + site

if len(sys.argv) < 2:
    print "Need argument"
else:
    if len(sys.argv) > 2:
        media_type = sys.argv[2]
    else:
        media_type = "photo"
    site = sys.argv[1]

    if not os.path.exists(site):
        os.makedirs(site)

    download(site, media_type)
