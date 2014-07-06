#!/usr/bin/env python
import os, sys, re, io
from wsgiref.simple_server import make_server
from classes import PMLHTMLParser,HTMLParser


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


def handle_pml(html):
    parser = PMLHTMLParser()
    ret = parser.feed(html)
    return ret


import re
from cgi import escape
from urlparse import parse_qs

regex_pml = re.compile(r'</?\w+\s+[^>]*>')

def index(environ, start_response):
    status = '200 OK'
    d = parse_qs(environ['QUERY_STRING'])
    try:
        name = environ.get('LOGNAME', '')
    except:
        name = environ.get('USER', '')

    html = io.open('index.html', 'rb').read()
    pml = [p for p in html.split(' ') if regex_pml.findall(p)]

    response = html.replace("<pml>", "<h2> Thanks " + name + "</h2>")
    response = response.replace("</pml>", "",1)
    headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response)))]
    start_response(status, headers)
    pml = handle_pml(io.open('index.html', 'rb').read())
    return pml # response

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']


def hello(environ, start_response):
    # get the name from the url if it was specified there.
    try:
        name = environ.get('LOGNAME', '')
    except:
        name = environ.get('USER', '')

    args = environ['pml.urls']
    print args
    if args:
        subject = escape(args[0])
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["Hello {0} \nHello {1}!".format(name, subject)]


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
    (r'hello/?$', hello),
    # (r'hello/(.+)$', hello)
]


if __name__ == "__main__":
    # httpd = make_server('', 9001, test_env_app)
    # print "Serving tests on port 9001..."
    # httpd.serve_forever()

    httpd = make_server('', 9000, application)
    print "Serving on port 9000..."

    # Serve until process is killed
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass