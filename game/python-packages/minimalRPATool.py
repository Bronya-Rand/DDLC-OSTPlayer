
# Based off rpatool but only focused on reading RPAs 

import pickle
import codecs
import sys

if sys.version_info[0] >= 3:
    def _unicode(text):
        return text

    def _printable(text):
        return text

    def _unmangle(data):
        return data.encode('latin1')

    def _unpickle(data):
        # Specify latin1 encoding to prevent raw byte values from causing an ASCII decode error.
        return pickle.loads(data, encoding='latin1')
elif sys.version_info[0] == 2:
    def _unicode(text):
        if isinstance(text, unicode):
            return text
        return text.decode('utf-8')

    def _printable(text):
        return text.encode('utf-8')

    def _unmangle(data):
        return data

    def _unpickle(data):
        return pickle.loads(data)

class RenPyArchive():

    file = None
    handle = None

    files = {}
    indexes = {}

    version = None
    padlength = 0
    key = None
    verbose = False

    RPA2_MAGIC = 'RPA-2.0 '
    RPA3_MAGIC = 'RPA-3.0 '
    RPA3_2_MAGIC = 'RPA-3.2 '

    # For backward compatibility, otherwise Python3-packed archives won't be read by Python2
    PICKLE_PROTOCOL = 2

    def __init__(self, file = None, version = 3, padlength = 0, key = 0xDEADBEEF, verbose = False):
        self.padlength = padlength
        self.key = key
        self.verbose = verbose

        if file is not None:
            self.load(file)
        else:
            self.version = version

    def __del__(self):
        if self.handle is not None:
            self.handle.close()

    def get_version(self):
        self.handle.seek(0)
        magic = self.handle.readline().decode('utf-8')

        if magic.startswith(self.RPA3_2_MAGIC):
            return 3.2
        elif magic.startswith(self.RPA3_MAGIC):
            return 3
        elif magic.startswith(self.RPA2_MAGIC):
            return 2
        elif self.file.endswith('.rpi'):
            return 1

        raise ValueError('the given file is not a valid Ren\'Py archive, or an unsupported version')

    # Load archive.
    def load(self, filename):
        filename = _unicode(filename)

        if self.handle is not None:
            self.handle.close()
        self.file = filename
        self.files = {}
        self.handle = open(self.file, 'rb')
        self.version = self.get_version()
        self.indexes = self.extract_indexes()

    def extract_indexes(self):
        self.handle.seek(0)
        indexes = None

        if self.version in [2, 3, 3.2]:
            # Fetch metadata.
            metadata = self.handle.readline()
            vals = metadata.split()
            offset = int(vals[1], 16)
            if self.version == 3:
                self.key = 0
                for subkey in vals[2:]:
                    self.key ^= int(subkey, 16)
            elif self.version == 3.2:
                self.key = 0
                for subkey in vals[3:]:
                    self.key ^= int(subkey, 16)

            # Load in indexes.
            self.handle.seek(offset)
            contents = codecs.decode(self.handle.read(), 'zlib')
            indexes = _unpickle(contents)

            # Deobfuscate indexes.
            if self.version in [3, 3.2]:
                obfuscated_indexes = indexes
                indexes = {}
                for i in obfuscated_indexes.keys():
                    if len(obfuscated_indexes[i][0]) == 2:
                        indexes[i] = [ (offset ^ self.key, length ^ self.key) for offset, length in obfuscated_indexes[i] ]
                    else:
                        indexes[i] = [ (offset ^ self.key, length ^ self.key, prefix) for offset, length, prefix in obfuscated_indexes[i] ]
        else:
            indexes = pickle.loads(codecs.decode(self.handle.read(), 'zlib'))

        return indexes

# List files in archive and current internal storage.
    def list(self):
        return list(self.indexes.keys()) + list(self.files.keys())