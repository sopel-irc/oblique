import BeautifulSoup
import base64
import chardet
import codecs
import collections
import copy
import csv
import datetime
import dateutil
import encodings
import feedparser
import getopt
import glob
import gzip
import htmlentitydefs
import itertools
import new
import mailbox
import md5
import mimetypes
import operator
import os
import pytz
import quopri
import random
import re
import sets
import simplejson
import simplejson as json
import socket
import string
import StringIO
import sys
import textwrap
import time
import unescape
import unicodedata
import urllib
import urllib2
import urlparse
import xml
import zlib
from BeautifulSoup import BeautifulSoup as soup
from html2text import html2text
from os import path
from xml.dom import minidom

from google.appengine import api

import base

def get(uri):
    return urllib.urlopen(uri).read()

def text(html):
    return html2text(html).encode("utf8")

def run(uri):
    exec(get(uri))

def load(uri):
    load.module = new.module("module")
    exec get(uri) in load.module.__dict__
    return load.module


SAFER_BUILTINS = dict(__builtins__)
del SAFER_BUILTINS['globals']


class Main(base.RequestHandler):

    def get(self, *args):
        command = args[1] or ""
        command = urllib.unquote(command)
        output = StringIO.StringIO()
        sys.stdout = output
        sys.stderr = output
        try:
            try:
                output.write(str(eval(command, {'__builtins__': SAFER_BUILTINS})))
            except SyntaxError:
                exec(command, {'__builtins__': SAFER_BUILTINS})
            output.seek(0)
            self.ok(output.readline())
        except Exception, error:
            if str(error):
                return self.ok("%s: %s" % (type(error).__name__, str(error)))
            else:
                return self.ok(type(error).__name__)
