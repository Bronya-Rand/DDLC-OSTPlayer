
init python:
    from store.ost_tracks import TRACK_LIST
    from store.ost_track_scanner import start_observer

    CURRENT_SONG = None

    renpy.music.register_channel("music_player", mixer="music_player_mixer", loop=False)

    class OSTPlayerControls():
        def __init__(self):
            self.paused = False
            self.muted = False
            self.pause_position = 0.0
            self.old_volume = 0.0

        def play(self, track):
            global CURRENT_SONG
            if track not in TRACK_LIST:
                return

            if track != CURRENT_SONG:
                CURRENT_SONG = track

            if self.paused:
                renpy.music.play(f"<from {str(self.pause_position)}>{track.path}", channel="music_player")
                self.paused = False
            else:
                renpy.music.play(f"{track.path}", channel="music_player")

        def pause(self):
            ## Return if nothing is playing
            if not renpy.audio.music.is_playing("music_player"):
                return

            self.paused = True
            self.pause_position = renpy.music.get_pos("music_player")
            renpy.music.stop("music_player")

        def next(self):
            global CURRENT_SONG
            self.paused = False

            ## Stop when at the end of the track list
            if TRACK_LIST.index(CURRENT_SONG) == len(TRACK_LIST) - 1:
                return
            
            CURRENT_SONG = TRACK_LIST[TRACK_LIST.index(CURRENT_SONG) + 1]
            self.play(CURRENT_SONG)

        def previous(self):
            global CURRENT_SONG
            self.paused = False

            ## Stop when at the beginning of the track list
            if TRACK_LIST.index(CURRENT_SONG) == 0:
                return
            
            CURRENT_SONG = TRACK_LIST[TRACK_LIST.index(CURRENT_SONG) - 1]
            self.play(CURRENT_SONG)
        
        def mute(self):
            self.old_volume = renpy.game.preferences.get_volume("music_player_mixer")
            renpy.game.preferences.set_volume("music_player_mixer", 0.0)
            self.muted = True

        def unmute(self):
            vol = self.old_volume
            if vol == 0.0:
                vol = 0.5

            renpy.game.preferences.set_volume("music_player_mixer", vol)
            self.muted = False
            ## Reset the old volume
            self.old_volume = 0.0
        
        def exit(self):
            if not renpy.music.is_playing(channel='music_player'):
                renpy.game.preferences.set_mute("music", False)
        
        def enter(self):
            renpy.game.preferences.set_mute("music", True)
        
    ost_player_controls = OSTPlayerControls()
    renpy.game.preferences.set_mute("music", False)
    start_observer()