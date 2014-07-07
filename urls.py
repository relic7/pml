#!/usr/bin/env python
from views import index, hello

urls = [
    (r'^$', index),
    (r'hello/?$', hello),
    #(r'goodbye/(.+)$', goodbye),
    #(r'testenv/?$', 'testenv')
    
]
