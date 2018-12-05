#!/usr/bin/env python

# Usage: dumblr.py <site name>
# Example: dumblr.py makingmoments


import urllib
import sys
import os
import pprint
import pytumblr
from bs4 import BeautifulSoup


client = pytumblr.TumblrRestClient(
  '5dwIMgOCuf8D4OjK92hThcFbnG7Jnn78jOt4Z90AKtVTKOU3Ij',
  'BBgTeFW1Z9PLVBSTvnamLt59QZ1znHjUh414kHSBZlAgiBKw5a',
  'QRpK3JKLWIiKuXaSdQ9Xz3HU6G6tc2oilUbTeztXyc90eLfA6V',
  'IHwQgbH3nQhBBggvJITKlz3eMG5zMahuf4kkKbQVNa5RQwc5eJ'
)

def get_urls(data, media_type):
    urls = {}
    for post in data:
        post_id = post["id"]
        if media_type == "photo":
            if post["type"] == "text":
                urls[post_id] = []
                body = post["body"]

                soup = BeautifulSoup(body, 'html.parser')
                for link in soup.find_all('img'):
                    urls[post_id].append(link.get('src'))
            elif post["type"] == "photo":
                urls[post_id] = []
                for photo in post["photos"]:
                    urls[post_id].append(photo["original_size"]["url"])
            else:
                pprint.pprint(post)
                os.exit()
    return urls

def save_files(site, urls):
    for id in urls.keys():
        for index, url in enumerate(urls[id]):
            filename = str(id) + "_" + str(index + 1)
            filepath = os.path.join(site, filename) + ".jpg"
            if os.path.exists(filepath):
                continue
            urllib.urlretrieve(url, filepath)

def download(site, media_type):
    start = 0
    page = 0
    total_posts = 0
    while True:
        page = page + 1
        data = client.posts(site, media_type, offset=start, limit=50, filter="raw")
        total_posts = data["total_posts"]
        start = start + 50
        print "Downloading " + media_type + "s from page: " + str(page)
        urls = get_urls(data["posts"], media_type)
        save_files(site, urls)

        if start > total_posts:
            break

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
