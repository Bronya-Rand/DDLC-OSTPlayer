
# Based off ost.py from Renpy-Universal-Player but Ren'Py 6 compatible

init python:
    import random
    import re
    import io
    import os
    import pygame_sdl2
    import logging
    import json
    from tinytag import TinyTag

    renpy.store.build.archive("track", "mod")
    renpy.store.build.classify("game/RPASongMetadata.json", "track all")
    renpy.store.build.classify("game/python-packages/binaries.txt", "mod all")
    renpy.store.build.classify("game/python-packages/tinytag.py", "mod all")
    renpy.store.build.classify("game/track/**", "track all")

    # Creation of Music Room and Code Setup
    ostVersion = 3.0
    renpy.audio.music.register_channel("music_player", mixer="music_player_mixer", loop=False)

    if renpy.windows:
        gamedir = renpy.config.gamedir.replace("\\", "/")
    elif renpy.android:
        try: os.mkdir(os.path.join(os.environ["ANDROID_PUBLIC"], "game"))
        except: pass
        gamedir = os.path.join(os.environ["ANDROID_PUBLIC"], "game")
        try: file(gamedir + "/RPASongMetadata.json", "r")
        except: open(gamedir + "/RPASongMetadata.json", "w").write(renpy.file("RPASongMetadata.json").read())
    else:
        gamedir = renpy.config.gamedir

    if renpy.android:
        logdir = os.path.join(os.environ["ANDROID_PUBLIC"], "ost_log.txt")
    else:
        logdir = os.path.join(config.basedir, "ost_log.txt")
    if os.path.exists(logdir):
        os.remove(logdir)

    # Lists for holding media types
    autoDefineList = []
    manualDefineList = []
    soundtracks = []
    file_types = ('.mp3', '.ogg', '.opus', '.wav')

    # Stores soundtrack in progress
    current_soundtrack = False

    # Stores positions of track/volume/default priority
    time_position = 0.0
    time_duration = 3.0
    old_volume = 0.0

    # Stores paused track/player controls
    current_soundtrack_pause = False
    prevTrack = False
    randomSong = False
    loopSong = False
    pausedstate = False

    random.seed()

    class soundtrack:
        def __init__(self, name, author, path, album="Unknown Album", albumartist="Unknown Album Artist", 
            composer="Unknown Composer", genre="Unknown Genre", byteTime=False, 
            sideloaded=False, description="", cover_art=None, unlocked=True):
            self.name = name
            self.author = author
            self.path = path
            self.album = album
            self.albumartist = albumartist
            self.composer = composer
            self.genre = genre
            if byteTime:
                self.byteTime = byteTime
            else:
                self.byteTime = get_duration(path)
            self.sideloaded = sideloaded
            self.description = description
            if not cover_art:
                self.cover_art = "mod_assets/music_player/nocover.png"
            else:
                self.cover_art = cover_art
            self.unlocked = unlocked

    @renpy.exports.pure
    class AdjustableAudioPositionValue(renpy.ui.BarValue):
        def __init__(self, channel='music_player', update_interval=0.0):
            self.channel = channel
            self.update_interval = update_interval
            self.adjustment = None
            self._hovered = False

        def get_pos_duration(self):
            pos = renpy.audio.music.get_pos(self.channel) or 0.0
            duration = get_duration()

            return pos, duration

        def get_song_options_status(self):
            return loopSong, randomSong

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = renpy.ui.adjustment(value=pos, range=duration, 
                                                changed=self.set_pos, adjustable=True)

            return self.adjustment

        def hovered(self):
            self._hovered = True

        def unhovered(self):
            self._hovered = False

        def set_pos(self, value):
            loopThis = self.get_song_options_status()
            if (self._hovered and pygame_sdl2.mouse.get_pressed()[0]):
                renpy.audio.music.play("<from {}>".format(value) + current_soundtrack.path,
                    self.channel)
                if loopThis:
                    renpy.audio.music.queue(current_soundtrack.path, self.channel, 
                        loop=True)

        def periodic(self, st):

            pos, duration = self.get_pos_duration()
            loopThis, doRandom = self.get_song_options_status()

            if pos and pos <= duration:
                self.adjustment.set_range(duration)
                self.adjustment.change(pos)
                        
            if pos >= duration - 0.20:
                if loopThis:
                    renpy.audio.music.play(current_soundtrack.path, self.channel, 
                        loop=True)
                elif doRandom:
                    random_song()
                else:
                    next_track()

            return self.update_interval 

    def music_pos(style_name, st, at):
        global time_position

        if renpy.audio.music.get_pos(channel='music_player') is not None:
            time_position = renpy.audio.music.get_pos(channel='music_player')

        readableTime = convert_time(time_position)
        
        if persistent.listui: return renpy.text.text.Text(readableTime,
            style=style_name, substitute=False, size=16), 0.20
        else: return renpy.text.text.Text(readableTime, style=style_name), 0.20
    
    def get_duration(songPath=None):
        if current_soundtrack and current_soundtrack.byteTime and not songPath:
            return current_soundtrack.byteTime
        else:
            try:
                if songPath:
                    pathToSong = songPath
                else:
                    pathToSong = current_soundtrack.path

                tags = TinyTag.get(pathToSong, image=False)
                    
                if tags.duration:
                    return tags.duration
                else:
                    if not songPath:
                        return renpy.audio.music.get_duration(channel='music_player') or time_duration 
            except:
                if not songPath:
                    return renpy.audio.music.get_duration(channel='music_player') or time_duration 

    def music_dur(style_name, st, at):
        global time_duration

        time_duration = get_duration()

        readableDuration = convert_time(time_duration) 
        if persistent.listui: return renpy.text.text.Text(readableDuration, 
            style=style_name, substitute=False, size=16), 0.20
        else: return renpy.text.text.Text(readableDuration, style=style_name), 0.20

    def dynamic_title_text(style_name, st, at):
        title = len(current_soundtrack.name)

        if persistent.listui:
            return renpy.text.text.Text(current_soundtrack.name, style=style_name, substitute=False, 
                                size=21), 0.20
        if title <= 21: 
            songNameSize = int(37) 
        elif title <= 28:
            songNameSize = int(29)
        else:
            songNameSize = int(23)

        return renpy.text.text.Text(current_soundtrack.name, style=style_name, 
            substitute=False, size=songNameSize), 0.20

    def dynamic_author_text(style_name, st, at):
        author = len(current_soundtrack.author)

        if persistent.listui:
            return renpy.text.text.Text(current_soundtrack.author, style=style_name,
                substitute=False, size=21), 0.20

        if author <= 32:
            authorNameSize = int(25)
        elif author <= 48:
            authorNameSize = int(23)
        else:
            authorNameSize = int(21)

        return renpy.text.text.Text(current_soundtrack.author, style=style_name, 
            substitute=False, size=authorNameSize), 0.20

    def refresh_cover_data(st, at):
        return renpy.display.im.image(current_soundtrack.cover_art.replace("[", "\[")), 0.20

    def dynamic_album_text(style_name, st, at):
        desc = len(current_soundtrack.album)

        if persistent.listui:
            return renpy.text.text.Text(current_soundtrack.album, style=style_name, substitute=False, 
                                size=21), 0.20

        if desc <= 32:
            descSize = int(25)
        elif desc <= 48:
            descSize = int(23)
        else:
            descSize = int(21)

        return renpy.text.text.Text(current_soundtrack.album, 
            style=style_name, substitute=False, size=descSize), 0.20

    def auto_play_pause_button(st, at):
        if renpy.audio.music.is_playing(channel='music_player'):
            if pausedstate:
                d = renpy.display.behavior.ImageButton("mod_assets/music_player/pause.png")
            else:
                d = renpy.display.behavior.ImageButton("mod_assets/music_player/pause.png", 
                                                    action=current_music_pause)
        else:
            d = renpy.display.behavior.ImageButton("mod_assets/music_player/play.png", 
                                                action=current_music_play)
        return d, 0.20

    def convert_time(x):
        hour = ""
        
        if int (x / 3600) > 0:
            hour = str(int(x / 3600))
        
        if hour != "":
            if int((x % 3600) / 60) < 10:
                minute = ":0" + str(int((x % 3600) / 60))
            else:
                minute = ":" + str(int((x % 3600) / 60))
        else:
            minute = "" + str(int(x / 60))

        if int(x % 60) < 10:
            second = ":0" + str(int(x % 60))
        else:
            second = ":" + str(int(x % 60))

        return hour + minute + second

    def current_music_pause():
        global current_soundtrack_pause, pausedstate
        pausedstate = True

        if not renpy.audio.music.is_playing(channel='music_player'):
            return
        
        soundtrack_position = (renpy.audio.music.get_pos(channel = 'music_player') or 0.0) + 1.6

        if soundtrack_position is not None:
            current_soundtrack_pause = ("<from " + str(soundtrack_position) + ">" 
                                + current_soundtrack.path)

        renpy.audio.music.stop(channel='music_player',fadeout=2.0)

    def current_music_play():
        global pausedstate
        pausedstate = False

        if not current_soundtrack_pause:
            renpy.audio.music.play(current_soundtrack.path, channel = 'music_player', fadein=2.0)
        else:
            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player', fadein=2.0)
        
    def current_music_forward():
        global current_soundtrack_pause

        if not renpy.audio.music.get_pos(channel = 'music_player'):
            soundtrack_position = time_position + 5
        else:
            soundtrack_position = renpy.audio.music.get_pos(channel = 'music_player') + 5

        if soundtrack_position >= time_duration: 
            current_soundtrack_pause = False
            if randomSong:
                random_song()
            else:
                next_track()
        else:
            current_soundtrack_pause = ("<from " + str(soundtrack_position) + ">" 
                                + current_soundtrack.path)

            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player')

    def current_music_backward():
        global current_soundtrack_pause

        if not renpy.audio.music.get_pos(channel = 'music_player'):
            soundtrack_position = time_position - 5
        else:
            soundtrack_position = renpy.audio.music.get_pos(channel = 'music_player') - 5

        if soundtrack_position <= 0.0:
            current_soundtrack_pause = False
            next_track(back=True)
        else:
            current_soundtrack_pause = ("<from " + str(soundtrack_position) + ">" 
                                + current_soundtrack.path)
                
            renpy.audio.music.play(current_soundtrack_pause, channel = 'music_player')

    def next_track(back=False):
        global current_soundtrack

        index = 0
        while current_soundtrack != soundtracks[index]:
            index = index + 1

        if back:
            current_soundtrack = soundtracks[index-1]
        else:
            try: current_soundtrack = soundtracks[index+1]
            except: current_soundtrack = soundtracks[0]

        renpy.audio.music.play(current_soundtrack.path, channel='music_player', loop=loopSong)

    def random_song():
        global current_soundtrack

        unique = 1
        while unique != 0:
            a = random.randrange(0, len(soundtracks))
            if current_soundtrack != soundtracks[a]:
                unique = 0
                current_soundtrack = soundtracks[a]

        renpy.audio.music.play(current_soundtrack.path, channel='music_player', loop=loopSong)

    def mute_player():
        global old_volume
        logging.info("Muting the audio player.")

        if renpy.game.preferences.get_volume("music_player_mixer") != 0.0:
            old_volume = renpy.game.preferences.get_volume("music_player_mixer")
            renpy.game.preferences.set_volume("music_player_mixer", 0.0)
        else:
            if old_volume == 0.0:
                renpy.game.preferences.set_volume("music_player_mixer", 0.5)
            else:
                renpy.game.preferences.set_volume("music_player_mixer", old_volume)

    def refresh_list():
        logging.info("Refreshing the music player list.")
        scan_song()
        if renpy.config.developer:
            rpa_mapping()
        resort()

    def resort():
        global soundtracks
        logging.info("Sorting the music player list.")

        for obj in autoDefineList:
            if obj not in soundtracks and obj.unlocked:
                soundtracks.append(obj)
        logging.info("Added auto-defined songs to the music list.")

        for obj in manualDefineList:
            if obj not in soundtracks and obj.unlocked:
                soundtracks.append(obj)
        logging.info("Added manual-defined songs to the music list.")

        soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.name)

    def get_info(path, tags):   
        sec = tags.duration
        try:
            image_data = tags.get_image()
            
            if renpy.version_tuple == (6, 99, 12, 4, 2187) and renpy.android:
                with io.open(gamedir + "/binaries.txt", "rb") as a:
                    lines = a.readlines() 
            else:
                with renpy.exports.file("python-packages/binaries.txt") as a:
                    lines = a.readlines()

            jpgbytes = bytes("\\xff\\xd8\\xff")
            utfbytes = bytes("o\\x00v\\x00e\\x00r\\x00\\x00\\x00\\x89PNG\\r\\n")

            jpgmatch = re.search(jpgbytes, image_data) 
            utfmatch = re.search(utfbytes, image_data) 

            if jpgmatch:
                cover_formats=".jpg" 
            else:
                cover_formats=".png" 

                if utfmatch: # addresses itunes cover descriptor fixes
                    logging.warning("Improper PNG data was found. Repairing cover art.")
                    image_data = re.sub(utfbytes, lines[2], image_data)

            coverAlbum = re.sub(r"(\\|/|\:|\?|\*|\<|\>|\||\[|\])", "", tags.album)

            if not os.path.exists(os.path.join(gamedir, 'track/covers', coverAlbum + cover_formats)):
            
                with open(os.path.join(gamedir, 'track/covers', coverAlbum + cover_formats), 'wb') as f:
                    f.write(image_data)

            art = "track/covers/" + coverAlbum + cover_formats
            logging.info("Obtained album cover for " + path + ".")
            return art
        except TypeError:
            logging.warning("Cover art could not be obtained/written to the \"covers\" directory.")
            return None

    def scan_song():
        global autoDefineList

        logging.info("Scanning music directories.")
        exists = check_removed_songs()
        
        logging.info("Scanning the \"track\" folder for music.")
        for x in os.listdir(gamedir + '/track'):
            if x.endswith((file_types)) and "track/" + x not in exists:
                path = "track/" + x
                logging.info("Obtaining metadata info for " + path + ".")

                try: tags = TinyTag.get(gamedir + "/" + path, image=True) 
                except IOError: 
                    logging.error("'IOError' while obtaining metadata info for " + path + ". Skipping song.")
                    continue

                albumart = get_info(path, tags)
                def_song(path, tags, albumart, True)
                exists.append(path)

    def check_removed_songs():
        exists = []
        logging.info("Checking for removed songs.")

        for x in autoDefineList[:]:
            try:
                renpy.exports.file(x.path)
                exists.append(x.path)    
            except:
                if renpy.android and not renpy.version_tuple == (6, 99, 12, 4, 2187):
                    try:
                        file(x.path)
                        exists.append(x.path)
                    except:
                        logging.info("Removed " + x.path + " from the music player list.")
                        autoDefineList.remove(x)
                else:
                    logging.info("Removed " + x.path + " from the music player list.")
                    autoDefineList.remove(x)

        return exists

    def def_song(path, tags, albumart, unlocked=True):
        logging.info("Defining song located in " + path + " to the music player.")            
        
        class_name = re.sub(r"-|'| ", "_", tags.title or str(path.replace("track/", "")))

        class_name = soundtrack(
            name = tags.title or str(path.replace("track/", "")),
            author = tags.artist or "Unknown Artist",
            album = tags.album or "Unknown Album",
            albumartist = tags.albumartist or "Unknown Album Artist",
            composer = tags.composer or "Unknown Composer",
            genre = tags.genre or "Unknown Genre",
            path = path,
            byteTime = tags.duration or False,
            sideloaded = True,
            description = tags.comment or "",
            cover_art = albumart,
            unlocked = unlocked
        )
        autoDefineList.append(class_name)

    def get_music_channel_info():
        global prevTrack

        logging.info("Getting music playing from music channel.")
        prevTrack = renpy.audio.music.get_playing(channel='music') or prevTrack
        logging.info("Obtained music status from \"renpy.audio.music\".")

        if not prevTrack:
            logging.warning("No music was found via \"renpy.audio.music\".")
            prevTrack = False

    def check_paused_state():
        logging.info("Checking if a music session exists or if we are in a paused state.")
        if not current_soundtrack or pausedstate:
            logging.info("No music session found or we are currently in a paused state. " 
                "Exiting check state.")
            return
        else:
            logging.info("A music session was found or we are currently not in a paused state. "
                "Stopping music session and exiting check state.")
            current_music_pause()

    def ost_log_start():
        logging.basicConfig(filename=logdir, level=logging.DEBUG)
        logging.info("Started logging this OST-Player session for errors.")

    def ost_log_stop():
        logging.info("Stopped logging this OST-Player session for errors.")
        logging.shutdown()

    def ost_start():
        if renpy.config.developer: rpa_mapping()
        else: rpa_load_mapping() 
        get_music_channel_info()
        resort()

    def ost_quit():
        check_paused_state()
        ost_log_stop()

    def rpa_mapping():
        if not renpy.config.developer: return
        data = []

        try: os.remove(os.path.join(gamedir, "RPASongMetadata.json"))
        except: pass

        for y in autoDefineList:
            data.append ({
                "class": re.sub(r"-|'| ", "_", y.name or str(y.path.replace("track/", ""))),
                "title": y.name,
                "artist": y.author,
                "album": y.album,
                "albumartist": y.albumartist,
                "composer": y.composer,
                "genre": y.genre,
                "path": y.path,
                "sec": y.byteTime,
                "sideloaded": y.sideloaded,
                "comment": y.description,
                "cover_art": y.cover_art,
                "unlocked": y.unlocked,
            })

        with open(gamedir + "/RPASongMetadata.json", "a") as f:
            json.dump(data, f)

    def rpa_load_mapping():
        try: 
            logging.info("Attempting to load 'RPASongMetadata.json'.")
            if renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187): 
                with file(gamedir + "/RPASongMetadata.json") as f:
                    data = json.load(f)
            else:
                with renpy.exports.file("RPASongMetadata.json") as f:
                    data = json.load(f)
            logging.info("Loaded 'RPASongMetadata.json'.")
        except IOError: 
            logging.warning("Attempting to load 'RPASongMetadata.json' failed.")
            return
        
        exists = check_removed_songs()

        for p in data:
            logging.info("Defining cached class " + p['class'] + " to the music player.")
            if p['path'] not in exists:

                p['class'] = soundtrack(
                    name = p['title'],
                    author = p['artist'],
                    album = p['album'],
                    albumartist = p['albumartist'],
                    composer = p['composer'],
                    genre = p['genre'],
                    path = p['path'],
                    byteTime = p['sec'],
                    sideloaded = p['sideloaded'],
                    description = p['comment'],
                    cover_art = p['cover_art'],
                    unlocked = p['unlocked']
                )
                autoDefineList.append(p['class'])
    
    ost_log_start()

    logging.info("Making the \"track\" folder in " + gamedir + " if it's not present.")
    try: os.mkdir(os.path.join(gamedir, "track"))
    except: pass
    logging.info("Making the \"covers\" folder in " + gamedir + "/track if it's not present.")
    try: os.mkdir(os.path.join(gamedir, "track", "covers"))
    except: pass

    logging.info("Clearing the covers folder of cover art.")
    for x in os.listdir(os.path.join(gamedir, "track", "covers")):
        os.remove(os.path.join(gamedir, "track", "covers", x))

    scan_song()

    renpy.game.preferences.set_mute("music", False)
