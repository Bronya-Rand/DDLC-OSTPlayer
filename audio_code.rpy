
# Based off ost.py from Renpy-Universal-Player but Ren'Py 6 compatible

init python:
    import time, random, re, glob, os, json
    import pygame_sdl2
    from tinytag import TinyTag

    # Creation of Music Room and Code Setup
    ostVersion = 2.0
    renpy.audio.music.register_channel("music_player", mixer="music_player_mixer", loop=False)
    if renpy.windows:
        gamedir = renpy.config.gamedir.replace("\\", "/")
    elif renpy.android:
        try: os.mkdir(os.path.join(os.environ["ANDROID_PUBLIC"], "game"))
        except: pass
        gamedir = os.path.join(os.environ["ANDROID_PUBLIC"], "game")
    else:
        gamedir = renpy.config.gamedir


    # Lists for holding media types
    songList = []
    manualDefineList = []
    soundtracks = []
    file_types = ['.mp3', '.ogg', '.opus', '.wav']

    # Stores soundtrack in progress
    current_soundtrack = False

    # Stores positions of track/volume/default priority
    time_position = 0.0 
    time_duration = 3.0
    old_volume = 0.0
    priorityScan = 2

    # Stores paused track/player controls
    current_soundtrack_pause = False
    prevTrack = False
    randomSong = False
    loopSong = False
    organizeAZ = False
    organizePriority = True
    pausedstate = False

    random.seed()

    class soundtrack:
        def __init__(self, name="", path="", priority=2, author="", byteTime=False, description="", cover_art=False, unlocked=True):
            #name that will be displayed
            self.name = name
            #path to the music file
            self.path = path
            #priority of the list
            self.priority = priority
            #author names
            self.author = author
            # byte time duration of song (backup for some songs)
            self.byteTime = byteTime
            #description of soundtrack
            self.description = description
            #path to the cover art image
            if cover_art == False:
                self.cover_art = "mod_assets/music_player/nocover.png"
            else:
                self.cover_art = cover_art
            self.unlocked = unlocked

    # Adjustable Bar for track scrolling
    @renpy.exports.pure
    class AdjustableAudioPositionValue(renpy.ui.BarValue):
        def __init__(self, channel='music_player', update_interval=0.0):
            self.channel = channel
            self.update_interval = update_interval
            self.adjustment = None
            self._hovered = False

        def get_pos_duration(self):
                
            pos = renpy.audio.music.get_pos(self.channel) or 0.0
            duration = renpy.audio.music.get_duration(self.channel) or time_duration
            if current_soundtrack.byteTime:
                duration = current_soundtrack.byteTime

            return pos, duration

        def get_song_options_status(self):
            return loopSong, randomSong

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = renpy.ui.adjustment(value=pos, range=duration, changed=self.set_pos, adjustable=True)
            return self.adjustment

        def hovered(self):
            self._hovered = True

        def unhovered(self):
            self._hovered = False

        def set_pos(self, value):
            loopThis = self.get_song_options_status()
            if (self._hovered and pygame_sdl2.mouse.get_pressed()[0]):
                renpy.audio.music.play("<from {}>".format(value) + current_soundtrack.path, self.channel)
                if loopThis:
                    renpy.audio.music.queue(current_soundtrack.path, self.channel, loop=True)

        def periodic(self, st):

            pos, duration = self.get_pos_duration()
            loopThis, doRandom = self.get_song_options_status()
            if pos and pos <= duration:
                self.adjustment.set_range(duration)
                self.adjustment.change(pos)
                        
            if pos > duration - 0.20:
                if loopThis:
                    renpy.audio.music.play(current_soundtrack.path, self.channel, loop=True)
                elif doRandom:
                    random_song()
                else:
                    next_track()

            return self.update_interval 

    def music_pos(style_name, st, at):
        global time_position
        global time_duration

        if current_soundtrack == False: # failsafe to when user quits out of OST
            return renpy.text.text.Text("", style=style_name, size=40), 0.0

        if renpy.audio.music.is_playing(channel='music_player'): # checks if music is playing
            time_position = renpy.audio.music.get_pos(channel='music_player') or time_position # grabs position of song
        else:
            if time_position > time_duration - 0.20:
                time_position = 0.0

        readableTime = convert_time(time_position) # converts to readable time for display
        d = renpy.text.text.Text(readableTime, style=style_name) 
        return d, 0.20

    def music_dur(style_name, st, at):
        global time_duration

        if current_soundtrack == False: # failsafe to when user quits out of OST
            return renpy.text.text.Text("", style=style_name, size=40), 0.0

        if renpy.audio.music.is_playing(channel='music_player'): # checks if music is playing
            time_duration = renpy.audio.music.get_duration(channel='music_player') or time_duration # sets duration to what renpy thinks it lasts
        if current_soundtrack.byteTime:
            time_duration = current_soundtrack.byteTime

        readableDuration = convert_time(time_duration) # converts to readable time for display
        d = renpy.text.text.Text(readableDuration, style=style_name)     
        return d, 0.20

    def dynamic_title_text(style_name, st, at):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return renpy.text.text.Text("Exiting...", size=int(36)), 0.0

        title = len(current_soundtrack.name) # grabs the length of the name and artist 

        if title <= 21: # checks length against set var checks (can be changed) 
            songNameSize = int(37) 
        elif title <= 28:
            songNameSize = int(29)
        else:
            songNameSize = int(23)

        d = renpy.text.text.Text(current_soundtrack.name, style=style_name, substitute=False, size=songNameSize)
        return d, 0.20

    def dynamic_author_text(style_name, st, at):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return renpy.text.text.Text("", style=style_name, size=gui.text_size), 0.0

        author = len(current_soundtrack.author)

        if author <= 32:
            authorNameSize = int(25)
        elif author <= 48:
            authorNameSize = int(23)
        else:
            authorNameSize = int(21)

        d = renpy.text.text.Text(current_soundtrack.author, style=style_name, substitute=False, size=authorNameSize)
        return d, 0.20

    def refresh_cover_data(st, at):
        if current_soundtrack == False: # failsafe to when user quits out of OST
            return renpy.text.text.Text("", size=gui.text_size), 0.0

        d = renpy.display.im.image(current_soundtrack.cover_art)
        return d, 0.20

    # displays current music description
    def dynamic_description_text(style_name, st, at):
        if current_soundtrack == False: 
            return renpy.text.text.Text("", size=23), 0.0

        desc = len(current_soundtrack.description)

        if desc <= 32:
            descSize = int(25)
        elif desc <= 48:
            descSize = int(23)
        else:
            descSize = int(21)

        d = renpy.text.text.Text(current_soundtrack.description, style=style_name, substitute=False, size=descSize) # false sub for albums with brackets/etc
        return d, 0.20

    def auto_play_pause_button(st, at):
        if current_soundtrack == False: 
            return renpy.text.text.Text("", size=23), 0.0
        
        if renpy.audio.music.is_playing(channel='music_player'):
            d = renpy.display.behavior.ImageButton("mod_assets/music_player/pause.png", action=current_music_pause)
        else:
            d = renpy.display.behavior.ImageButton("mod_assets/music_player/play.png", action=current_music_play)
        return d, 0.20

    def rpa_mapping_detection(style_name, st, at):
        try: 
            renpy.exports.file("RPASongMetadata.json")
            return renpy.text.text.Text("", size=23), 0.0
        except:
            return renpy.text.text.Text("{b}Warning:{/b} The RPA metadata file hasn't been generated. Songs in the {i}track{/i} folder that are archived into a\nRPA won't work without it. Set {i}config.developer{/i} to {i}True{/i} in order to generate this file.", style=style_name, size=20), 0.0

    # Converts the time to a readable time
    def convert_time(x):
        readableTime = time.gmtime(float(x))
        res = time.strftime("%M:%S",readableTime)
        return res

    # Pauses the song and saves it's pause spot
    def current_music_pause():
        global current_soundtrack_pause, pausedstate
        pausedstate = True

        soundtrack_position = renpy.audio.music.get_pos(channel = 'music_player') + 1.6

        if soundtrack_position is not None:
            current_soundtrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path

        renpy.audio.music.stop(channel='music_player',fadeout=2.0)

    # Starts the song from it's pause spot
    def current_music_play():
        global pausedstate
        pausedstate = False

        if current_soundtrack_pause is False:
            renpy.audio.music.play(current_soundtrack.path, channel = 'music_player', fadein=2.0)
        else:
            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player', fadein=2.0)
        
    # Forwards track by 5 seconds
    def current_music_forward():
        global current_soundtrack_pause, time_duration

        if renpy.audio.music.get_pos(channel = 'music_player') is None:
            soundtrack_position = time_position + 5
        else:
            soundtrack_position = renpy.audio.music.get_pos(channel = 'music_player') + 5

        soundtrack_duration = renpy.audio.music.get_duration(channel = 'music_player') or time_duration #! to handle latin duration issues
        if current_soundtrack.byteTime:
            time_duration = current_soundtrack.byteTime

        if soundtrack_position >= soundtrack_duration: 
            current_soundtrack_pause = False
            if randomSong:
                random_song()
            else:
                next_track()
        else:
            current_soundtrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path

            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player')

    # Rewinds track by 5 seconds
    def current_music_backward():
        global current_soundtrack_pause

        if renpy.audio.music.get_pos(channel = 'music_player') is None:
            soundtrack_position = time_position - 5
        else:
            soundtrack_position = renpy.audio.music.get_pos(channel = 'music_player') - 5

        if soundtrack_position <= 0.0:
            current_soundtrack_pause = False
            next_track(back=True)
        else:
            current_soundtrack_pause = "<from "+str(soundtrack_position) +">"+current_soundtrack.path
                
            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player')

    # Advances to next track or track behind the current track
    def next_track(back=False):
        global current_soundtrack

        for st in range(len(soundtracks)):
            if current_soundtrack.description == soundtracks[st].description and current_soundtrack.name == soundtracks[st].name:
                try:
                    if back:
                        current_soundtrack = soundtracks[st-1]
                    else:
                        current_soundtrack = soundtracks[st+1]
                except:
                    if back:
                        current_soundtrack = soundtracks[len(soundtracks)-1]
                    else:
                        current_soundtrack = soundtracks[0]
                break

        if current_soundtrack != False:
            renpy.audio.music.play(current_soundtrack.path, channel='music_player', loop=loopSong)

    # Advances to a random track
    def random_song():
        global current_soundtrack

        unique = 1
        if len(soundtracks) == 1:
            pass
        else:
            while unique != 0:
                a = random.randrange(0,len(soundtracks)-1)
                if current_soundtrack != soundtracks[a]:
                    unique = 0
                    current_soundtrack = soundtracks[a]

        if current_soundtrack != False:
            renpy.audio.music.play(current_soundtrack.path, channel='music_player', loop=loopSong)

    # Mutes audio from the player
    def mute_player():
        global old_volume

        if renpy.game.preferences.get_volume("music_player_mixer") != 0.0:
            old_volume = renpy.game.preferences.get_volume("music_player_mixer")
            renpy.game.preferences.set_volume("music_player_mixer", 0.0)
        else:
            renpy.game.preferences.set_volume("music_player_mixer", old_volume)

    def refresh_list():
        scan_song(rescan=True) # scans songs
        if renpy.config.developer or renpy.config.developer == "auto":
            rpa_mapping()
        else:
            rpa_load_mapping()
        resort()

    def resort():
        global soundtracks
        soundtracks = [] # resets soundtrack list
        for obj in songList:
            if obj.unlocked:
                soundtracks.append(obj)
        for obj in manualDefineList:
            if obj.unlocked:
                soundtracks.append(obj)
        if organizeAZ:
            soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.name)
        if organizePriority:
            soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.priority)

    # grabs info from the mp3/ogg (and cover if available)
    def get_info(path, tags):   
        sec = tags.duration
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
            art = altAlbum + cover_formats
            return tags.title, tags.artist, sec, art, tags.album, tags.comment
        except TypeError:
            return tags.title, tags.artist, sec, None, tags.album, tags.comment

    # Scans tracks to the OST Player
    def scan_song(rescan=False):
        global songList

        if rescan:
            songList = []
            
        for ext in file_types:
            songList += ["track/" + x for x in os.listdir(gamedir + '/track') if x.endswith(ext)]

        for y in range(len(songList)):
            if "track/" in songList[y]:
                path = songList[y]
                tags = TinyTag.get(gamedir + "/" + path, image=True) 
                title, artist, sec, altAlbum, album, comment = get_info(path, tags)
                def_song(title, artist, path, priorityScan, sec, altAlbum, y, album, comment, ext)

    # Makes a class for a track to the OST Player
    def def_song(title, artist, path, priority, sec, altAlbum, y, album, comment, ext, unlocked=True, rpa=False):
        if title is None:
            title = "Unknown " + str(ext.replace(".", "")).upper() + " File " + str(y)
        if artist is None:
            artist = "Unknown Artist"
        if altAlbum is None:
            description = "Non-Metadata " + str(ext.replace(".", "")).upper() + " File"
            altAlbum = "mod_assets/music_player/nocover.png" 
        else:
            altAlbum = "track/covers/"+altAlbum
            try:
                renpy.exports.image_size(altAlbum)
            except:
                altAlbum = "mod_assets/music_player/nocover.png" 
        if album is not None: 
            if comment is not None: 
                description = album + '\n' + comment 
            else:
                description = album
        else:
            description = None

        songList[y] = soundtrack(
            name = title,
            author = artist,
            path = path,
            byteTime = sec,
            priority = priorityScan,
            description = description,
            cover_art = altAlbum,
            unlocked = unlocked
        )

    # maps track files in track folder before building the game
    def rpa_mapping():
        data = []
        try: os.remove(gamedir + "/RPASongMetadata.json")
        except: pass
        for y in songList:
            data.append ({
                "class": re.sub(r"-|'| ", "_", y.name),
                "title": y.name,
                "artist": y.author,
                "path": y.path,
                "sec": y.byteTime,
                "altAlbum": y.cover_art,
                "description": y.description,
                "unlocked": y.unlocked,
            })
        with open(gamedir + "/RPASongMetadata.json", "a") as f:
            json.dump(data, f)

    # loads the JSON file that holds RPA metadata
    def rpa_load_mapping():
        try: renpy.exports.file("RPASongMetadata.json")
        except: return

        with renpy.exports.file("RPASongMetadata.json") as f:
            data = json.load(f)

        for p in data:
            title, artist, path, sec, altAlbum, description, unlocked = p['title'], p['artist'], p["path"], p["sec"], p["altAlbum"], p["description"], p["unlocked"]

            p['class'] = soundtrack(
                name = title,
                author = artist,
                path = path,
                byteTime = sec,
                priority = priorityScan,
                description = description,
                cover_art = altAlbum,
                unlocked = unlocked
            )
            songList.append(p['class'])

    def get_music_channel_info():
        global prevTrack
        prevTrack = renpy.audio.music.get_playing(channel='music')
        if prevTrack is None:
            prevTrack = False

    def check_paused_state():
        global pausedstate
        if current_soundtrack == False:
            return
            
        if pausedstate:
            return
        else:
            current_music_pause()

    try: os.mkdir(gamedir + "/track")
    except: pass
    try: os.mkdir(gamedir + "/track/covers")
    except: pass

    # cleans cover directory
    for x in os.listdir(gamedir + '/track/covers'):
        os.remove(gamedir + '/track/covers/' + x)

    scan_song()
    if renpy.config.developer:
        rpa_mapping()
    else:
        rpa_load_mapping()
    resort()