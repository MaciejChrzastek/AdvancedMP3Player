import os
import tkinter
from tkinter import filedialog
from tkinter import PhotoImage, END
import pygame
import pickle
import requests
import json
import googletrans
import wikipedia
from tinytag import TinyTag
import io
from PIL import Image, ImageTk
from urllib.request import urlopen


def getWikiImageURL(searched_title):
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
def getWikiInfo(searched_title):
    try:
        result = wikipedia.search(searched_title, results=1)
        wikipedia.set_lang('en')
        wikipage = wikipedia.WikipediaPage(title=result[0])
        return wikipage.summary
    except:
        return 0
def resize(original_image_width, original_image_height, destination_image_box_width, destination_image_box_height, pil_image):
    f1 = 1.0 * destination_image_box_width / original_image_width
    f2 = 1.0 * destination_image_box_height / original_image_height
    factor = min([f1, f2])
    new_image_width = int(original_image_width * factor)
    new_image_height = int(original_image_height * factor)
    return pil_image.resize((new_image_width, new_image_height), Image.ANTIALIAS)

def showWikiInfo(searched_title):
    url_image = getWikiImageURL(searched_title)
    info = getWikiInfo(searched_title)

    root = tkinter.Tk()
    root.configure(background="black")
    root.geometry("600x500")
    root.resizable(0, 0)
    title_text=searched_title + " - Wiki Info"
    root.title(title_text)

    destination_image_box_width = 560
    destination_image_box_height = 160

    if url_image!=0:
        image_bytes = urlopen(url_image).read()
        data_stream = io.BytesIO(image_bytes)

        pil_image = Image.open(data_stream)

        original_image_width, original_image_height = pil_image.size

        pil_image_resized = resize(original_image_width, original_image_height, destination_image_box_width, destination_image_box_height, pil_image)

        # Convert PIL image object to Tkinter's PhotoImage object
        tk_image = ImageTk.PhotoImage(pil_image_resized)

        #fill frame with image
        wiki_image_canvas = tkinter.Label(root, image=tk_image, width=destination_image_box_width, height=destination_image_box_height)
        wiki_image_canvas.configure(background="white")
        wiki_image_canvas.pack(padx=5, pady=5)

    if info !=0:
        t = tkinter.Text(root,wrap=tkinter.WORD, background="black", fg="white",font='Courier 10 bold')
        t.insert(END,info)
        t.tag_configure("center", justify='center')
        t.tag_add("center", 1.0, "end")
        t.pack()
    root.mainloop()

showWikiInfo("Elvis Presley")
