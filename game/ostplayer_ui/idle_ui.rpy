
screen ostplayer_compact_idle_ui():

    style_prefix "ost_idle"

    fixed:
        xpos 0.35
        ypos 0.35

        vbox:

            text "No music is currently playing."

            hbox:
                xalign 0.5
                textbutton "Music List":
                    action [Show("music_list_type"), With(Dissolve(0.25))]
                        
                textbutton "Settings":
                    action [Show("music_settings"), With(Dissolve(0.25))]

screen ostplayer_list_idle_ui():

    style_prefix "ost_idle"

    fixed:
        xpos 0.35

        vbox:
            text "No music is currently playing."

            hbox:
                xalign 0.5

                textbutton "Settings":
                    action [Show("music_settings"), With(Dissolve(0.25))]

style ost_idle_text is music_player_text:
    size 24

style ost_idle_button_text is navigation_button_text