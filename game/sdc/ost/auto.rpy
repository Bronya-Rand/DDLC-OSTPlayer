
init python in ost_track_scanner:
    from store.ost_tracks import OSTPlayerMetadata, OSTTrack, TRACK_LIST
    from renpy import config

    from tinytag import TinyTag
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import os
    import threading
    import re

    TRACK_FOLDER = os.path.join(config.gamedir, 'tracks')
    TRACK_FOLDER_PRESENT = os.path.exists(TRACK_FOLDER)

    def scan_tracks(file_path=None):
        '''
        Scans tracks present in the 'tracks' folder.
        '''
        global TRACK_LIST

        files_to_scan = []
        if file_path:
            if file_path.endswith(('.mp3', '.ogg', '.wav', '.opus')):
                ost_path = "/".join(file_path.split("/")[-2:])
                files_to_scan.append(ost_path)
        else:
            for root, _, files in os.walk(os.path.join(config.gamedir, 'tracks')):
                for file in files:
                    if file.endswith(('.mp3', '.ogg', '.wav', '.opus')):
                        files_to_scan.append(os.path.join('tracks', file))

        for file in files_to_scan:
            tag = TinyTag.get(os.path.join(config.gamedir, file), image=True)

            ## Get the cover art (if available)
            cover_art = tag.get_image()
            
            ## Get the album cover
            album_cover = cover_art if cover_art else "sdc/ost/assets/unknown_album_cover.png"

            renpy_cover_path = None

            ## Write the cover art to the 'covers' folder
            if cover_art:
                if not os.path.exists(os.path.join(config.gamedir, 'tracks/covers')):
                    os.makedirs(os.path.join(config.gamedir, 'tracks/covers'))

                ## Clean Album Title for problematic characters
                cleaned_album_title = re.sub(r'[\[\\/:*?"<>|\]]', '', tag.album)

                cover_art_path = None
                ## Determine the cover art type (JPEG, PNG)
                if cover_art.startswith(b'\xff\xd8\xff'): ## JPEG
                    cover_art_path = os.path.join(config.gamedir, 'tracks/covers', cleaned_album_title + ".jpg")
                    renpy_cover_path = os.path.join('tracks/covers', cleaned_album_title + ".jpg")
                elif cover_art.startswith(b'\x89PNG\r\n\x1a\n'): ## PNG
                    cover_art_path = os.path.join(config.gamedir, 'tracks/covers', cleaned_album_title + ".png")
                    renpy_cover_path = os.path.join('tracks/covers', cleaned_album_title + ".png")
                else:
                    pass
                
                ## Check if current cover art is correct or not saved
                if cover_art_path is not None:
                    write = False
                    if not os.path.exists(cover_art_path):
                        write = True
                    else:
                        with open(cover_art_path, 'rb') as f:
                            if f.read() != cover_art:
                                write = True
                    if write:
                        with open(cover_art_path, 'wb') as f:
                            f.write(cover_art)

            metadata = OSTPlayerMetadata(
                title = tag.title,
                artist = tag.artist,
                album = tag.album,
                album_cover = renpy_cover_path,
                album_artist = tag.albumartist,
                composer = tag.composer,
                genre = tag.genre,
                comment = tag.comment
            )

            # Remove any existing track with the same path to avoid duplicates
            TRACK_LIST[:] = [track for track in TRACK_LIST if track.path != file]

            OSTTrack(file, metadata)

    def remove_track(file_path):
        '''
        Removes a track from the TRACK_LIST based on the file path.
        '''
        global TRACK_LIST
        ost_path = "/".join(file_path.split("/")[-2:])
        TRACK_LIST[:] = [track for track in TRACK_LIST if track.path != ost_path]

    ## Periodically scan the tracks folder
    class TrackScanHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                scan_tracks(event.src_path)

        def on_created(self, event):
            if not event.is_directory:
                scan_tracks(event.src_path)

        def on_deleted(self, event):
            if not event.is_directory:
                remove_track(event.src_path)
        
    ## Start the track scanner
    def start_observer():
        global TRACK_FOLDER_PRESENT, TRACK_FOLDER

        ## Check if the 'tracks' folder exists again
        if not TRACK_FOLDER_PRESENT:
            TRACK_FOLDER_PRESENT = os.path.exists(TRACK_FOLDER)

        if TRACK_FOLDER_PRESENT:
            for root, dirs, files in os.walk(TRACK_FOLDER):
                if 'covers' in dirs:
                    dirs.remove('covers')
                
                if len(files) > 0:
                    event_handler = TrackScanHandler()
                    observer = Observer()
                    observer.schedule(event_handler, TRACK_FOLDER)
                    observer_thread = threading.Thread(target=observer.start)
                    observer_thread.daemon = True
                    observer_thread.start()
                    scan_tracks()
