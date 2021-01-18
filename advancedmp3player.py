import os
import tkinter
from tkinter import filedialog
from tkinter import PhotoImage, END
import pygame
import requests
import json
import googletrans
import wikipedia
from tinytag import TinyTag
import io
from PIL import Image, ImageTk
from urllib.request import urlopen


class MusicPlayer(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack()

        self.dict_of_images={}

        self.list_of_songs = []
        self.current_track_index=0
        self.has_already_been_playing=False
        self.is_paused=True
        self.curr_track_title = ""
        self.curr_track_artist = ""
        self.curr_track_album = ""
        self.curr_track_year = ""
        self.curr_track_genre = ""
        self.curr_track_duration = ""
        pygame.init()
        pygame.mixer.init()

        self.create_root_frames()

        self.create_widgets_title_image_frame()
        self.create_widgets_current_track_frame()
        self.create_widgets_additional_data_frame()
        self.create_widgets_controls_frame()
        self.create_widgets_current_tracklist_frame()


    def create_root_frames(self):
        self.title_image_frame = tkinter.LabelFrame(self,bg='black',fg='white',bd=6, relief=tkinter.RIDGE)
        self.title_image_frame.configure(width=600,height=100)
        self.title_image_frame.grid_propagate(0)
        self.title_image_frame.grid(row=0,column=0,columnspan=2)

        self.current_track_frame = tkinter.LabelFrame(self,text='Currently Playing...',  font='Courier 10 bold', bg='black',fg='white',bd=6,relief=tkinter.RIDGE)
        self.current_track_frame.configure(width=410,height=250)
        self.current_track_frame.grid_propagate(0)
        self.current_track_frame.grid(row=1,column=0)

        self.access_additional_data_frame = tkinter.LabelFrame(self, text='Access Additional Data', font='Courier 10 bold',bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.access_additional_data_frame.configure(width=410, height=75)
        self.access_additional_data_frame.grid_propagate(0)
        self.access_additional_data_frame.grid(row=2, column=0)

        self.track_controls_frame = tkinter.LabelFrame(self, text='Controls', font='Courier 10 bold', bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.track_controls_frame.configure(width=410, height=75)
        self.track_controls_frame.grid_propagate(0)
        self.track_controls_frame.grid(row=3, column=0)

        self.current_tracklist_frame = tkinter.LabelFrame(self,text='Current Playlist',  font='Courier 10 bold', bg='black',fg='white',bd=6,relief=tkinter.RIDGE)
        self.current_tracklist_frame.configure(width=190,height=400)
        self.current_tracklist_frame.grid_propagate(0)
        self.current_tracklist_frame.grid(row=1,column=1,rowspan=3)

    # Fill Frames With Widgets

    def create_widgets_title_image_frame(self):
        self.title_image_canvas = tkinter.Label(self.title_image_frame,image=title_image)
        self.title_image_canvas.configure(width=584,height=84)
        self.title_image_canvas.pack()
        pass
    def create_widgets_current_track_frame(self):
        self.text_title_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                               fg='white')
        self.text_title_canvas['text'] = "Title: "
        self.text_title_canvas.configure(width=30, height=1)
        self.text_title_canvas.grid(row=0, column=0, pady=5)

        self.text_artist_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                                fg='white')
        self.text_artist_canvas['text'] = "Artist: "
        self.text_artist_canvas.configure(width=30, height=1)
        self.text_artist_canvas.grid(row=1, column=0, pady=4)

        self.text_album_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                                fg='white')
        self.text_album_canvas['text'] = "Album: "
        self.text_album_canvas.configure(width=30, height=1)
        self.text_album_canvas.grid(row=2, column=0, pady=4)

        self.text_year_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                               fg='white')
        self.text_year_canvas['text'] = "Year: "
        self.text_year_canvas.configure(width=30, height=1)
        self.text_year_canvas.grid(row=3, column=0, pady=4)

        self.text_genre_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                              fg='white')
        self.text_genre_canvas['text'] = "Genre: "
        self.text_genre_canvas.configure(width=30, height=1)
        self.text_genre_canvas.grid(row=4, column=0, pady=4)

        self.text_duration_canvas = tkinter.Label(self.current_track_frame, font='Courier 15 bold', bg='black',
                                               fg='white')
        self.text_duration_canvas['text'] = "Duration (secs): "
        self.text_duration_canvas.configure(width=30, height=1)
        self.text_duration_canvas.grid(row=5, column=0, pady=4)
        pass
    def create_widgets_additional_data_frame(self):
        self.button_get_lyrics  = tkinter.Button (self.access_additional_data_frame, bg='grey', fg='white', font='Courier 15 bold')
        self.button_get_lyrics['text'] = 'Lyrics'
        self.button_get_lyrics['command'] = self.show_lyrics
        self.button_get_lyrics.grid(row=0,column=0, pady=4,padx=3)

        self.button_get_artist_info = tkinter.Button(self.access_additional_data_frame, bg='grey', fg='white',
                                                font='Courier 15 bold')
        self.button_get_artist_info['text'] = 'Artist Data'
        self.button_get_artist_info['command'] = lambda: self.showWikiInfo(self.curr_track_artist)
        self.button_get_artist_info.grid(row=0, column=1, pady=4,padx=4)

        self.button_get_track_info = tkinter.Button(self.access_additional_data_frame, bg='grey', fg='white',
                                                font='Courier 15 bold')
        self.button_get_track_info['text'] = 'Track Data'
        self.button_get_track_info['command'] = lambda: self.showWikiInfo(self.curr_track_title)
        self.button_get_track_info.grid(row=0, column=2, pady=4,padx=4)
        pass
    def create_widgets_controls_frame(self):
        self.button_choose_folder = tkinter.Button(self.track_controls_frame, bg='grey', fg='white',
                                                   font='Courier 10 bold')
        self.button_choose_folder['text'] = 'Choose Folder'
        self.button_choose_folder['command'] = self.choose_folder
        self.button_choose_folder.config(height=2)
        self.button_choose_folder.grid(row=0, column=0, pady=3, padx=6)

        self.button_previous = tkinter.Button(self.track_controls_frame, bg='grey', fg='white', image=previous_button_image)
        self.button_previous['command'] = self.previous_track
        self.button_previous.grid(row=0, column=1, pady=0, padx=3)

        self.button_pause = tkinter.Button(self.track_controls_frame, bg='grey', fg='white',image=pause_button_image)
        self.button_pause['command'] = self.pause_track
        self.button_pause.grid(row=0, column=2, pady=0, padx=3)

        self.button_next = tkinter.Button(self.track_controls_frame, bg='grey', fg='white',image=next_button_image)
        self.button_next['command'] = self.next_track
        self.button_next.grid(row=0, column=3, pady=0, padx=3)

        self.volume_variable = tkinter.DoubleVar()
        self.volume_slider = tkinter.Scale(self.track_controls_frame, from_=0, to =100, orient = tkinter.HORIZONTAL, bg='grey', fg='white',highlightbackground='black', troughcolor='black', font='Courier 15 bold')
        self.volume_slider['variable']  = self.volume_variable
        self.volume_slider['command'] = self.change_volume
        self.volume_slider.set(50)
        pygame.mixer.music.set_volume(0.50)
        self.volume_slider.grid(row=0,column=4, pady=0, padx=3)
        pass


    def create_widgets_current_tracklist_frame(self):
        self.list_of_songs_scrollbar = tkinter.Scrollbar(self.current_tracklist_frame,orient = tkinter.VERTICAL)
        self.list_of_songs_scrollbar.grid(row=0,column=1,pady=6,rowspan=6,sticky='NS')

        self.list_of_songs_listbox = tkinter.Listbox(self.current_tracklist_frame, selectmode = tkinter.SINGLE, yscrollcommand=self.list_of_songs_scrollbar.set, selectbackground='grey', bg='black', fg='white',font='Courier 10 bold')
        self.list_of_songs_listbox.config(width=19,height=21)
        self.fill_list_of_songs_listbox()
        self.list_of_songs_listbox.bind('<Double-Button-1>', self.play_track)
        self.list_of_songs_scrollbar.config(command=self.list_of_songs_listbox.yview)
        self.list_of_songs_listbox.grid(row=0,column=0,padx=1,pady=6, rowspan=6,sticky='NS')

        pass

    def fill_list_of_songs_listbox(self):
        for index, track in enumerate(self.list_of_songs):
            self.list_of_songs_listbox.insert(index, os.path.basename(track))

    # Button Functions
    def get_lyrics(self):
        artist = self.curr_track_artist
        title = self.curr_track_title
        url = 'https://api.lyrics.ovh/v1/' + artist + '/' + title
        response = requests.get(url)
        json_response = json.loads(response.content)
        lyrics = json_response["lyrics"]
        return lyrics
        pass
    def show_lyrics(self):
        lyrics = self.get_lyrics()
        self.show_lyrics_window = tkinter.Toplevel()
        title_text = self.curr_track_title + " by " + self.curr_track_artist + " Lyrics"
        self.show_lyrics_window.wm_title(title_text)
        self.show_lyrics_window.geometry("300x550")
        self.show_lyrics_window.resizable(0, 0)
        self.show_lyrics_window.configure(background="black")

        #create frames for lyrics window
        self.lyrics_window_title_frame = tkinter.LabelFrame(self.show_lyrics_window, bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.lyrics_window_title_frame.configure(width=300, height=100)
        self.lyrics_window_title_frame.grid_propagate(0)
        self.lyrics_window_title_frame.pack_propagate(0)
        self.lyrics_window_title_frame.grid(row=0, column=0)

        self.lyrics_window_text_frame = tkinter.LabelFrame(self.show_lyrics_window, bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.lyrics_window_text_frame.configure(width=300, height=400)
        self.lyrics_window_text_frame.grid_propagate(0)
        self.lyrics_window_text_frame.pack_propagate(0)
        self.lyrics_window_text_frame.grid(row=1, column=0)

        self.lyrics_window_button_frame = tkinter.LabelFrame(self.show_lyrics_window, bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.lyrics_window_button_frame.configure(width=300, height=50)
        self.lyrics_window_button_frame.grid_propagate(0)
        self.lyrics_window_button_frame.pack_propagate(0)
        self.lyrics_window_button_frame.grid(row=2, column=0)

        #fill frames of lyrics window
        self.lyrics_title1_canvas = tkinter.Label(self.lyrics_window_title_frame, font='Courier 12 bold', bg='black',fg='white')
        self.lyrics_title1_canvas['text'] = self.curr_track_title
        self.lyrics_title1_canvas.configure(width=28, height=1)
        self.lyrics_title1_canvas.grid(row=0, column=0, sticky='W')
        self.lyrics_title2_canvas = tkinter.Label(self.lyrics_window_title_frame, font='Courier 12 bold', bg='black',fg='white')
        self.lyrics_title2_canvas['text'] = "by"
        self.lyrics_title2_canvas.configure(width=28, height=1)
        self.lyrics_title2_canvas.grid(row=1, column=0, sticky='W')
        self.lyrics_title3_canvas = tkinter.Label(self.lyrics_window_title_frame, font='Courier 12 bold', bg='black',fg='white')
        self.lyrics_title3_canvas['text'] = self.curr_track_artist
        self.lyrics_title3_canvas.configure(width=28, height=1)
        self.lyrics_title3_canvas.grid(row=2, column=0, sticky='W')

        t = tkinter.Text(self.lyrics_window_text_frame, wrap=tkinter.WORD, background="black", fg="white", font='Courier 10 bold')
        t.pack_propagate(0)
        t.insert(END, lyrics)
        t.tag_configure("center", justify='center')
        t.tag_add("center", 1.0, "end")
        t.pack()

        option_menu_variable = tkinter.StringVar(self.lyrics_window_button_frame)
        option_menu_variable.set(list(googletrans.LANGUAGES.values())[73])  # default value

        w = tkinter.OptionMenu(self.lyrics_window_button_frame, option_menu_variable, *list(googletrans.LANGUAGES.values()))
        w.config(width=15,bg='black', fg='white',font='Courier 10 bold',highlightthickness=0,highlightcolor='grey')
        w.grid(row=0, column=0, padx=15,pady=5)
        self.button_translate = tkinter.Button(self.lyrics_window_button_frame, bg='grey', fg='white',
                                                   font='Courier 10 bold')
        self.button_translate['text'] = 'Translate'
        self.button_translate['command'] = lambda : self.show_translated_lyrics(lyrics,option_menu_variable.get())
        self.button_translate.config(height=1)
        self.button_translate.grid(row=0, column=1,pady=5)
        pass

    def translate_lyrics(self, lyrics, selected_language_name):
        languagesNames = list(googletrans.LANGUAGES.values())
        languagesCodes = list(googletrans.LANGUAGES.keys())
        selected_language_code = languagesCodes[languagesNames.index(selected_language_name)]

        tranlator = googletrans.Translator()
        translated_lyrics = tranlator.translate(lyrics, dest=selected_language_code)
        return translated_lyrics.text

    def show_translated_lyrics(self,lyrics,chosen_language):
        translated_lyrics = self.translate_lyrics(lyrics, chosen_language)
        self.show_translated_lyrics_window = tkinter.Toplevel()
        title_text = "["+chosen_language+"] "+ self.curr_track_title + " by " + self.curr_track_artist + " Lyrics"
        self.show_translated_lyrics_window.wm_title(title_text)
        self.show_translated_lyrics_window.geometry("300x500")
        self.show_translated_lyrics_window.resizable(0, 0)
        self.show_translated_lyrics_window.configure(background="black")

        # create frames for translated lyrics window
        self.translated_lyrics_window_title_frame = tkinter.LabelFrame(self.show_translated_lyrics_window, bg='black', fg='white', bd=6,
                                                            relief=tkinter.RIDGE)
        self.translated_lyrics_window_title_frame.configure(width=300, height=100)
        self.translated_lyrics_window_title_frame.grid_propagate(0)
        self.translated_lyrics_window_title_frame.pack_propagate(0)
        self.translated_lyrics_window_title_frame.grid(row=0, column=0)

        self.translated_lyrics_window_text_frame = tkinter.LabelFrame(self.show_translated_lyrics_window, bg='black', fg='white', bd=6,
                                                           relief=tkinter.RIDGE)
        self.translated_lyrics_window_text_frame.configure(width=300, height=400)
        self.translated_lyrics_window_text_frame.grid_propagate(0)
        self.translated_lyrics_window_text_frame.pack_propagate(0)
        self.translated_lyrics_window_text_frame.grid(row=1, column=0)

        # fill frames of translated lyrics window
        self.translated_lyrics_title1_canvas = tkinter.Label(self.translated_lyrics_window_title_frame, font='Courier 12 bold', bg='black',
                                                  fg='white')
        self.translated_lyrics_title1_canvas['text'] = "["+chosen_language+"] "+self.curr_track_title
        self.translated_lyrics_title1_canvas.configure(width=28, height=1)
        self.translated_lyrics_title1_canvas.grid(row=0, column=0, sticky='W')
        self.translated_lyrics_title2_canvas = tkinter.Label(self.translated_lyrics_window_title_frame, font='Courier 12 bold', bg='black',
                                                  fg='white')
        self.translated_lyrics_title2_canvas['text'] = "by"
        self.translated_lyrics_title2_canvas.configure(width=28, height=1)
        self.translated_lyrics_title2_canvas.grid(row=1, column=0, sticky='W')
        self.translated_lyrics_title3_canvas = tkinter.Label(self.translated_lyrics_window_title_frame, font='Courier 12 bold', bg='black',
                                                  fg='white')
        self.translated_lyrics_title3_canvas['text'] = self.curr_track_artist
        self.translated_lyrics_title3_canvas.configure(width=28, height=1)
        self.translated_lyrics_title3_canvas.grid(row=2, column=0, sticky='W')

        t = tkinter.Text(self.translated_lyrics_window_text_frame, wrap=tkinter.WORD, background="black", fg="white",
                         font='Courier 10 bold')
        t.pack_propagate(0)
        t.insert(END, translated_lyrics)
        t.tag_configure("center", justify='center')
        t.tag_add("center", 1.0, "end")
        t.pack()
        pass

    def getWikiImageURL(self,searched_title):
        WIKI_REQUEST_LINE = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
        try:
            result = wikipedia.search(searched_title, results=1)
            wikipedia.set_lang('en')
            wikipage = wikipedia.WikipediaPage(title=result[0])
            wikipage_title = wikipage.title
            response = requests.get(WIKI_REQUEST_LINE + wikipage_title)
            json_data = json.loads(response.text)
            image_url = list(json_data['query']['pages'].values())[0]['original']['source']
            return image_url
        except:
            return 0

    def getWikiInfo(self,searched_title):
        try:
            result = wikipedia.search(searched_title, results=1)
            wikipedia.set_lang('en')
            wikipage = wikipedia.WikipediaPage(title=result[0])
            return wikipage.summary
        except:
            return 0
    @staticmethod
    def resize(original_image_width, original_image_height, destination_image_box_width, destination_image_box_height,pil_image):
        f1 = 1.0 * destination_image_box_width / original_image_width
        f2 = 1.0 * destination_image_box_height / original_image_height
        factor = min([f1, f2])
        new_image_width = int(original_image_width * factor)
        new_image_height = int(original_image_height * factor)
        return pil_image.resize((new_image_width, new_image_height), Image.ANTIALIAS)

    def showWikiInfo(self, searched_title):
        url_image = self.getWikiImageURL(searched_title)
        info = self.getWikiInfo(searched_title)

        self.show_wiki_info_window = tkinter.Toplevel()
        title_text = searched_title + " - Wiki Info"
        self.show_wiki_info_window.wm_title(title_text)
        self.show_wiki_info_window.geometry("600x550")
        self.show_wiki_info_window.resizable(0, 0)
        self.show_wiki_info_window.configure(background="black")

        # create frames for wiki info window
        self.wiki_info_window_title_frame = tkinter.LabelFrame(self.show_wiki_info_window, bg='black', fg='white', bd=6, relief=tkinter.RIDGE)
        self.wiki_info_window_title_frame.configure(width=600, height=50)
        self.wiki_info_window_title_frame.grid_propagate(0)
        self.wiki_info_window_title_frame.pack_propagate(0)
        self.wiki_info_window_title_frame.grid(row=0, column=0)
        if(url_image!=0):
            #pass
            self.wiki_info_window_image_frame = tkinter.LabelFrame(self.show_wiki_info_window, bg='black', fg='white',bd=6, relief=tkinter.RIDGE)
            self.wiki_info_window_image_frame.configure(width=600, height=180)
            self.wiki_info_window_image_frame.pack_propagate(0)
            self.wiki_info_window_image_frame.grid(row=1, column=0)
        else:
            self.show_wiki_info_window.geometry("600x370")

        self.wiki_info_window_content_frame = tkinter.LabelFrame(self.show_wiki_info_window, bg='black', fg='white',bd=6, relief=tkinter.RIDGE)
        self.wiki_info_window_content_frame.configure(width=600, height=320)
        self.wiki_info_window_content_frame.grid_propagate(0)
        self.wiki_info_window_content_frame.pack_propagate(0)
        self.wiki_info_window_content_frame.grid(row=2, column=0)

        # fill frames of wiki info window frames

        self.wiki_info_title_canvas = tkinter.Label(self.show_wiki_info_window, font='Courier 15 bold',bg='black', fg='white')
        self.wiki_info_title_canvas['text'] = searched_title
        self.wiki_info_title_canvas.configure(width=48, height=1)
        self.wiki_info_title_canvas.grid(row=0, column=0, pady=5)

        if url_image != 0:
            destination_image_box_width = 560
            destination_image_box_height = 160

            image_bytes = urlopen(url_image).read()
            data_stream = io.BytesIO(image_bytes)

            pil_image = Image.open(data_stream)

            original_image_width, original_image_height = pil_image.size

            pil_image_resized = MusicPlayer.resize(original_image_width, original_image_height, destination_image_box_width,
                                            destination_image_box_height, pil_image)


            # Convert PIL image object to Tkinter's PhotoImage object
            #self.tk_image = ImageTk.PhotoImage(pil_image_resized)
            if(len(self.dict_of_images)==100):
                self.dict_of_images.clear()
            self.dict_of_images[searched_title] = ImageTk.PhotoImage(pil_image_resized)

            # fill frame with image
            self.wiki_image_canvas = tkinter.Label(self.wiki_info_window_image_frame, image=self.dict_of_images[searched_title],width=destination_image_box_width, height=destination_image_box_height)
            self.wiki_image_canvas.configure(background="black")
            self.wiki_image_canvas.pack(padx=5, pady=5)

        if info != 0:
            self.wiki_text = tkinter.Text(self.wiki_info_window_content_frame, wrap=tkinter.WORD, background="black",
                                          fg="white", font='Courier 10 bold')
            self.wiki_text.insert(END, info)
            self.wiki_text.tag_configure("center", justify='center')
            self.wiki_text.tag_add("center", 1.0, "end")
            self.wiki_text.pack()

    def choose_folder(self):
        self.list_of_compatible_tracks = []
        chosen_directory = filedialog.askdirectory(title="Choose Folder")
        for root_path,directories,files in os.walk(chosen_directory):
            for file in files:
                if os.path.splitext(file)[1]=='.mp3':
                    path_to_song = (root_path+'/'+file).replace('\\','/')
                    self.list_of_compatible_tracks.append(path_to_song)
        if self.list_of_compatible_tracks:
            self.list_of_songs = self.list_of_compatible_tracks
            self.list_of_songs_listbox.delete(0,tkinter.END)
            self.fill_list_of_songs_listbox()
        pass

    def play_track(self,event=None):
        if event is not None:
            self.current_track_index= self.list_of_songs_listbox.curselection()[0]
        pygame.mixer.music.load(self.list_of_songs[self.current_track_index])

        self.button_pause['image'] = play_button_image
        self.is_paused=False
        self.has_already_been_playing=True

        metadata = self.get_file_metadata(self.list_of_songs[self.current_track_index])
        self.curr_track_title = metadata[0]
        self.curr_track_artist = metadata[1]
        self.curr_track_album = metadata[2]
        self.curr_track_year = metadata[3]
        self.curr_track_genre = metadata[4]
        self.curr_track_duration = metadata[5]

        self.text_title_canvas['text'] = "Title: " + self.curr_track_title
        self.text_artist_canvas['text'] = "Artist: " + self.curr_track_artist
        self.text_album_canvas['text'] = "Album: " + self.curr_track_album
        self.text_year_canvas['text'] = "Year: " + self.curr_track_year
        self.text_genre_canvas['text'] = "Genre: " + self.curr_track_genre
        self.text_duration_canvas['text'] = "Duration (secs): " + self.curr_track_duration

        self.list_of_songs_listbox.activate(self.current_track_index)
        pygame.mixer.music.play()
        pass
    def get_file_metadata(self, file):
        tag = TinyTag.get(file)
        curr_title = tag.title
        curr_artist = tag.artist
        curr_album = tag.album
        curr_year=tag.year
        curr_genre = tag.genre
        curr_duration = str(round(float(tag.duration),3))
        return [curr_title,curr_artist,curr_album,curr_year,curr_genre,curr_duration]
        pass
    def previous_track(self):
        if self.current_track_index>=1:
            self.current_track_index-=1
        else:
            self.current_track_index=(len(self.list_of_songs)-1)
        self.play_track()
        pass
    def pause_track(self):
        if self.is_paused == False:
            self.is_paused=True
            pygame.mixer.music.pause()
            self.button_pause['image'] = pause_button_image
        else:
            if self.has_already_been_playing == False:
                self.play_track()
            self.is_paused = False
            pygame.mixer.music.unpause()
            self.button_pause['image'] = play_button_image
        pass
    def next_track(self):
        if self.current_track_index<(len(self.list_of_songs)-1):
            self.current_track_index+=1
        else:
            self.current_track_index=0
        self.play_track()
        pass
    def change_volume(self,event=None):
        self.new_volume = self.volume_slider.get()
        pygame.mixer.music.set_volume((self.new_volume/100))

        pass




root = tkinter.Tk()
root.geometry("600x500")
root.configure(background="purple")
root.resizable(0, 0)
root.wm_title('Advanced MP3 Player By Maciej Chrzastek')

title_image=PhotoImage(file='resources/title.gif')
play_button_image=PhotoImage(file='resources/play.gif')
pause_button_image=PhotoImage(file='resources/pause.gif')
next_button_image=PhotoImage(file='resources/next.gif')
previous_button_image=PhotoImage(file='resources/previous.gif')


application = MusicPlayer(root)
application.mainloop()