
screen ostplayer_list_ui(bar_val):

    if not ost_info.get_current_soundtrack():
                
        use ostplayer_list_idle_ui

    else:
        
        style_prefix "ostplayer_list"
        
        fixed:
            xpos 0.1

            hbox:
                yalign -0.25
                spacing 10

                add "coverArt" at cover_art_resize(200)

                null width 3

                vbox:
                    yalign 0.2

                    add "titleName"

                    add "authorName"

                    add "albumName"

                    null height 6

                    hbox:
                        spacing 10

                        imagebutton:
                            idle "mod_assets/music_player/backward.png"
                            hover "mod_assets/music_player/backwardHover.png"
                            action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.rewind_music)]

                        imagebutton:
                            idle If(ost_controls.pausedState, "mod_assets/music_player/pause.png", "mod_assets/music_player/play.png")
                            hover If(ost_controls.pausedState, "mod_assets/music_player/play.png", "mod_assets/music_player/pause.png")
                            action If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music))

                        imagebutton:
                            idle "mod_assets/music_player/forward.png"
                            hover "mod_assets/music_player/forwardHover.png"
                            action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.forward_music)]

                        null width 15

                        imagebutton:
                            idle ConditionSwitch("ost_controls.loopSong", "mod_assets/music_player/replayOn.png", 
                                "True", "mod_assets/music_player/replay.png")
                            hover "mod_assets/music_player/replayHover.png"
                            action [ToggleVariable("ost_controls.loopSong", False, True)]
                        imagebutton:
                            idle ConditionSwitch("ost_controls.randomSong", "mod_assets/music_player/shuffleOn.png", 
                                "True", "mod_assets/music_player/shuffle.png")
                            hover "mod_assets/music_player/shuffleHover.png"
                            action [ToggleVariable("ost_controls.randomSong", False, True)]
                        imagebutton:
                            idle "mod_assets/music_player/info.png"
                            hover "mod_assets/music_player/infoHover.png"
                            action [Show("music_info"), With(Dissolve(0.25))]
                        imagebutton:
                            idle "mod_assets/music_player/settings.png"
                            hover "mod_assets/music_player/settingsHover.png"
                            action [Show("music_settings"), With(Dissolve(0.25))]
                        imagebutton:
                            idle "mod_assets/music_player/refreshList.png"
                            hover "mod_assets/music_player/refreshHover.png"
                            action [Function(ost_song_assign.refresh_list)]

                        null width 15
                        
                        imagebutton:
                            idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                "mod_assets/music_player/volume.png", "True", 
                                "mod_assets/music_player/volumeOn.png")
                            hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                "mod_assets/music_player/volumeHover.png", "True", 
                                "mod_assets/music_player/volumeOnHover.png")
                            action [Function(ost_controls.mute_player)]
                            yoffset -8
                        bar value Preference ("music_player_mixer volume") xsize 100 yoffset 8 xoffset -15

                    hbox:
                        bar:
                            style "music_player_list_bar"

                            value bar_val
                            hovered bar_val.hovered
                            unhovered bar_val.unhovered

                    null height 2

                    hbox:
                        add "readablePos" 
                        add "readableDur" xpos 550
    
    fixed:
        xpos 0.035
        ypos 0.25

        vpgrid id "mpl":
            rows len(soundtracks)
            cols 1
            mousewheel True
            draggable True

            xsize 950
            ysize 380
            spacing 5

            for st in soundtracks:
                frame: 
                    xsize 900

                    button:
                        ysize None
                        action If(ost_info.get_current_soundtrack() == st, If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music)), [SetVariable("ost_controls.pausedState", False), Function(ost_info.set_current_soundtrack, st), Play("music_player", st.path, loop=ost_controls.loopSong, fadein=2.0)])
                        
                        hbox:
                            if ost_info.get_current_soundtrack() == st:
                                add Transform(If(ost_controls.pausedState, "mod_assets/music_player/music_list_pause.png", "mod_assets/music_player/music_list_play.png"), size=(68, 68))
                            else:
                                add Transform(st.cover_art, size=(68, 68))

                            null width 12

                            vbox:
                                xsize 770
                                if renpy.version_tuple == (6, 99, 12, 4, 2187) and renpy.android:
                                    text "{b}[st.name]{/b}" style "r6_android_list_title_text"
                                    text "[st.author]" style "r6_android_list_author_text"
                                    text "[st.album]"  style "r6_android_list_author_text"
                                else:
                                    text "{b}[st.name]{/b}" style "music_player_list_title_text"
                                    text "[st.author]" style "music_player_list_author_text"
                                    text "[st.album]"  style "music_player_list_author_text"
                            
                            if st.byteTime:
                                vbox:
                                    yalign 0.5
                                    xpos -20
                                    if renpy.version_tuple == (6, 99, 12, 4, 2187) and renpy.android:
                                        text ost_info.convert_time(st.byteTime) style "r6_android_list_author_text"
                                    else:
                                        text ost_info.convert_time(st.byteTime) style "music_player_list_author_text"

style ostplayer_list_bar is ostplayer_bar:
    xsize 680