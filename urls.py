#!/usr/bin/env python
from urlparse import parse_qs
from cgi import escape

urls = [
    (r'^$', index),
    (r'hello/?$', hello),
    (r'goodbye/(.+)$', goodbye)
]