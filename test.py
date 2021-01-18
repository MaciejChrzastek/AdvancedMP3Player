import pygame
import requests
import json
import googletrans
import wikipedia
from tinytag import TinyTag



def getLyrics(artist, title):
    url = 'https://api.lyrics.ovh/v1/' + artist + '/' + title
    response = requests.get(url)
    json_response = json.loads(response.content)
    lyrics = json_response["lyrics"]
    return lyrics

def translateLyrics(lyrics):
    languagesNames = list(googletrans.LANGUAGES.values())
    languagesCodes = list(googletrans.LANGUAGES.keys())
    print(languagesNames)
    selected_language_name = input("Select language to translate to: ")
    selected_language_code = languagesCodes[languagesNames.index(selected_language_name)]

    tranlator = googletrans.Translator()
    print (selected_language_code)
    translated_lyrics  = tranlator.translate(lyrics, dest=selected_language_code)
    return translated_lyrics.text

def getWikiInfo(searched_title):
    try:
        result = wikipedia.search(searched_title, results=1)
        wikipedia.set_lang('en')
        wikipage = wikipedia.WikipediaPage(title=result[0])
        return wikipage.summary
    except:
        return 0

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

def showInfo(searched_term):
    info = getWikiInfo(searched_term)
    image_url = getWikiImageURL(searched_term)


file = r'C:\Users\Maciej Chrząstek\Music\iTunes\iTunes Media\Music\Elvis Presley\Elvis Presley [1956]\01 Blue Suede Shoes.mp3'.lower()



tag = TinyTag.get(file)

print()
print('"title": "%s",' % tag.title)
print('"artist": "%s",' % tag.artist)
print('"album": "%s",' % tag.album)
print('"year": "%s",' % tag.year)
print('"genre": "%s",' % tag.genre)
print('"duration(secs)": "%s",' % tag.duration)
currLyrics = getLyrics(tag.artist,tag.title)
print(currLyrics)
print(translateLyrics(currLyrics))

print()
print(getWikiInfo(tag.artist))
print()
print(getWikiInfo(tag.title))
print()
print(getWikiImageURL(tag.artist))

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)