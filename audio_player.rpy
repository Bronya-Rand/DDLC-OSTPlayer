#init -1 default soundtracks = [your_reality, your_reality_2]
default current_soundtrack = False
default soundtrack_position = 0.0
default soundtrack_duration = 0.0
default time_position = 0.0 # Music Position (Temp Var)
default time_duration = 3.0 # Music Duration (Temp Var)
default audio.current_soundrack_pause = False
default music_was_muted_before_soundtrack_player_opened = False
define organizeAZ = False
define organizePriority = True
define loopSong = False
define priorityScan = 2
define ostVersion = "1.33"

init python:
    def music_pos(d, refresh):
        global time_position
        global time_duration

        if current_soundtrack == False: # failsafe to when user quits out of OST
            return Text("", style="music_player_description_text", size=40), 0.0

        if renpy.music.is_playing(channel='music_player'): # checks if music is playing
            time_position = renpy.music.get_pos(channel='music_player') or time_position # grabs position of song
        else:
            if time_position > time_duration - 0.20:
                time_position = 0.0

        readableTime = convert_time(time_position) # converts to readable time for display
        d = Text(readableTime, style="music_player_description_text") 
        return d, 0.20

    def music_dur(d, refresh):
        global time_duration

        if current_soundtrack == False: # failsafe to when user quits out of OST
            return Text("", style="music_player_description_text", size=40), 0.0

        if renpy.music.is_playing(channel='music_player'): # checks if music is playing
            time_duration = renpy.music.get_duration(channel='music_player') or time_duration # sets duration to what renpy thinks it lasts
        else:
            time_duration = time_duration

        readableDuration = convert_time(time_duration) # converts to readable time for display
        d = Text(readableDuration, style="music_player_description_text")     
        return d, 0.20

    def dynamic_title_text(d, refresh):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return Text("Exiting...", style="music_player_music_text", size=36), 0.0

        title = len(current_soundtrack.full_name) # grabs the length of the name and artist 

        if title <= 21: # checks length against set var checks (can be changed) 
            songNameSize = 37 # sets font size 32
        elif title <= 28:
            songNameSize = 29
        else:
            songNameSize = 23

        d = Text(current_soundtrack.full_name, style="music_player_music_text", size=songNameSize)
        return d, 0.20

    def dynamic_author_text(d, refresh):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return Text("", style="music_player_song_author_text", size=23), 0.0

        author = len(current_soundtrack.author)

        if author <= 32:
            authorNameSize = 25
        elif author <= 48:
            authorNameSize = 23
        else:
            authorNameSize = 21

        d = Text(current_soundtrack.author, style="music_player_song_author_text", size=authorNameSize)
        return d, 0.20

    def dynamic_description_text(d, refresh):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return Text("", style="music_player_song_author_text", size=23), 0.0

image readablePos = DynamicDisplayable(music_pos)
image readableDur = DynamicDisplayable(music_dur) 
image titleName = DynamicDisplayable(dynamic_title_text) 
image authorName = DynamicDisplayable(dynamic_author_text) 

label music_player:
    call screen music_player()
    hide screen music_player
    return

label exit_loop:
    $ renpy.music.stop(channel='music_player',fadeout=2.0)
    $ renpy.full_restart()

screen music_player:

    tag menu

    add "game_menu_bg"
    add "gui/overlay/main_menu.png"
    
    default bar_val = AdjustableAudioPositionValue()

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
                        action [SensitiveIf(current_soundtrack.name != st.name), SetVariable("current_soundtrack", st), Play("music_player", st.path, loop=loopSong)]
                    else:
                        action [SetVariable("current_soundtrack", st), Play("music_player", st.path, loop=loopSong)]

        vbar value YScrollValue("vpo") xpos 1.0 ypos 20

    if current_soundtrack:
        if current_soundtrack.cover_art:
            add current_soundtrack.cover_art at cover_art_fade(500, 300)

        hbox:
            style "play_pause_button_hbox"
            imagebutton:
                idle "mod_assets/music_player/backward.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_backward)]
            imagebutton:
                idle "mod_assets/music_player/play.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_play)]
            imagebutton:
                idle "mod_assets/music_player/pause.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_pause)]
            imagebutton:
                idle "mod_assets/music_player/forward.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_forward)]
        hbox:
            style "music_options_hbox"
            imagebutton:
                idle ConditionSwitch("organizeAZ", "mod_assets/music_player/A-ZOn.png", "True", "mod_assets/music_player/A-Z.png")
                action [ToggleVariable("organizeAZ", False, True), Function(resort)]
            imagebutton:
                idle ConditionSwitch("organizePriority", "mod_assets/music_player/priorityOn.png", "True", "mod_assets/music_player/priority.png")
                action [ToggleVariable("organizePriority", False, True), Function(resort)]
            imagebutton:
                idle "mod_assets/music_player/refreshList.png"
                action [Function(refresh_list)]
            imagebutton:
                idle ConditionSwitch("loopSong", "mod_assets/music_player/replayOn.png", "True", "mod_assets/music_player/replay.png")
                action [ToggleVariable("loopSong", False, True), Function(current_music_play)]
        
        bar:
            xsize 710
            value bar_val
            hovered bar_val.hovered
            unhovered bar_val.unhovered
            style "music_player_time_bar"

        #displaying name of current soundtrack and authon
        if current_soundtrack.author:
            vbox: # sets the vbox for the song name / artist name
                xoffset 700 # old pos but as offsets
                yoffset 220
                hbox: # adds a hbox to the area set
                    #box_wrap True # wraps text when full
                    vbox:
                        style_prefix "player" # sets prefix of style to a custom style called player
                        add "titleName"
                hbox:
                    vbox:
                        style_prefix "playerB" # another custom style to fit the vboxes 
                        if current_soundtrack:
                            add "authorName" xpos 6
        else:
            # same but for alternative formating
            vbox:
                xoffset 700 # old pos but as offsets
                yoffset 220
                hbox:
                    vbox:
                        style_prefix "player"
                        text "[current_soundtrack.full_name]" style "music_player_music_text" size title_size 

        #displaying description of current soundtrack
        if current_soundtrack.description:
            viewport id "desc":
                mousewheel True
                xpos 705
                ypos 320
                xsize 580
                xfill True
                #child_size (700, None)
                style "music_player_description_viewport"
                text "[current_soundtrack.description]" style "music_player_description_text"
            vbar value YScrollValue("desc") xpos 1250 ypos 470 ysize 200

        bar value Preference ("music_player_mixer volume") style "music_player_volume_bar"

        # displays the time elapsed of the soundtrack
        if current_soundtrack:
            add "readablePos" xpos 330 ypos 540
            add "readableDur" xpos 970 ypos 540
    
    #button returns to main menu
    textbutton "Main Menu":
        text_style "navigation_button_text"
        align (0.045,0.95)
        #hides the screen, unmutes music channel and stops music on music_player channel
        action [Hide("music_player"), If(music_was_muted_before_soundtrack_player_opened, true=None, false=SetMute("music", False)), Jump("exit_loop")]

    text "OST-Player v[ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

#transform for the cover art
transform cover_art_fade(x,y):
    anchor(0.5, 0.5)
    pos(x, y)
    size(350,350) # adjusts so any cover art is 350x350
    alpha 0
    linear 0.2 alpha 1

#play and pause button position
style play_pause_button_hbox:
    pos (710, 410)
    spacing 25

style music_options_hbox:
    pos (710, 450)
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
    xsize 580
    xfill True

style playerB_vbox: # controls artist formatting
    xsize 580
    xfill True

#style for the name of the music that appears when it is playing
style music_player_music_text:
    font "gui/font/RifficFree-Bold.ttf"
    color "#000"
    outlines [(0, "#000", 0, 0)]
    size 36
    ypos -5

#style for author of the music
style music_player_song_author_text:
    font "gui/font/Halogen.ttf"
    size 22
    outlines[]
    color "#000"

#style for viewport where description shows
style music_player_description_viewport:
    xsize 600
    ysize 200

#style for description text
style music_player_description_text:
    font "gui/font/Halogen.ttf"
    size 25
    outlines[]
    color "#000"

#the slider that indicates how far music is
style music_player_time_bar:
    xsize 400
    pos (325, 520)
    thumb "gui/slider/horizontal_hover_thumb.png"

#slider that controls player music sound
style music_player_volume_bar:
    xsize 120
    pos (1125, 520)
    thumb "gui/slider/horizontal_hover_thumb.png"

#style for the scrollable music list 
style music_player_viewport:
    xsize 210
    ysize 600

init python:
    from tinytag import TinyTag # imports Tinytag
    import os, glob, time, re, gc # imports other needed packages
    renpy.music.register_channel("music_player", mixer = "music_player_mixer", loop = False)
    
    # Converts the time to a readable time
    def convert_time(x):
        readableTime = time.gmtime(float(x))
        res = time.strftime("%M:%S",readableTime)
        return res

    #code that pauses music and changes audio.current_soundrack_pause with a starting point when the play button is clicked
    # This is unused but can be left here JIC
    def current_music_pause():
        global soundtrack_position
        global soundtrack_duration

        if renpy.music.get_pos(channel = 'music_player') is None:
            return

        soundtrack_position = renpy.music.get_pos(channel = 'music_player') + 1.6
        soundtrack_duration = renpy.music.get_duration(channel = 'music_player')

        if soundtrack_position is not None:
            audio.current_soundrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path # Reminiscent of Traditional Players

        renpy.music.stop(channel='music_player',fadeout=2.0)

    def current_music_play():
        global time_position

        if renpy.music.get_pos(channel = 'music_player') is not None:
            return

        if time_position == 0.0:
            if loopSong == True:
                audio.current_soundrack_pause = False
                renpy.music.play(current_soundtrack.path, channel = 'music_player', loop=True)
            else:
                audio.current_soundrack_pause = False
                renpy.music.play(current_soundtrack.path, channel = 'music_player', loop=False)
        else:
            if audio.current_soundrack_pause is not False:
                if loopSong == True:
                    renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=True)
                else:
                    renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=False)   
    
    def current_music_forward():
        global soundtrack_position
        global soundtrack_duration

        if renpy.music.get_pos(channel = 'music_player') is None:
            return

        soundtrack_position = renpy.music.get_pos(channel = 'music_player') + 5
        soundtrack_duration = renpy.music.get_duration(channel = 'music_player')

        if soundtrack_position > soundtrack_duration:
            soundtrack_position = soundtrack_duration

        audio.current_soundrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path

        if loopSong == True:
            renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=True)
        else:
            renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=False)

    def current_music_backward():
        global soundtrack_position

        if renpy.music.get_pos(channel = 'music_player') is None:
            return

        soundtrack_position = renpy.music.get_pos(channel = 'music_player') - 5

        if soundtrack_position < 0.0:
            soundtrack_position = 0.0

        audio.current_soundrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path
        
        if loopSong == True:
            renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=True)
        else:
            renpy.music.play(audio.current_soundrack_pause, channel = 'music_player', loop=False)

    @renpy.pure
    class AdjustableAudioPositionValue(BarValue):
        def __init__(self, channel='music_player', update_interval=0.0):
            self.channel = channel
            self.update_interval = update_interval
            self.adjustment = None
            self._hovered = False
            self.loopThis = loopSong

        def get_pos_duration(self):
            pos = renpy.music.get_pos(self.channel) or 0.0
            duration = renpy.music.get_duration(self.channel) or time_duration

            return pos, duration

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = ui.adjustment(value=pos, range=duration, changed=self.set_pos, adjustable=True)
            return self.adjustment

        def hovered(self):
            self._hovered = True

        def unhovered(self):
            self._hovered = False

        def set_pos(self, value):
            if (self._hovered and pygame_sdl2.mouse.get_pressed()[0]):
                if self.loopThis:
                    renpy.music.play("<from {}>".format(value) + current_soundtrack.path, self.channel, self.loopThis)
                else:
                    renpy.music.play("<from {}>".format(value) + current_soundtrack.path, self.channel)

            return

        def periodic(self, st):

            pos, duration = self.get_pos_duration()
            if pos and pos <= duration:
                self.adjustment.set_range(duration)
                self.adjustment.change(pos)
            if renpy.music.get_pos(self.channel) > renpy.music.get_duration(self.channel) - 0.20:
                if self.loopThis:
                    renpy.music.play(current_soundtrack.path, self.channel, self.loopThis)

            return self.update_interval
    
    class soundtrack:
        def __init__(self, name = "", full_name = "", path = "", priority = 2, author = False, time = False, description = False, cover_art = False):
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
            #description of soundtrack
            self.description = description
            #path to the cover art image
            if cover_art == False:
                self.cover_art = "mod_assets/music_player/nocover.png"
            else:
                self.cover_art = cover_art  
        
    # grabs info from the mp3/ogg (and cover if available)
    def get_info(path, tags):   
        try:
            image_data = tags.get_image()
            jpgregex = r"\\xFF\\xD8\\xFF"

            match = re.search(jpgregex, image_data) # searches the image data in the file for a JPG pattern
            if match:
                cover_formats=".jpg" # set image format to jpg
            else:
                cover_formats=".png" # set image format to png
            altAlbum = re.sub(r"\[|\]|/|:|\?",'', tags.album) # converts problematic symbols to nothing i.e Emotion [Deluxe] to Emotion Deluxe
                
            with open(gamedir + '/track/covers/' + altAlbum + cover_formats, 'wb') as f: # writes image data with proper extension to destination
                f.write(image_data)
            return tags.title, tags.artist, altAlbum, cover_formats, tags.album, tags.comment
        except TypeError:
            return tags.title, tags.artist, None, None, tags.album, tags.comment
    
    # makes a ogg class for all ogg files
    def def_ogg(title, artist, priority, altAlbum, cover_formats, y, album, comments):
        if title is None: # checks if the file has a title
            title = "Unknown OGG File " + str(y)
        if artist is None: # checks if the file has an artist 
            artist = "Unknown Artist"
        if cover_formats is None: # checks if it has a cover
            description = "Non-Metadata OGG"
            cover_formats = "mod_assets/music_player/nocover.png" # tells the class there is no cover art
        else:
            cover_formats = "track/covers/"+altAlbum+cover_formats # sets path of cover art made in a folder
            try:
                renpy.image_size(cover_formats)
            except:
                cover_formats = "mod_assets/music_player/nocover.png" # set to generic cover
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
            author = artist,
            path = path,
            priority = priorityScan,
            description = description,
            cover_art = cover_formats
        )

    def def_mp3(title, artist, path, priority, altAlbum, cover_formats, y, album, comment):
        if title is None: # checks if the file has a title
            title = "Unknown MP3 File " + str(y)
        if artist is None: #checks if the file has an artist 
            artist = "Unknown Artist"
        if cover_formats is None: # checks if it has a cover
            description = "Non-Metadata MP3"
            cover_formats = "mod_assets/music_player/nocover.png" # tells the class there is no cover art
        else:
            cover_formats = "track/covers/"+altAlbum+cover_formats # sets path of cover art made in a folder
            try:
                renpy.image_size(cover_formats)
            except:
                cover_formats = "mod_assets/music_player/nocover.png" # set to generic cover
        if album is not None: # checks if the file has a album name
            if comment is not None: # checks if the file has comments (replaces description)
                description = album + '\n' + comment # adds album and comments to the description
            else:
                description = album # sets just album to description
        else:
            description = None # says there is no description

        # makes the mp3 a class to be displayed/played
        playableMP3List[y] = soundtrack(
            name = title,
            full_name = title,
            author = artist,
            path = path,
            priority = priorityScan,
            description = description,
            cover_art = cover_formats
        )

    def scan_mp3():
        global mp3List, playableMP3List
        if glob.glob(gamedir + '/track/*.mp3'): # checks if a mp3 available in pointed directory
            if len(mp3List) != 0: # checks if not a empty array
                for x in reversed(range(len(playableMP3List))): # removes every song from the playableOggList section for rescan
                    playableMP3List.pop(x)
                mp3List = [gamedir + "/track\\" + x for x in os.listdir(gamedir + '/track') if x.endswith(".mp3")] # grabs all mp3s again
                playableMP3List = [gamedir + "/track\\" + x for x in os.listdir(gamedir + '/track') if x.endswith(".mp3")]
                mp3ListLengthA = len(playableMP3List) # grabs total found of the list mp3
                for y in range(mp3ListLengthA):
                    path = playableMP3List[y].replace("\\", "/") # changes path to be python path
                    tags = TinyTag.get(path, image=True) # opens the mp3 and reads the metadata | image=True allows TinyTag to read cover images from files
                    title, artist, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
                    def_mp3(title, artist, path, priorityScan, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the mp3
            else:
                mp3List = glob.glob(gamedir + '/track/*.mp3') # lists out all song paths in a array
                playableMP3List = glob.glob(gamedir + '/track/*.mp3')
                mp3ListLength = len(playableMP3List) # grabs total found of the list mp3
                for y in range(mp3ListLength):
                    path = playableMP3List[y].replace("\\", "/") # changes path to be python path
                    tags = TinyTag.get(path, image=True) # opens the mp3 and reads the metadata | image=True allows TinyTag to read cover images from files
                    title, artist, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
                    def_mp3(title, artist, path, priorityScan, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the mp3

    def scan_ogg():
        global oggList, playableOGGList
        if glob.glob(gamedir + '/track/*.ogg'): # checks if a ogg available in pointed directory
            if len(oggList) != 0: # checks if not a empty array
                for x in reversed(range(len(playableOGGList))): # removes every song from the playableMP3List section for rescan
                    playableOGGList.pop(x)
                oggList = [gamedir + "/track\\" + x for x in os.listdir(gamedir + '/track') if x.endswith(".ogg")] # grabs all oggs again
                playableOGGList = [gamedir + "/track\\" + x for x in os.listdir(gamedir + '/track') if x.endswith(".ogg")]
                oggListLengthA = len(playableOGGList) # grabs total found of the list ogg
                for y in range(oggListLengthA):
                    path = playableOGGList[y].replace("\\", "/") # changes path to be python path
                    tags = TinyTag.get(path, image=True) # opens the oggs and reads the metadata | image=True allows TinyTag to read cover images from files
                    title, artist, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
                    def_ogg(title, artist, path, priorityScan, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the ogg
            else:
                oggList = glob.glob(gamedir + '/track/*.ogg') # lists out all song paths in a array
                playableOGGList = glob.glob(gamedir + '/track/*.ogg')
                oggListLength = len(playableOGGList) # grabs total found of the list oggs
                for y in range(oggListLength):
                    path = playableOGGList[y].replace("\\", "/") # changes path to be python path
                    tags = TinyTag.get(path, image=True) # opens the ogg and reads the metadata | image=True allows TinyTag to read cover images from files
                    title, artist, altAlbum, cover_formats, album, comment = get_info(path, tags) # calls get_info() to obtain song info
                    def_ogg(title, artist, path, priorityScan, altAlbum, cover_formats, y, album, comment) # makes a class to play/display the ogg
    
    def resort():
        soundtracks = []
        global soundtracks
        #for obj in gc.get_objects():
        for obj in playableMP3List: # fuck garbage collection, we yanking it from these vars
            #if isinstance(obj, soundtrack):
            soundtracks.append(obj)
        for obj in playableOGGList:
            soundtracks.append(obj)
        for obj in manualDefineList:
            soundtracks.append(obj)
        if organizeAZ:
            soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.name)
        if organizePriority:
            soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.priority)

    def refresh_list():
        scan_mp3() # scans mp3
        scan_ogg() # scans ogg
        resort()

    gamedir = config.gamedir.replace('\\', '/')
    try:
        os.mkdir(gamedir + "/track")
    except:
        pass
    try:
        os.mkdir(gamedir + "/track/covers")
    except:
        pass
    renpyFileList = renpy.list_files(common=False)
    trackFileName = []
    trackFilePath = []
    mp3List = []
    oggList = []
    playableMP3List = []
    playableOGGList = []
    manualDefineList = []
    global manualDefineList

    invalidCharacters =r" - |'| "
    for contents in renpyFileList:
        if contents.startswith("track/"):
            if contents.endswith(".mp3") or contents.endswith(".ogg"):
                try: renpy.file(gamedir + "/" + contents)
                except: 
                    if re.search(invalidCharacters, contents):
                        temp = re.sub(invalidCharacters, "_", contents)
                    else:
                        temp = contents
                    trackFileName.append(temp)
                    trackFilePath.append(contents)
    
    # writes songs in a track folder inside a RPA to the track folder outside the rpa
    for tracks in range(len(trackFileName)):
        try: renpy.file(gamedir + "/" + trackFileName[tracks])
        except: open(gamedir + "/" + trackFileName[tracks], "wb").write(renpy.file(trackFilePath[tracks]).read())

    scan_mp3()

    scan_ogg()
    
    # template for soundtracks
    # this method still works. you can still set it manually like it if you mind.
    # however now you must include manualDefineList.append(variable) to add it properly for refreshing
    your_reality = soundtrack(
        name = "Your reality",
        full_name = "Your reality",
        path = "bgm/credits.ogg",
        priority = 1,
        author = "Monika",
        description = "I made mistakes, hurt you, hurt my friends. All I can do is hope you all forgive me.",
        cover_art = False
    )     
    manualDefineList.append(your_reality)
    
    Wake_Up_Unchanged = soundtrack(
        name = "Unchanged",
        full_name = "Wake up unchanged",
        path = "mod_assets/music_player/sample/Unchanged.ogg",
        priority = 0,
        author = "PabloLuaxerc#1719",
        description = "Sad soundtrack",
        cover_art = "mod_assets/music_player/cover/cover.png"
    )
    manualDefineList.append(Wake_Up_Unchanged)

    # adds instances of soundtrack class to soundtracks list
    resort()
