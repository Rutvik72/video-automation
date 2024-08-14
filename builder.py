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
from time import gmtime, strftime

#API
GENAI_API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"
PEXEL_API_KEY = "5vDSTVQlrm84J9teecafE7XDM6fZCqLe6U9hDdVLenn2Az6SRRzcV6U6"

# Constants
genai.configure(api_key=GENAI_API_KEY)
idList = [5896379, 4812203, 5147455, 8856785, 8859849]
pathToVideos = "./assets/videos/"

#Text Constants
textFont = "arial.ttf"
textFontSizeLambda = lambda clipWidth: pickFontSize(clipWidth)
textColor = 'yellow'
textCharSpace = 5


#Helper Functions

def pickFontSize(clipWidth):
    dictOfFontSize = {
        500: 20,
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
            print(fontSize)
            break
        else:
            fontSize = 160

    return fontSize

def soft_wrap_text(
    text: str, 
    fontsize: int, 
    letter_spacing: int, 
    font_family: str, 
    max_width: int,
):
    
    image_font = ImageFont.truetype(font_family, fontsize) 
    text_width = image_font.getlength(text) + (len(text)-1) * letter_spacing

    letter_width = text_width / len(text)

    if text_width < max_width:
        return text

    max_chars = max_width / letter_width
    wrapped_text = textwrap.fill(text, width=max_chars)
    return wrapped_text

def combineVideoText(quote, videoID):

    clip = me.VideoFileClip(pathToVideos + str(videoID) + ".mp4")
    if clip.duration > 15:
        clip.subclip(0,15)
    clip_duration = clip.duration
    clip.fx(me.vfx.colorx, 1)
    width, height = clip.size[0], clip.size[1]
    textFontSize = textFontSizeLambda(width)
    wrap_title = soft_wrap_text(quote,
                                font_family=textFont,
                                fontsize=textFontSize,
                                letter_spacing=textCharSpace,
                                max_width=width-100)
    
    txt_clip = (me.TextClip(wrap_title, 
                            fontsize=textFontSize, 
                            color=textColor,
                            kerning=textCharSpace, 
                            size=(width, height))
                .set_duration(clip_duration)
                .set_position("center"))
    
    txt_fading = txt_clip.crossfadein(1)
    video = me.CompositeVideoClip([clip, txt_fading])
    videoName = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    print(videoName)
    video.write_videofile("./src/" + videoName + ".mp4", fps=30)
    
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
    newVideosFlag = False

    response = pexel.search_videos(query='nature', orientation='portrait', page=1, per_page=5)
    for videos in response["videos"]:
        id = videos["id"]
        if not videoIdInList(id):
            get_video = pexel.get_video(get_id=id)
            download_video = requests.get(get_video['video_files'][0]['link'], stream=True)
            with open(pathToVideos + str(get_video["id"]) +".mp4", 'wb') as outfile:
                for chunk in download_video.iter_content(chunk_size=256):
                    outfile.write(chunk)
            newVideosFlag = True
    return newVideosFlag


def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    return quote

def getCaption(quote):

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
    return caption

def getRandomVideo():
    
    if checkForNewVideos():
        randomVideoId = idList[-1]
    else:
        randomVideoId = random.choice(idList)
    print(randomVideoId)
    return randomVideoId


def getRandomMusic():

    return


#Builder Function
def build():
    # get all the elements
    # print(getCaption(getQuote()))
    # randomQuoteStr = "You must be the change you wish to see in the world. -Mahatma Gandhi"
    randomVideoID = getRandomVideo()
    randomQuote = getQuote()
    randomQuoteStr = randomQuote['q'] + " - " + randomQuote['a']
    combineVideoText(randomQuoteStr, randomVideoID)
    # for i in idList:
    #      clip = me.VideoFileClip(pathToVideos + str(i) + ".mp4")
    #      print(textFontSize(clip.size[0]))

    # build video from the elements
    print(getCaption(randomQuote))
    return


if __name__ == "__main__":
    build()