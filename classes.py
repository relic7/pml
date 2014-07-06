#!/usr/bin/env python
from urlparse import parse_qs
from cgi import escape
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from HTMLParser import HTMLParser
import tokenize
import StringIO

## Parser to extract text data within html
inPML = False
class PMLHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dataArray = []
        self.countFuncs = 0
        self.lasttag = None
        self.lastfuncname = None
        self.lastfuncpy = None

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
            return data

    def _python_interactive_indent(self, code):
        prev_toktype = tokenize.INDENT
        first_line = None
        last_lineno = -1
        last_col = 0

        output = ''

        tokgen = tokenize.generate_tokens(StringIO.StringIO(code).readline)
        indent = 0
        hasNL = False
        prefixed = False
        for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
            done = False
            if toktype == tokenize.INDENT:
                indent = indent + 1
            if toktype == tokenize.DEDENT:
                indent = indent - 1
            if slineno > last_lineno:
                last_col = 0
            if not done and toktype == tokenize.NL:
                hasNL = True
                done = True
            if not done and toktype == tokenize.COMMENT:
                done = True
            if not done and toktype == tokenize.STRING and prev_toktype == tokenize.INDENT:
                done = True
            if not done and hasNL and toktype != tokenize.DEDENT and toktype != tokenize.INDENT:
                hasNL = False
                output = output + ("    " * indent) + '\n'
                output += "    " * indent
                prefixed = True
            if not done:
                if not prefixed and scol > last_col:
                    output += (" " * (scol - last_col))
                output += (ttext)
            prefixed = False
            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno
        return output

from HTMLParser import HTMLParser

class PMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataArray = []
        self.countLanguages = 0
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'script':
            for name, value in attrs:
                if name == 'src' and value == 'js/plugins.js':
                    self.countLanguages += 1
                    self.inLink = True
                    self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == "script":
            self.inlink = False

    def handle_data(self, data):
        if self.lasttag == 'script' and self.inLink and data.strip():
            print data


    def _python_interactive_indent(self, code):
        prev_toktype = tokenize.INDENT
        first_line = None
        last_lineno = -1
        last_col = 0

        output = ''

        tokgen = tokenize.generate_tokens(StringIO.StringIO(code).readline)
        indent = 0
        hasNL = False
        prefixed = False
        for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
            done = False
            if toktype == tokenize.INDENT:
                indent = indent + 1
            if toktype == tokenize.DEDENT:
                indent = indent - 1
            if slineno > last_lineno:
                last_col = 0
            if not done and toktype == tokenize.NL:
                hasNL = True
                done = True
            if not done and toktype == tokenize.COMMENT:
                done = True
            if not done and toktype == tokenize.STRING and prev_toktype == tokenize.INDENT:
                done = True
            if not done and hasNL and toktype != tokenize.DEDENT and toktype != tokenize.INDENT:
                hasNL = False
                output = output + ("    " * indent) + '\n'
                output += "    " * indent
                prefixed = True
            if not done:
                if not prefixed and scol > last_col:
                    output += (" " * (scol - last_col))
                output += (ttext)
            prefixed = False
            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno
        return output