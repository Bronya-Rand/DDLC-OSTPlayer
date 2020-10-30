#init -1 default soundtracks = [your_reality, your_reality_2]
default current_soundtrack = False
default soundtrack_time = False
default soundtrack_position = 0.0
default soundtrack_duration = 0.0
default time_position = 0.0 # Temp Position
default time_duration = 3.0 # Temp Duration
default title_size = 40 # Default Font Size
default title_offset = 15 # Default Font Y Position 
default author_size = 25 
default audio.current_soundrack_pause = False
default music_was_muted_before_soundtrack_player_opened = False
define organizeAZ = False
define organizePriority = True
define priorityScan = 2

label music_player:
    call screen music_player()
    hide screen music_player
    jump time_loop # loops a process for the time duration/elapsed and font scaler

# Loops time position and font sizes each 1/3rd sec of the song at play
label time_loop:
    python:
        if renpy.music.is_playing(channel='music_player'): # checks if music is playing
            if renpy.music.get_pos(channel='music_player') is None: # gets position of song
                time_position = time_position # saves position to default or set position
                time_duration = time_duration # saves duration to default or music time
            else:
                time_position = renpy.music.get_pos(channel='music_player') # grabs position of song
                if current_soundtrack.byteTime: # attempts to read time from the song file
                    time_duration = current_soundtrack.byteTime # sets duration to the song duration
                else:
                    time_duration = renpy.music.get_duration(channel='music_player') # sets duration to what renpy thinks it lasts
                    
            readableTime = convert_time(time_position) #converts to readable time for display
            readableDuration = convert_time(time_duration)
        else:
            if time_position > time_duration - 2.0:
                time_position = 0.0
                time_duration = time_duration
            else:
                time_position = time_position # sets everything to default or saved values
                time_duration = time_duration
            readableTime = convert_time(time_position) # converts to readable time for display
            readableDuration = convert_time(time_duration)
        title = len(current_soundtrack.full_name) # grabs the length of the name and artist 
        author = len(current_soundtrack.author)
        if title <= 28: # checks length against set var checks (can be changed) 
            title_size = 40 # sets font size
            title_offset = 12 # sets offset of text to be almost flush with title
        else:
            title_size = 26
            title_offset = 8
        if author <= 32:
            author_size = 25
        elif author <= 48:
            author_size = 23
        else:
            author_size = 21
        if time_position == 0.0:
            audio.current_soundrack_pause = current_soundtrack.path
        renpy.pause(int(0.20)) # stops the loop for 1/3rd second
    jump time_loop #re-calls var

label exit_loop:
    $ renpy.music.stop(channel='music_player',fadeout=2.0)
    $ renpy.full_restart()

screen music_player:
    add "game_menu_bg"
    add "gui/overlay/main_menu.png"
    side "c l":
        
        viewport id "vpo":
            style "music_player_viewport"
            mousewheel True

            child_size (210, 600)

            xpos 20
            ypos 20

            has vbox    
            spacing gui.navigation_spacing
            #lists textbuttons with names of soundtracks
            for st in soundtracks:
                textbutton "[st.name]":
                    style "l_list" # style responsible for listing songs to the left hand side
                    text_style "navigation_button_text"
                    if current_soundtrack:
                        action [SensitiveIf(current_soundtrack.name != st.name), SetVariable("current_soundtrack", st), Play("music_player", st.path), Jump("time_loop")]
                    else:
                        action [SetVariable("current_soundtrack", st), Play("music_player", st.path), Jump("time_loop")]


        vbar value YScrollValue("vpo") xpos 1.0 ypos 20

    if current_soundtrack:
        if current_soundtrack.cover_art:
            add current_soundtrack.cover_art at cover_art_fade (500, 200)


        hbox:
            style "play_pause_button_hbox"
#            imagebutton:
#                idle "mod_assets/music_player/backward.png"
#                action [Function(current_music_forward(-15.0)), Play("music_player", audio.current_soundrack_pause, selected = True)]
            imagebutton:
                idle "mod_assets/music_player/play.png"
                action [SensitiveIf(renpy.music.is_playing(channel = 'music_player') == False), Play("music_player", audio.current_soundrack_pause, selected = True, fadein=2.0), Jump("time_loop")]
            imagebutton:
                idle "mod_assets/music_player/pause.png"
                action [SensitiveIf(renpy.music.is_playing(channel = 'music_player')), Function(current_music_pause)]
#             imagebutton:
#                 idle "mod_assets/music_player/forward.png"
#                 action [Function(current_music_forward(15.0)), Play("music_player", audio.current_soundrack_pause, selected = True)]

        #if renpy.music.is_playing(channel = 'music_player'):
            #bar value AudioPositionValue(channel=u'music_player', update_interval=0.01) style "music_player_time_bar"
        #else:
            #bar value StaticValue(value = soundtrack_position, range = soundtrack_duration) style "music_player_time_bar"

        bar value StaticValue(value = time_position, range = time_duration) style "music_player_time_bar" # new time bar responsible for progress

        #displaying name of current soundtrack and authon
        if current_soundtrack.author:
            vbox: # sets the vbox for the song name / artist name
                xoffset 330 # old pos but as offsets
                yoffset 390
                hbox: # adds a hbox to the area set
                    box_wrap True # wraps text when full
                    vbox:
                        style_prefix "player" # sets prefix of style to a custom style called player
                        #pos (330, 390)

                        text "[current_soundtrack.full_name]" style "music_player_music_text" size title_size # displays song name but with scaler
                    vbox:
                        style_prefix "playerB" # another custom style to fit the vboxes 
                        text "[current_soundtrack.author]" style "music_player_song_author_text" xpos 12 size author_size yoffset title_offset #displays artist with different pos and scaler
        else:
            # same but for alternative formating
            vbox:
                xoffset 330
                yoffset 390
                hbox:
                    box_wrap True
                    vbox:
                        style_prefix "player"
                        text "[current_soundtrack.full_name]" style "music_player_music_text" size title_size 

        #displaying description of current soundtrack
        if current_soundtrack.description:
            viewport id "desc":
                mousewheel True
                xpos 510
                ypos 520
                child_size (700, None)
                style "music_player_description_viewport"
                text "[current_soundtrack.description]" style "music_player_description_text"
            vbar value YScrollValue("desc") xpos 1250 ypos 470 ysize 200

        bar value Preference ("music_player_mixer volume") style "music_player_volume_bar"

        # displays the time elapsed of the soundtrack
        text "[readableTime]" style "music_player_description_text" xpos 510 ypos 480
        text "([readableDuration])" style "music_player_description_text" xpos 590 ypos 480
        
        ## Debugging Code for time positions
        # text "Current: [time_position]" style "music_player_description_text" xpos 590 ypos 620
        # text "Total: [time_duration]" style "music_player_description_text" xpos 590 ypos 660
        # text "File Time Registers: [readableDuration]" style "music_player_description_text" xpos 860 ypos 630

    #button returns to main menu
    textbutton "Main Menu":
        text_style "navigation_button_text"
        align (0.045,0.95)
        #hides the screen, unmutes music channel and stops music on music_player channel
        action [Hide("music_player"), If(music_was_muted_before_soundtrack_player_opened, true=None, false=SetMute("music", False)), Jump("exit_loop")]

#transform for the cover art
transform cover_art_fade(x,y):
    anchor(0.5, 0.5)
    pos(x, y)
    size(350,350) # adjusts so any cover art is 350x350
    alpha 0
    linear 0.2 alpha 1

#play and pause button position
style play_pause_button_hbox:
    pos (335, 520)
    spacing 25

style l_default: # default responsible for other l_ info
    font gui.default_font
    size 18
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

style l_list is l_default: # controls list formatting
    left_padding 20
    size 16
    xfill True

style player_vbox: # controls title formatting
    xsize 500

style playerB_vbox: # controls artist formatting
    xsize 430

#style for the name of the music that appears when it is playing
style music_player_music_text:
    font "gui/font/RifficFree-Bold.ttf"
    color "#000"
    outlines [(0, "#000", 0, 0)]
    size 40

#style for author of the music
style music_player_song_author_text is music_player_description_text
style music_player_song_author_text:
    yoffset 15

#style for viewport where description shows
style music_player_description_viewport:
    xsize 700
    ysize 200

#style for description text
style music_player_description_text:
    font "gui/font/Halogen.ttf"
    size 25
    outlines[]
    color "#000"

#the slider that indicates how far music is
style music_player_time_bar:
    xsize 900
    pos (320, 460)
    thumb "gui/slider/horizontal_hover_thumb.png"

#slider that controls player music sound
style music_player_volume_bar:
    xsize 150
    pos (323, 490)
    thumb "gui/slider/horizontal_hover_thumb.png"

#style for the scrollable music list 
style music_player_viewport:
    xsize 210
    ysize 600

init python:
    from tinytag import TinyTag # imports Tinytag
    import os, glob, time, re # imports other needed packages
    renpy.music.register_channel("music_player", mixer = "music_player_mixer", loop = False)

    # Converts the time to a readable time
    def convert_time(x):
        readableTime = time.gmtime(float(x))
        res = time.strftime("%M:%S",readableTime)
        return res

    #code that pauses music and changes audio.current_soundrack_pause with a starting point when the play button is clicked
    # This is unused but can be left here JIC
    def current_music_pause(time_offset = 0.0):
        global soundtrack_position
        global soundtrack_duration
        global time_position
        soundtrack_position = renpy.music.get_pos(channel = 'music_player') + 1.6
        soundtrack_duration = renpy.music.get_duration(channel = 'music_player')
        if soundtrack_position is not None:
            audio.current_soundrack_pause = "<from "+str(soundtrack_position + time_offset) +">"+current_soundtrack.path # Reminiscent of Traditional Players
        else:
            pass
        renpy.music.stop(channel='music_player',fadeout=2.0)
#            audio.current_soundrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path

    #function that shows the screen
    def open_music_player():
        global current_soundtrack
        #renpy.show_screen("music_player")
        current_soundtrack = False      
    
#    def current_music_forward(time_offset):
#        if renpy.music.is_playing(channel = 'music_player'):
#            current_music_pause(time_offset = time_offset)
#            if soundtrack_position is not None:
#                renpy.music.play(audio.current_soundrack_pause, channel = 'music_player')
#        else:
#            global soundtrack_position
#            if soundtrack_position is not None:
#                soundtrack_position = soundtrack_position + time_offset
#                audio.current_soundrack_pause = "<from "+str(soundtrack_position + time_offset) +">"+current_soundtrack.path
#            else:
#                pass
#                audio.current_soundrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path

    class soundtrack:
        def __init__(self, name = "", full_name = "", path = "", priority = 2, author = False, time = False, byteTime = False, description = False, cover_art = False):
            #name that will be displayed
            self.name = name
            #name that will be displayed in 
            self.full_name = full_name
            #path to the music file
            self.path = path
            #priority of the list
            self.priority = priority
            #author names
            self.author = author
            # time duration of the song
            self.time = time
            # byte time duration of song
            self.byteTime = byteTime
            #description of soundtrack
            self.description = description
            #path to the cover art image
            self.cover_art = cover_art  
        
    # grabs info from the mp3/ogg (and cover if available)
    def get_info(path, tags):
        sec = tags.duration # takes the duration and converts to a 2 decimal float
        res = convert_time(sec) # converts duration to readable time       
        try:
            image_data = tags.get_image()
            jpgregex = r"\\xFF\\xD8\\xFF"

            match = re.search(jpgregex, image_data) # searches the image data in the file for a JPG pattern
            if match:
                cover_formats=".jpg" # set image format to jpg
            else:
                cover_formats=".png" # set image format to png
            altAlbum = re.sub(r"(\[|\])",'', tags.album) # converts problematic symbols to nothing i.e Emotion [Deluxe] to Emotion Deluxe
                
            with open(config.gamedir + '/track/' + altAlbum + cover_formats, 'wb') as f: # writes image data with proper extension to destination
                f.write(image_data)
            return tags.title, tags.artist, res, sec, altAlbum, cover_formats, tags.album, tags.comment
        except TypeError:
            pass
            return tags.title, tags.artist, res, sec, None, None, tags.album, tags.comment
    
    # makes a ogg class for all ogg files
    def def_ogg(title, artist, priority, res, sec, altAlbum, cover_formats, y, album, comments):
        if title is None: # checks if the file has a title
            title = "Unknown OGG File " + str(y)
        if artist is None: # checks if the file has an artist 
            artist = "Unknown Artist"
        if cover_formats is None: # checks if it has a cover
            description = "Non-Metadata OGG"
            cover_formats = False # tells the class there is no cover art
        else:
            cover_formats = 'track/'+altAlbum+cover_formats # sets path of cover art made in a folder
        if album is not None: # checks if the file has a album name
            if comment is not None: # checks if the file has comments (replaces description)
                description = album + '\n' + comment # adds album and comments to the description
            else:
                description = album # sets just album to description
        else:
            description = None # says there is no description
        
        # makes the ogg a class to be displayed/played
        oggList[y] = soundtrack(
            name = title,
            full_name = title,
            path = path,
            time = res,
            priority = priorityScan,
            byteTime = sec,
            author = artist,
            description = description,
            cover_art = cover_formats
        )

    def def_mp3(title, artist, priority, res, sec, altAlbum, cover_formats, y, album, comment):
        if title is None: # checks if the file has a title
            title = "Unknown MP3 File " + str(y)
        if artist is None: #checks if the file has an artist 
            artist = "Unknown Artist"
        if cover_formats is None: # checks if it has a cover
            description = "Non-Metadata MP3"
            cover_formats = False # tells the class there is no cover art
        else:
            cover_formats = 'track/'+altAlbum+cover_formats # sets path of cover art made in a folder
        if album is not None: # checks if the file has a album name
            if comment is not None: # checks if the file has comments (replaces description)
                description = album + '\n' + comment # adds album and comments to the description
            else:
                description = album # sets just album to description
        else:
            description = None # says there is no description

        # makes the mp3 a class to be displayed/played
        mp3List[y] = soundtrack(
            name = title,
            full_name = title,
            path = path,
            author = artist,
            time = res,
            priority = priorityScan,
            byteTime = sec,
            description = description,
            cover_art = cover_formats
        )       

    # checks if a mp3 available in pointed directory
    if glob.glob(config.gamedir + '/track/*.mp3'):
        mp3List = glob.glob(config.gamedir + '/track/*.mp3') # lists out all songs in mp3
        mp3ListLength = len(mp3List) # grabs total found of the list mp3
        for y in range(mp3ListLength):
            path = mp3List[y].replace("\\", "/") # changes path to be python path
            tags = TinyTag.get(path, image=True) # opens the mp3 and reads the metadata | image=True allows TinyTag to read cover images from files
            title, artist, res, sec, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
            def_mp3(title, artist, priorityScan, res, sec, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the mp3

    # checks if a ogg available in pointed directory
    if glob.glob(config.gamedir + '/track/*.ogg'):
        oggList = glob.glob(config.gamedir + '/track/*.ogg') # lists out all songs in ogg
        oggListLength = len(oggList) # grabs total found of the list ogg
        for y in range(oggListLength):
            path = oggList[y].replace("\\", "/") # changes path to be python path
            tags = TinyTag.get(path, image=True) # opens the ogg and reads the metadata | image=True allows TinyTag to read cover images from files
            title, artist, res, sec, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
            def_ogg(title, artist, priorityScan, res, sec, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the ogg

    # template for soundtracks
    # this method still works. you can still set it manually like it if you mind.
    your_reality = soundtrack(
        name = "Your reality",
        full_name = "Your reality",
        path = "bgm/credits.ogg",
        priority = 1,
        author = "Monika",
        description = "I made mistakes, hurt you, hurt my friends. All I can do is hope you all forgive me.",
        cover_art = False
    )     
    
    Wake_Up_Unchanged = soundtrack(
        name = "Unchanged",
        full_name = "Wake up unchanged",
        path = "mod_assets/music_player/sample/Unchanged.ogg",
        priority = 0,
        author = "PabloLuaxerc#1719",
        description = "Sad soundtrack",
        cover_art = "mod_assets/music_player/cover/cover.png"
    )

    
    # adds instances of soundtrack class to soundtracks list
    soundtracks = []
    import gc
    for obj in gc.get_objects():
        if isinstance(obj, soundtrack):
            global soundtracks
            soundtracks.append(obj)
    if organizeAZ:
        soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.name)
    if organizePriority:
        soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.priority)

