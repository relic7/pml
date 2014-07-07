import re, sys, os
from cgi import escape
from urlparse import parse_qs

regex_tag = re.compile(r'</?\w+\s+[^>]*>')
regex_pml = re.compile(r'</?pml>')

PROJECT_ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)))
URLS_ROOT     = os.path.join(PROJECT_ROOT, "urls")
VIEWS_ROOT    = os.path.join(PROJECT_ROOT, "views")

sys.path.append(PROJECT_ROOT)
sys.path.append(URLS_ROOT)
sys.path.append(VIEWS_ROOT)

html='''<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>PML File</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>

    <p>
        This is an example of a pml file
    </p>

    <pml>
        def f():
        return "<h2>Good Bye</h2>"

        pml = f()
    </pml>



    </body>
</html>'''
