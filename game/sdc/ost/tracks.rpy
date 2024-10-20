
init -1 python in ost_tracks:
    from dataclasses import dataclass
    from typing import Optional
    from renpy import config
    import os
    import re

    ## Stores the default album title for local tracks
    DEFAULT_ALBUM_TITLE = config.name + " OST"

    ## Stores the default album cover for local tracks
    DEFAULT_ALBUM_COVER = "sdc/assets/ost_album_cover.png" if os.path.exists(os.path.join(config.gamedir, 'sdc/assets/album_cover.png')) else "sdc/ost/assets/unknown_album_cover.png"

    ## The track list
    TRACK_LIST = []

    @dataclass
    class OSTPlayerMetadata:
        '''
        Stores metadata for local tracks
        '''
        title: str
        artist: str
        album: str = DEFAULT_ALBUM_TITLE
        album_cover: str = DEFAULT_ALBUM_COVER
        album_artist: Optional[str] = None
        composer: Optional[str] = None
        genre: Optional[str] = None
        comment: Optional[str] = None
        

    class OSTTrack(object):
        '''
        Stores tracks to include to the OST Player.
        '''
        def __init__(self, path: str, metadata: OSTPlayerMetadata): 
            self.path = path
            self.metadata = metadata

            ## Adds the track to the track list
            TRACK_LIST.append(self)

    class OSTLocalTrack(OSTTrack):
        '''
        Stores local tracks to include to the OST Player.
        '''
        def __init__(self, path: str, metadata: OSTPlayerMetadata, locked: bool = False):
            ## Remove <from X.X> or <loop X.X> from the path
            sub = re.sub(r'<(from|loop) \d+\.\d+>', '', path)

            super().__init__(sub, metadata)
            self.ddlc_path = path
            self.locked = locked
        
        ## Returns the path of the track for Ren'Py's audio/music namespace with tags
        def __repr__(self):
            return self.ddlc_path

    def get_track_list():
        '''
        Returns the track list
        '''
        return TRACK_LIST

    def get_local_track_list():
        '''
        Returns the local track list
        '''
        return [track for track in TRACK_LIST if isinstance(track, OSTLocalTrack)]

    def get_sideloaded_track_list(name):
        '''
        Returns the sideloaded track list
        '''
        return [track for track in TRACK_LIST if not isinstance(track, OSTLocalTrack)]

    def sort_by_name(tracks):
        '''
        Sorts the tracks by name
        '''
        return sorted(tracks, key=lambda track: track.metadata.title)
