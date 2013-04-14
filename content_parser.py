from __future__ import division
from xml.sax import make_parser, handler
from file_wrapper import FileWrapper

"""
Sample usage:

class TestHandler:
    def page(self, page, content):
        print page, content
    def finish(self): return

parser = DmozContentParser(DMOZ_CONTENT_FILE)
parser.add_handler(TestHandler())
parser.run()
"""

class DmozContentHandler(handler.ContentHandler):

    def __init__(self, handler):
        self._handler = handler
        self._current_page = ''
        self._capture_content = False
        self._current_content = {}
        self._capture_content_type = None
        self._expect_end = False

    def startElement(self, name, attrs):
        if name == 'ExternalPage':
            self._current_page = attrs['about']
            self._current_content = {}
        elif name in ['d:Title', 'd:Description', 'priority', 'topic']:
            self._capture_content = True
            self._capture_content_type = name

    def endElement(self, name):
        # Make sure that the only thing after "topic" is "/ExternalPage"
        if self._expect_end:
            assert name == 'topic' or name == 'ExternalPage'
            if name == 'ExternalPage':
                self._expect_end = False
                self._handler.page(self._current_page, self._current_content)
            self._capture_content_type = None
        if name == 'topic':
            self._expect_end = True
        self._capture_content = False

    def characters(self, content):
        if self._capture_content:
            self._current_content.setdefault(self._capture_content_type, '')
            self._current_content[self._capture_content_type] += content

    def endDocument(self):
        self._handler.finish()

class DmozContentParser:

    def __init__(self, file_path):
        self._file_path = file_path
        self._parser = make_parser()

    def run(self):
        self._parser.setContentHandler(DmozContentHandler(self._handler))
        if hasattr(self._file_path, 'read'):
            self._parser.parse(self._file_path)
        else:
            self._parser.parse(FileWrapper(self._file_path))

    def add_handler(self, handler):
        self._handler = handler
