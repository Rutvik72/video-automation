import random
import os
import requests
import google.generativeai as genai
import json
import pprint
from pexelsapi.pexels import Pexels
# from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, ColorClip, VideoClip, VideoFileClip
import moviepy.editor as me
import moviepy.video as mv
import textwrap
from PIL import ImageFont

# Constants
GENAI_API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"
PEXEL_API_KEY = "5vDSTVQlrm84J9teecafE7XDM6fZCqLe6U9hDdVLenn2Az6SRRzcV6U6"
idList = [5896379, 4812203, 5147455, 8856785, 8859849]
path = "./assets/videos/"

#Helper Functions

def soft_wrap_text(
    text: str, 
    fontsize: int, 
    letter_spacing: int, 
    font_family: str, 
    max_width: int,
):
    # Note that font_family has to be an absolut path to your .ttf/.otf
    image_font = ImageFont.truetype(font_family, fontsize) 

    # I am not sure my letter spacing calculation is accurate
    text_width = image_font.getlength(text) + (len(text)-1) * letter_spacing
    print(len(text))
    print(text_width)
    letter_width = text_width / len(text)

    if text_width < max_width:
        return text

    max_chars = max_width / letter_width
    wrapped_text = textwrap.fill(text, width=max_chars)
    return wrapped_text

def combineVideoText():

    clip = me.VideoFileClip(path + "5147455.mp4")
    clip_duration = clip.duration
    print(clip.size)
    width = clip.size[0]
    height = clip.size[1]
    print(clip_duration)
    wrap_title = soft_wrap_text("You must be the change you wish to see in the world. -Mahatma Gandhi",
                                font_family="arial.ttf",
                                fontsize=60,
                                letter_spacing=8,
                                max_width=width-100)
    
    print(wrap_title)
    txt_clip = (me.TextClip(wrap_title, fontsize=60, color='yellow',kerning=8, size=(width, height))
                .set_duration(clip_duration)
                .set_position("center"))
    txt_fading = txt_clip.crossfadein(1)
    video = me.CompositeVideoClip([clip, txt_fading])
    video.write_videofile("./src/text.mp4", fps=30)
    
    return

def parseMessageText(response):
    response_json = json.loads(response)
    return response_json['caption_text'] + " " + response_json['hashtags']

def videoIdInList(id):
    if id not in idList:
        idList.append(id)
        return False
    return True

def checkForNewVideos():
    pexel = Pexels(PEXEL_API_KEY)
    path = "./assets/videos/"
    newVideosFlag = False

    response = pexel.search_videos(query='nature', orientation='portrait', page=1, per_page=5)
    # pprint.pp(response)
    for videos in response["videos"]:
        id = videos["id"]
        if not videoIdInList(id):
            get_video = pexel.get_video(get_id=id)
            download_video = requests.get(get_video['video_files'][0]['link'], stream=True)
            with open(path + str(get_video["id"]) +".mp4", 'wb') as outfile:
                for chunk in download_video.iter_content(chunk_size=256):
                    outfile.write(chunk)
            newVideosFlag = True
    return newVideosFlag


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

def getRandomVideo():
    
    if checkForNewVideos():
        randomVideoId = idList[-1]
    else:
        randomVideoId = random.choice(idList)
    print(randomVideoId)
    combineVideoText()
    return randomVideoId


def getRandomMusic():

    return



#Builder Function
def build():
    # get all the elements
    # print(getCaption(getQuote()))
    getRandomVideo()

    # build video from the elements
    return


if __name__ == "__main__":
    build()