
import renpy
import ost_loader

renpy.loader.SubFile = ost_loader.AltSubFile

def file(fn):
    return ost_loader.load(fn)