
## Main Player Styles
style music_player_label_text is navigation_button_text:
    #font "mod_assets/music_player/riffic-bold.ttf"
    color "#000"
    outlines [(0, "#000", 0, 0)]
    hover_outlines []
    insensitive_outlines []
    size 34

style music_player_text:
    font "mod_assets/music_player/NotoSansSC-Light.otf"
    size 22
    outlines[]
    color "#000"

style ostplayer_bar:
    thumb "gui/slider/horizontal_hover_thumb.png"

style music_player_list_bar is music_player_bar:
    xsize 600

transform music_player_transition:
    alpha(0.0)
    linear 0.5 alpha(1.0)

transform cover_art_resize(x):
    size(x, x)

## Song Progress Text

style song_progress_text:
    font "gui/font/Halogen.ttf"
    size 25
    outlines[]
    color "#000"
    xalign 0.28 
    yalign 0.78

style song_duration_text is song_progress_text:
    xalign 0.79 
    yalign 0.78

## List UI
style music_player_list_title_text is music_player_text:
    size 15
    bold True

style music_player_list_author_text is music_player_text:
    size 13

## R6 Backwards Compatibility
style renpy_generic_text:
    font "mod_assets/music_player/NotoSans-Regular.ttf"
    color "#000"
    outlines []

style music_player_info_text is renpy_generic_text:
    size 20
    bold False

style r6_android_song_author_text is renpy_generic_text

style r6_android_list_title_text is renpy_generic_text:
    size 15
    bold True

style r6_android_list_author_text is renpy_generic_text:
    size 14

style r6_android_music_player_info_text is renpy_generic_text:
    size 22

## Windows
style music_window_button_text is music_player_button_text:
    size 22

style music_window_text is renpy_generic_text:
    size 24
    bold False

style music_settings_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    #font "mod_assets/music_player/riffic-bold.ttf"
    size 22
    color "#fff"
    outlines [(4, text_outline_color, 0, 0), (2, text_outline_color, 2, 2)]

style music_player_generic_text is renpy_generic_text:
    size 24
    bold False

style music_list_button_text is navigation_button_text:
    size 22

style l_list:
    left_padding 5