Tumblr Downloader
=================

Downloads all the images or videos from a tumblr blog.

##Dependencies

Python libraries xmltodict and requests

### Install Dependencies

1. Install [pip](https://pypi.python.org/pypi/pip)
2. `pip install xmltodict requests`


##Install
1. Download dumblr.py
2. Copy dumblr.py to /usr/bin (or any other bin directory you've defined)
3. `chmod +x <path to dumblr.py>`

##Usage

```console
dumblr.py [site name] [media type]
```

Media type can be "photo" or "video" and defaults to "photo".

Example:

```
dumblr.py makingmoments video
```
