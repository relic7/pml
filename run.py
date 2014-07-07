#!/usr/bin/env python
import re
from wsgiref.simple_server import make_server

from urls import urls


def not_found(environ, start_response):
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



if __name__ == "__main__":

    httpd = make_server('', 9000, application)
    print "Serving on port 9000..."
    print "Visit http://localhost:9000 in your most convenient web browser" 
    httpd.serve_forever()    
    # Serve until process is killed by ctrl-c
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
