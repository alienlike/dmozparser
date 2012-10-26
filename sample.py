#!/usr/bin/env python

from parser import DmozParser

DMOZ_FILE = '../content.rdf.u8'

class TestHandler:
    def page(self, page, content):
        print page, content
    def finish(self): return

parser = DmozParser(DMOZ_FILE)
parser.add_handler(TestHandler())
parser.run()
