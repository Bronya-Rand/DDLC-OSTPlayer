
image song_title = DynamicDisplayable(dynamic_title_func)
image song_artist = DynamicDisplayable(dynamic_artist_func)
image song_album = DynamicDisplayable(dynamic_album_func)
image song_cover = DynamicDisplayable(dynamic_cover_func)

image song_position = DynamicDisplayable(dynamic_position_func)
image song_duration = DynamicDisplayable(dynamic_duration_func)

define ost_channel_position_value = AudioPositionValue("music_player")

init python:
    from store.ost_tracks import OSTLocalTrack, TRACK_LIST
    import time

    def convert_time(x):
        '''
        Converts seconds to 'MM:SS' format.
        '''
        return time.strftime('%M:%S', time.gmtime(x))

    def listen_to(track):
        global CURRENT_SONG
        if CURRENT_SONG == track:
            ost_player_controls.pause()
        else:
            CURRENT_SONG = track
            ost_player_controls.play(track)

    def dynamic_title_func(st, at):
        return renpy.text.text.Text(
            text=CURRENT_SONG.metadata.title, substitute=False, size=18), 0.1
    
    def dynamic_artist_func(st, at):
        return renpy.text.text.Text(
            text=CURRENT_SONG.metadata.artist, substitute=False, size=16), 0.1
    
    def dynamic_album_func(st, at):
        return renpy.text.text.Text(
            text=CURRENT_SONG.metadata.album, substitute=False, size=16), 0.1
    
    def dynamic_cover_func(st, at):
        return renpy.display.im.image(CURRENT_SONG.metadata.album_cover), 0.1

    def dynamic_position_func(st, at):
        if renpy.music.get_pos("music_player") is None:
            pos = ost_player_controls.pause_position
        else:
            pos = renpy.music.get_pos("music_player")

        return renpy.text.text.Text(
            text=convert_time(pos), substitute=False, size=16), 0.1
    
    def dynamic_duration_func(st, at):
        duration = renpy.music.get_duration("music_player")
        return renpy.text.text.Text(
            text=convert_time(duration), substitute=False, size=16), 0.1

        
screen new_music_room():

    style_prefix "music_player"

    modal True

    frame:
        xsize 960
        ysize 600

        xalign 0.5
        yalign 0.5
        
        hbox:
            xfill True
            yfill True
            spacing 10

            ## Song Information
            vbox:
                xalign 0.5
                yalign 0.5
                xsize 430
                spacing 5

                vbox:
                    xalign 0.5
                    spacing 5
                        
                    if CURRENT_SONG:
                        ## Cover Art
                        add "song_cover" at cover_art_resize(250) xalign 0.5

                        ## Song Title
                        add "song_title" xalign 0.5

                        ## Song Artist
                        add "song_artist" xalign 0.5

                        ## Song Album
                        add "song_album" xalign 0.5

                        bar:
                            value ost_channel_position_value

                        hbox:
                            xalign 0.5
                            spacing 2

                            ## Song Position
                            add "song_position" 

                            text "/"

                            ## Song Duration
                            add "song_duration"
                        
                        hbox:
                            xalign 0.5
                            spacing 5

                            ## Previous Button
                            imagebutton:
                                idle "sdc/ost/assets/previous_idle.png"
                                hover "sdc/ost/assets/previous_hover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_player_controls.previous)]

                            ## Play/Pause Button
                            imagebutton:
                                idle If(ost_player_controls.paused, "sdc/ost/assets/pause.png", "sdc/ost/assets/play.png")
                                hover If(ost_player_controls.paused, "sdc/ost/assets/play.png", "sdc/ost/assets/pause.png")
                                action If(ost_player_controls.paused, Function(ost_player_controls.play, CURRENT_SONG), Function(ost_player_controls.pause))

                            ## Next Button
                            imagebutton:
                                idle "sdc/ost/assets/next_idle.png"
                                hover "sdc/ost/assets/next_hover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_player_controls.next)]
                        
                        hbox:
                            xalign 0.5
                            imagebutton:
                                idle If(renpy.game.preferences.get_volume("music_player_mixer") == 0.0, "sdc/ost/assets/mute_idle.png", "sdc/ost/assets/unmute_idle.png")
                                hover If(renpy.game.preferences.get_volume("music_player_mixer") == 0.0, "sdc/ost/assets/mute_hover.png", "sdc/ost/assets/unmute_hover.png")
                                action If(renpy.game.preferences.get_volume("music_player_mixer") == 0.0, Function(ost_player_controls.unmute), Function(ost_player_controls.mute))
                            
                            bar value Preference("music_player_mixer volume") xsize 100 yalign 0.5

                    else:
                        text "No song is currently playing."


            ## Track List
            vbox:
                textbutton "X" action [Function(ost_player_controls.exit), Hide()] xalign 1.0
                
                null height 5

                viewport id "track_list":
                    xfill True
                    yfill True
                    mousewheel True

                    has vbox

                    spacing 5

                    for track in TRACK_LIST:
                        python:
                            locked = isinstance(track, OSTLocalTrack) and track.locked

                        if not locked:
                            frame:
                                xsize 500
                                
                                button:
                                    ysize None
                                    action [Function(listen_to, track)]

                                    hbox:
                                        if CURRENT_SONG == track:
                                            add Transform(If(ost_player_controls.paused, "sdc/ost/assets/music_list_pause.png", "sdc/ost/assets/music_list_play.png"), size=(50, 50))
                                        else:
                                            if track.metadata.album_cover:
                                                add Transform(track.metadata.album_cover, size=(50, 50))
                                            else:
                                                add "sdc/ost/assets/unknown_album_cover.png"

                                        null width 10

                                        vbox:
                                            xsize 400
                                            text track.metadata.title substitute False
                                            text track.metadata.artist substitute False
                                            text track.metadata.album substitute False

transform cover_art_resize(x):
    xysize(x,x)