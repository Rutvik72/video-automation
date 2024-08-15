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
import math

#API - temporary and will be changed
GENAI_API_KEY = "AIzaSyDv0bV2dWMdtEgJOxcCfiWr0lLHlb3QU2U"
PEXEL_API_KEY = "5vDSTVQlrm84J9teecafE7XDM6fZCqLe6U9hDdVLenn2Az6SRRzcV6U6"

# Constants
genai.configure(api_key=GENAI_API_KEY)
safety_settings = {
    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

idList = [4678261, 7297870, 6550972, 8045821, 5145199, 3226454, 5198956, 5544054, 5893890, 6521673, 5829173, 5829170, 5828488, 5829168, 5896379, 4812203, 5147455, 8856785, 8859849]
pathToVideos = "./assets/videos/"

#Text Constants
textFont = "arial.ttf"
textFontSizeLambda = lambda clipWidth: pickFontSize(clipWidth)
textColor = 'yellow'
textCharSpace = 5



#Helper Functions

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

def combineVideoText(quote, author, videoID):

    clip = me.VideoFileClip(pathToVideos + str(videoID) + ".mp4")
    clip_duration = clip.duration

    clipLength = 15/clip_duration
    if clipLength > 1:
        numOfClips = [clip] * math.ceil(clipLength)
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
                            color=textColor,
                            kerning=textCharSpace, 
                            size=(width, height))
                .set_duration(clip_duration)
                .set_position("center"))
    
    txt_fading = txt_clip.crossfadein(1)
    video = me.CompositeVideoClip([clip, txt_fading])
    videoName = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    video.write_videofile("./src/readytopost/" + videoName + ".mp4", fps=30)
    
    return

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


def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    quote = response.json()[0]
    return quote

def getCaption(quote):

    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}, safety_settings=safety_settings)
#['q'] + " - " + quote['a'] 
    prompt = quote + """
        Create a caption
        Using this JSON scheme:
            Caption Text = {"caption_text", str},
            Hashtags = {"hashtags": str}
        1. caption should only have text no hashtags
        2. hashtag should only have hashtags
    """
    print(len(prompt))
    print(prompt)
    
    try:
        response = model.generate_content(prompt).text
        caption = parseMessageText(response)
    except UnicodeEncodeError:
        caption = "Follow for more daily quotes and motivation. #power #mind #peace #motivation"

    return caption

def getRandomVideo():

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


#Builder Function
def build():
    randomQuoteStr = "Prefer to be defeated in the presence of the wise than to excel among fools. - Dogen"
    # randomVideoID = getRandomVideo()
    randomQuote = getQuote()
    # combineVideoText(randomQuote['q'], randomQuote['a'], randomVideoID)
    # for i in idList:
    #      clip = me.VideoFileClip(pathToVideos + str(i) + ".mp4")
    #      print(i, clip.size)
    print(getCaption(randomQuoteStr))

    return


if __name__ == "__main__":
    build()