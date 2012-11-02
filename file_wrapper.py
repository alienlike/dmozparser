import os

class FileWrapper(file):

    def __init__(self, name):
        self._name = name
        self._bytes = os.path.getsize(name)
        self._bytes_read = 0
        self._progress = 0
        print '0% complete'

        file.__init__(self, name)

    def read(self, size):

        self._bytes_read += size

        progress = int(self.progress())
        if self._progress < progress:
            print '%d%% complete' % progress
            self._progress = progress

        return file.read(self, size)

    def progress(self):
        return (self._bytes_read / self._bytes) * 100