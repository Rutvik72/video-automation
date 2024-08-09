import random
import os
import requests
import cohere

quote = None

def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    return quote

def getCaption():
    inputMessage = "Caption for the following quote, first caption then hashtags: " + quote['q'] + " - " + quote['a']
    co = cohere.Client("2haSGJan1MkH76qxSSVGsqQ3uPc1cIsD5hcIT5vi")
    response = co.chat(
        message=inputMessage
    )
    return response

def getRandomVideo():
    return

def getRandomMusic():
    return

class builder:
    # def __init__(self, video, music, caption, quote) -> None:
    #     self.video = video
    #     self.music = music
    #     self.caption = caption
    #     self.quote = quote

    
    def build():
        return


if __name__ == "__main__":
    build()