from cgi import escape
from urlparse import parse_qs
from classes import PMLHTMLParser
import re
import io
import os, sys
from settings import *


def handle_newlines_wspace(html):
    nlines = ''.join(re.split(r'\n+', html))
    html   = ''.join(re.split(r'\s\s+', nlines))
    return html

def handle_pml(html):
    parser = PMLHTMLParser()
    html = handle_newlines_wspace(html)
    ret = parser.feed(html)
    return ret

def index(environ, start_response):
    status = '200 OK'
    d = parse_qs(environ['QUERY_STRING'])
    try:
        name = environ.get('LOGNAME', '')
    except:
        name = environ.get('USER', '')

    html = io.open('index.html', 'rb').read()
    
    # parse python code from html -- ONLY outputs to console from parser
    pml = handle_pml(html)
    
    # formulate response 
    if not pml: 
        response = html.replace("<pml>", "<h2> Thanks " + name + "</h2>" + "\n<p>")     
        response = response.replace("</pml>", "</p>", 1)
    else:
        response = ''.join(pml)
    
    headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response)))]
    start_response(status, headers)
    
    return response


def hello(environ, start_response):
    # get the name from the url if it was specified there.
    import datetime
    try:
        name = environ.get('LOGNAME', '')
        uagent = environ.get('HTTP_USER_AGENT', '')
    except:
        name = environ.get('USER', '')
        uagent = environ.get('HTTP_USER_AGENT', '')
    
    name = name.title()
    mac = re.compile(r'^.*?Macintosh.*?$')
    win = re.compile(r'^.*?Win.*?$')
    linux = re.compile(r'^.*?Ubu.*?$')
    safari = re.compile(r'^.*?afari.*?$')
    explorer = re.compile(r'^.*?xplorer.*?$')
    firefox  = re.compile(r'^.*?irefox.*?$')
    b = ''
    c = ''
    
    if safari.findall(uagent): b = 'Safari'
    elif explorer.findall(uagent): b = 'Internet Explorer'
    elif firefox.findall(uagent): b = 'Firefox'
    
    if mac.findall(uagent): c = ' on a Mac. Good Choice, ' + name + '!'
    elif win.findall(uagent): c = ' on a PC. We use what we have, right ' + name + '?'
    elif linux.findall(uagent): c = ' on an Ubuntu Box. Definately a solid decision, ' + name + '.'

    if b and c:
        uagent = b + c
    
    args = environ['pml.urls']
    print args
    if args:
        subject = escape(args[0])
    else:
        subject = '{0:%A %B %d}'.format(datetime.datetime.now())
    start_response('200 OK', [('Content-Type', 'text/html')])
    response = ["""<p>Hello <strong>{0}</strong>.</p>
               <p>It is {1}!</p>
               <p>Apparently you are using {2}</p>
               <p>
                I thoroughly enjoyed this exercise, as it exposed some classes and methods I have not worked with at such a low level.</p>
               <p>Given a similar task without restricting myself to the standard Python 2.7 Library, I would normally accomplish this using
                   <a href="https://docs.djangoproject.com/en/dev/howto/custom-template-tags/">
               <strong style="color:forestgreen">Django</strong></a> 
               </p><p>Thanks again for you time, {0}</p>""".format(name, subject, uagent)]

    return response

