
screen ostplayer_compact_ui(bar_val):

    if not ost_info.get_current_soundtrack():
                
        use ostplayer_compact_idle_ui

    else:

        style_prefix "ostplayer_compact"
    
        fixed:
            xpos 0.05
            ypos 0.08

            hbox:
                spacing 10
                
                add "coverArt" at cover_art_resize(350)

                null width 3

                vbox:
                    yalign 0.5

                    add "titleName" 

                    add "authorName" 

                    add "albumName" 
                    
                    null height 10

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

                    null height 15

                    hbox:
                        spacing 15

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
                            idle "mod_assets/music_player/musicwindow.png"
                            hover "mod_assets/music_player/musicwindowHover.png"
                            action [Show("music_list_type"), With(Dissolve(0.25))]
                        imagebutton:
                            idle "mod_assets/music_player/settings.png"
                            hover "mod_assets/music_player/settingsHover.png"
                            action [Show("music_settings"), With(Dissolve(0.25))]
                        imagebutton:
                            idle "mod_assets/music_player/refreshList.png"
                            hover "mod_assets/music_player/refreshHover.png"
                            action [Function(ost_song_assign.refresh_list)]

            hbox:
                yalign 0.75

                vbox:
                    hbox:
                        bar:
                            value bar_val
                            hovered bar_val.hovered
                            unhovered bar_val.unhovered

                    null height 2

                    hbox:
                        add "readablePos" 
                        add "readableDur" xpos 640
                
                imagebutton:
                    idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                        "mod_assets/music_player/volume.png", "True", 
                        "mod_assets/music_player/volumeOn.png")
                    hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                        "mod_assets/music_player/volumeHover.png", "True", 
                        "mod_assets/music_player/volumeOnHover.png")
                    action [Function(ost_controls.mute_player)]
                    yoffset -16 xoffset 10
                bar value Preference ("music_player_mixer volume") xsize 100 xoffset 10

style ostplayer_compact_bar is ostplayer_bar:
    xsize 710