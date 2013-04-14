from __future__ import division
from xml.sax import make_parser, handler
from file_wrapper import FileWrapper

"""
Sample usage:

class TestHandler:
    def topic(self, topic):
        print topic
    def finish(self): return

parser = DmozStructureParser(DMOZ_STRUCTURE_FILE)
parser.add_handler(TestHandler())
parser.run()
"""

class DmozStructureHandler(handler.ContentHandler):

    def __init__(self, handler):
        self._handler = handler
        self._topic = None
        self._tag = ''
        self._capture = False
        self._chars = ''

    def startElement(self, name, attrs):
        if name == 'Topic':
            # if tag is Topic, create a new topic dict
            self._topic = {'id': attrs['r:id']}
        elif self._topic is None:
            # if no topic has been started, return
            return
        elif name in ['d:Title', 'd:Description', 'catid', 'lastUpdate']:
            # if a topic has been started, start capturing data for any of the tags above
            self._capture = True
            self._tag = name

    def endElement(self, name):
        if name == 'Topic':
            # if the closing tag is Topic, hand off topic dict to the handler
            self._handler.topic(self._topic)
            self._topic = None
        elif self._capture:
            # if we were capturing topic data, stop capturing now
            self._topic[self._tag] = self._chars
            self._capture = False
            self._chars = ''
            self._tag = ''

    def characters(self, content):
        # append character data if we are currently capturing
        if self._capture:
            self._chars += content

    def endDocument(self):
        # be done
        self._handler.finish()

class DmozStructureParser:

    def __init__(self, file_path):
        self._file_path = file_path
        self._parser = make_parser()

    def run(self):
        self._parser.setContentHandler(DmozStructureHandler(self._handler))
        if hasattr(self._file_path, 'read'):
            self._parser.parse(self._file_path)
        else:
            self._parser.parse(FileWrapper(self._file_path))

    def add_handler(self, handler):
        self._handler = handler
