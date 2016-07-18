#!/usr/bin/env python

# Usage: dumblr.py <site name>
# Example: dumblr.py makingmoments

import urllib2
import xmltodict
import sys
import requests
import os



def get_url(site, start = 0):
    url = "http://" + site + ".tumblr.com/api/read?type=photo&num=50&start=" + str(start)
    # print site  + str(start)
    return url

def get_data(url):
    file = urllib2.urlopen(url)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data

def get_image_urls(data):
    image_urls = []
    if isinstance(data["tumblr"]["posts"]["post"], list):
        posts = data["tumblr"]["posts"]["post"]
    else:
        posts = [data["tumblr"]["posts"]["post"]]
    for post in posts:
        # print post["photo-url"][0]["#text"]
        image_urls.append(post["photo-url"][0]["#text"])
    return image_urls

def save_files(site, image_urls):
    HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    session = requests.session()
    for url in image_urls:
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


if len(sys.argv) < 2:
    print "Need argument"
else:
    # print sys.argv[1]
    total = 0
    posts_retrieved = 0
    start = 0
    site = sys.argv[1]
    page = 0
    if not os.path.exists(site):
        os.makedirs(site)

    while True:
        page = page + 1
        url = get_url(site, start)
        start = start + 50
        data = get_data(url)
        if total == 0:
            total = int(data["tumblr"]["posts"]["@total"])
            print "Total pages: " + str(int(total/50))
        if posts_retrieved >= total:
            break

        print "Downloading images from page: " + str(page)
        image_urls = get_image_urls(data)

        save_files(site, image_urls)
        posts_retrieved = posts_retrieved + len(image_urls)
print "Completed"
