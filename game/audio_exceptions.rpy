
python early:

    class UnknownImageFileType(Exception):
        def __str__(self):
            return "Unknown image filetype found in embeded music file."
