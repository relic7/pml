#!/usr/bin/env python
import os, sys
from wsgiref.simple_server import make_server

PROJECT_ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)))
URLS_ROOT     = os.path.join(PROJECT_ROOT, "urls")
VIEWS_ROOT    = os.path.join(PROJECT_ROOT, "views")

sys.path.append(PROJECT_ROOT)
sys.path.append(URLS_ROOT)
sys.path.append(VIEWS_ROOT)

def start_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain')] # HTTP Headers
    res = start_response(status, headers)

    # The returned object is going to be printed
    return res

if __name__ == "__main__":


    httpd = make_server('', 8000, start_app)
    print "Serving on port 8000..."

    # Serve until process is killed
    httpd.serve_forever()