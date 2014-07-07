#!/usr/bin/env python
from HTMLParser import HTMLParser
import tokenize

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


