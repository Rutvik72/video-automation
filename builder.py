import random
import requests
import google.generativeai as genai
import json
import pprint
from pexelsapi.pexels import Pexels
import moviepy.editor as me
import textwrap
from PIL import ImageFont
from time import gmtime, strftime
import math
import os
from pathlib import Path

# API - temporary and will be changed
GENAI_API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"
PEXEL_API_KEY = "5vDSTVQlrm84J9teecafE7XDM6fZCqLe6U9hDdVLenn2Az6SRRzcV6U6"

# GenAi configuration
genai.configure(api_key=GENAI_API_KEY)
safety_settings = {
    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Constants
idList = [4678261, 7297870, 6550972, 8045821, 5145199, 3226454, 5198956, 5544054, 5893890, 6521673, 5829173, 5829170, 5828488, 5829168, 5896379, 4812203, 5147455, 8856785, 8859849]
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# pathToVideos = os.path.join(dir_path, "assets\\videos\\")
# pathTo_readytopost = os.path.join(dir_path, "src\\readytopost\\")
pathToVideos = "./assets/videos/"
pathTo_readytopost = "./src/readytopost/"

# Text Constants
textFont = "./assets/font/Lato-Black.ttf"
# print(textFont)
# print(me.TextClip.list('font'))
textFontSizeLambda = lambda clipWidth: pickFontSize(clipWidth)
textColor = 'yellow'
textCharSpace = 5
clip_Length = 15

################
# Helper Functions
################
def pickFontSize(clipWidth):
    dictOfFontSize = {
        600: 35,
        700: 50,
        900: 60,
        1100: 80,
        1500: 100,
        2000: 125
    }

    for key in dictOfFontSize:
        if clipWidth < key:
            fontSize = dictOfFontSize[key]
            break
        else:
            fontSize = 135

    return fontSize

def soft_wrap_text(
    text: str, 
    fontsize: int, 
    letter_spacing: int, 
    font_family: str, 
    max_width: int):

    image_font = ImageFont.truetype(font_family, fontsize) 
    text_width = image_font.getlength(text) + (len(text)-1) * letter_spacing

    letter_width = text_width / len(text)

    if text_width < max_width:
        return text

    max_chars = max_width / letter_width
    wrapped_text = textwrap.fill(text, width=max_chars)
    return wrapped_text

def combineVideoText(quote, author, videoID):

    clip = me.VideoFileClip(pathToVideos + str(videoID) + ".mp4")
    clip_duration = clip.duration

    clipLength = 15/clip_duration
    if clipLength > 1:
        numOfClips = [clip] * math.ceil(clip_Length)
        clip = me.concatenate_videoclips(numOfClips)

    clip = clip.subclip(0,15)
    clip_duration = clip.duration
    clip = clip.fx(me.vfx.colorx, 0.5)
    width, height = clip.size[0], clip.size[1]
    textFontSize = textFontSizeLambda(width)

    wrap_title = soft_wrap_text(quote,
                                font_family=textFont,
                                fontsize=textFontSize,
                                letter_spacing=textCharSpace,
                                max_width=width-100)
    
    wrap_author = soft_wrap_text(" - " + author,
                                font_family=textFont,
                                fontsize=textFontSize,
                                letter_spacing=textCharSpace,
                                max_width=width-100)
    
    wrapped_text = wrap_title + "\n\n" + wrap_author
    pprint.pp(wrapped_text)
    
    txt_clip = (me.TextClip(wrapped_text, 
                            fontsize=textFontSize,
                            font=textFont,
                            color=textColor,
                            kerning=textCharSpace, 
                            size=(width, height))
                .set_duration(clip_duration)
                .set_position("center"))
    
    txt_fading = txt_clip.crossfadein(1)
    video = me.CompositeVideoClip([clip, txt_fading])
    videoName = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    video.write_videofile(pathTo_readytopost + videoName + ".mp4", fps=30)
    
    return  videoName + ".mp4"

def parseMessageText(response):
    response_json = json.loads(response)
    return response_json['caption_text'] + " " + response_json['hashtags']

def videoIdInList(id):
    if id not in idList:
        idList.append(id)
        return False
    return True

def checkForNewVideos(queryTag):
    pexel = Pexels(PEXEL_API_KEY)
    newVideosFlag = False
    response = pexel.search_videos(query=queryTag, orientation='portrait', page=1, per_page=5)
    
    for videos in response["videos"]:
        id = videos["id"]
        if not videoIdInList(id):
            get_video = pexel.get_video(get_id=id)
            minWidthIndex = 0
            while get_video['video_files'][minWidthIndex]['width'] < 500:
                minWidthIndex += 1

            download_video = requests.get(get_video['video_files'][minWidthIndex]['link'], stream=True)

            with open(pathToVideos + str(get_video["id"]) +".mp4", 'wb') as outfile:
                for chunk in download_video.iter_content(chunk_size=256):
                    outfile.write(chunk)
            newVideosFlag = True

    return newVideosFlag

################
# Getter functions
################
def getQuote():
    # The getQuote function calls the ZenQuote API which returns a json
    # Returns string in json formate

    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    return quote


def getCaption(quote):
    # The getCaption function calls on the Googles Gemini AI, known as generative model.
    # A prompt containing the quote and with reponse guidelines is sent to Gemini, which returns
    # a caption in json string format. Then a parse helper function is called to grab the right string
    # and return caption with hashtag as singular string.
    # Returns string
    
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}, safety_settings=safety_settings)
    prompt = quote['q'] + " - " + quote['a']  + """
        Create a caption
        Using this JSON scheme:
            Caption Text = {"caption_text", str},
            Hashtags = {"hashtags": str}
        1. caption should only have text no hashtags
        2. hashtag should only have hashtags
    """
    
    try:
        response = model.generate_content(prompt).text
        caption = parseMessageText(response)
    except UnicodeEncodeError:
        caption = "Follow for more daily quotes and motivation. #power #mind #peace #motivation"

    return caption

def getRandomVideo():
    # The getRandomVideo function checks to see if there are new videos for 4 different searches,
    # if so, the new videos are downloaded to the assests/videos folder and the lastest one is picked,
    # otherwise, it randomly selects a video from idList and returns it.
    # Returns int

    queryList = ['peaceful', "cars", "urban architecture", "nature"]
    newVideoBool = False
    for query in queryList:
        newVideoBool = checkForNewVideos(query) | newVideoBool

    if newVideoBool:
        randomVideoId = idList[-1]
    else:
        randomVideoId = random.choice(idList)
    
    print(idList)

    return randomVideoId

def getRandomMusic():
    return

################
#Builder Function
################
def build(randomQuote, randomVideoID):
    # The build function is used to centralize the creation of new videos
    # based on quote recieved and video picked
    
    try:
        videoName = combineVideoText(randomQuote['q'], randomQuote['a'], randomVideoID)
    except OSError:
        videoName = combineVideoText(randomQuote['q'], randomQuote['a'], randomVideoID)

    return videoName

