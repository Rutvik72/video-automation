import random
import os
import requests
import google.generativeai as genai
# import cohere

import json

# Constants
API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"

def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    # print(quote)
    return quote

def getCaption(quote):
    inputMessage = quote['q'] + " - " + quote['a']
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

    prompt = quote['q'] + " - " + quote['a'] + """
        Create a caption for the followiong quote:
        
        Using this JSON scheme:
            Caption Text = {"caption_text", str},
            Hashtags = {"hashtags": str}

        1. caption should be only text without hashtag, 
        2. hashtag should only have hashtags
    """

    response = model.generate_content(prompt).text
    caption = parseMessageText(response)
    return response

def parseMessageText(response):
    response_json = json.loads(response)
    return response_json['caption_text'] + " " + response_json['hashtags']

def getRandomVideo():
    return

def getRandomMusic():
    return

def build():
    # get all the elements
    print(getCaption(getQuote()))

    # build video from the elements
    return


if __name__ == "__main__":
    build()