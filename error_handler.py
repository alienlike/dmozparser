from xml.sax import ErrorHandler
import os

class SaxErrorHandler(ErrorHandler):

    def error(self, exception):
        ln = exception.getLineNumber()
        cn = exception.getColumnNumber()
        print 'error at line %s, column %s' % (ln, cn)

    def fatalError(self, exception):
        ln = exception.getLineNumber()
        cn = exception.getColumnNumber()
        print 'fatal error at line %s, column %s' % (ln, cn)

    def warning(self, exception):
        ln = exception.getLineNumber()
        cn = exception.getColumnNumber()
        print 'warning at line %s, column %s' % (ln, cn)
