#!/usr/bin/env python
import os, sys, re, io
from wsgiref.simple_server import make_server

PROJECT_ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)))
URLS_ROOT     = os.path.join(PROJECT_ROOT, "urls")
VIEWS_ROOT    = os.path.join(PROJECT_ROOT, "views")

sys.path.append(PROJECT_ROOT)
sys.path.append(URLS_ROOT)
sys.path.append(VIEWS_ROOT)

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def test_env_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    ret = ["{0}: {1}\n".format(key, value)
           for key, value in environ.iteritems()]
    return ret


from HTMLParser import HTMLParser

inPML = False

# create a subclass and override the handler methods
class PMLHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global inPML
        if tag.lower() == "pml":
            inPML = True
    def handle_endtag(self, tag):
        global inPML
        if tag.lower() == "pml":
            inPML = False
    def handle_data(self, data):
        global inPML
        if inPML:
            print data


def handle_pml(html):
    parser = PMLHTMLParser()
    ret = parser.handle_data(html)
    return ret


def start_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    res = handle_pml()
    return res


import re
from cgi import escape

def index(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    ret = io.open('index.html', 'rb').read()
    #ret = handle_pml(io.open('index.html', 'rb').read())
    return ret

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['pml.urls'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)


# map urls to functions
urls = [
    (r'^$', index),
    # (r'hello/?$', hello),
    # (r'hello/(.+)$', hello)
]


if __name__ == "__main__":
    # httpd = make_server('', 9001, test_env_app)
    # print "Serving tests on port 9001..."
    # httpd.serve_forever()

    httpd = make_server('', 9000, application)
    # httpd = make_server('', 9000, start_app)
    print "Serving on port 9000..."

    # Serve until process is killed
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass