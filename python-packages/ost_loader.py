# modded loader.py to support peeking
import os
import renpy
import re

class AltSubFile(object):

    def __init__(self, fn, base, length, start):
        self.fn = fn

        self.f = None

        self.base = base
        self.offset = 0
        self.length = length
        self.start = start

        if not self.start:
            self.name = fn
        else:
            self.name = None

    def open(self):
        self.f = open(self.fn, "rb")
        self.f.seek(self.base)

    def __enter__(self):
        return self

    def __exit__(self, _type, value, tb):
        self.close()
        return False

    def read(self, length=None):

        if self.f is None:
            self.open()

        maxlength = self.length - self.offset

        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

        rv1 = self.start[self.offset:self.offset + length]
        length -= len(rv1)
        self.offset += len(rv1)

        if length:
            rv2 = self.f.read(length)
            self.offset += len(rv2)
        else:
            rv2 = ""

        return (rv1 + rv2)

    def readline(self, length=None):

        if self.f is None:
            self.open()

        maxlength = self.length - self.offset
        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

        # If we're in the start, then read the line ourselves.
        if self.offset < len(self.start):
            rv = ''

            while length:
                c = self.read(1)
                rv += c
                if c == '\n':
                    break
                length -= 1

            return rv

        # Otherwise, let the system read the line all at once.
        rv = self.f.readline(length)

        self.offset += len(rv)

        return rv

    def readlines(self, length=None):
        rv = [ ]

        while True:
            l = self.readline(length)

            if not l:
                break

            if length is not None:
                length -= len(l)
                if l < 0:
                    break

            rv.append(l)

        return rv

    def xreadlines(self):
        return self

    def __iter__(self):
        return self

    def __next__(self): # @ReservedAssignment
        rv = self.readline()

        if not rv:
            raise StopIteration()

        return rv

    next = __next__

    def flush(self):
        return

    def seek(self, offset, whence=0):

        if self.f is None:
            self.open()

        if whence == 0:
            offset = offset
        elif whence == 1:
            offset = self.offset + offset
        elif whence == 2:
            offset = self.length + offset

        if offset > self.length:
            offset = self.length

        self.offset = offset

        offset = offset - len(self.start)
        if offset < 0:
            offset = 0

        self.f.seek(offset + self.base)

    def peek(self, offset):
        return self.f.read()

    def tell(self):
        return self.offset

    def close(self):
        if self.f is not None:
            self.f.close()
            self.f = None

    def write(self, s):
        raise Exception("Write not supported by SubFile/AltSubFile")


open_file = open

if "RENPY_FORCE_SUBFILE" in os.environ:

    def open_file(name, mode):
        f = open(name, mode)

        f.seek(0, 2)
        length = f.tell()
        f.seek(0, 0)

        return AltSubFile(f, 0, length, '')


def get_prefixes(tl=True):
    """
    Returns a list of prefixes to search for files.
    """

    rv = [ ]

    if tl:
        language = renpy.game.preferences.language # @UndefinedVariable
    else:
        language = None

    for prefix in renpy.config.search_prefixes:

        if language is not None:
            rv.append(renpy.config.tl_directory + "/" + language + "/" + prefix)

        rv.append(prefix)

    return rv


def load(name, tl=True):

    if renpy.display.predict.predicting: # @UndefinedVariable
        if threading.current_thread().name == "MainThread":
            if not (renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False)):
                raise Exception("Refusing to open {} while predicting.".format(name))

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    name = re.sub(r'/+', '/', name).lstrip('/')

    for p in get_prefixes(tl):
        rv = renpy.loader.load_core(p + name)
        if rv is not None:
            return rv

    raise IOError("Couldn't find file '%s'." % name)
