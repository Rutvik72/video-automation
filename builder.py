import random
import os
import requests
import google.generativeai as genai
import json
from pexelsapi.pexels import Pexels

# Constants
GENAI_API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"
PEXEL_API_KEY = "5vDSTVQlrm84J9teecafE7XDM6fZCqLe6U9hDdVLenn2Az6SRRzcV6U6"

def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    return quote

def getCaption(quote):

    genai.configure(api_key=GENAI_API_KEY)
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
    pexel = Pexels(PEXEL_API_KEY)
    response = pexel.search_videos(query='nature', orientation='portrait', page=1, per_page=5)
    print(response['videos'][0]["id"])
    get_video = pexel.get_video(get_id=response['videos'][0]["id"])
    print(get_video)
    download_video = requests.get("https://www.pexels.com/video/" + str(get_video["id"]) + "/download/")
    with open(str(get_video['id']), 'wb') as outfile:
        outfile.write(download_video.content)
    return

def getRandomMusic():
    return

def build():
    # get all the elements
    # print(getCaption(getQuote()))
    getRandomVideo()

    # build video from the elements
    return


if __name__ == "__main__":
    build()