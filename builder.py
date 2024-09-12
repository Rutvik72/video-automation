import datetime
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
import api.apikeys as HIDDEN
import boto3

# GenAi configuration
genai.configure(api_key=HIDDEN.GENAI_API_KEY)
safety_settings = {
    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH : genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=HIDDEN.ACCESS_KEY,
    aws_secret_access_key=HIDDEN.SECRET_ACCESS_KEY,
    region_name=HIDDEN.REGION
)

# Constants
# dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# pathToVideos = os.path.join(dir_path, "assets\\videos\\")
# pathTo_readytopost = os.path.join(dir_path, "src\\readytopost\\")
pathTo_readytopost = "./src/readytopost/"
pathToStaging = "./assets/staging/"

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

def combineVideoText(quote, author, randomVideoPath):

    clip = me.VideoFileClip(randomVideoPath)
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
    print(response_json)
    try:
        quote_title = response_json["quote_title"]
        quote_caption = response_json['caption_text'] + " " + response_json['hashtags']
    except KeyError:
        quote_title = response_json["Quote Title"]["quote_title"]
        quote_caption = response_json['Caption Text']['caption_text'] + " " + response_json['Hashtags']['hashtags']
    return quote_title, quote_caption

def checkForNewVideos():
    pexel = Pexels(HIDDEN.PEXEL_API_KEY)
    queryList = ['peaceful', 'cars', 'urban architecture', 'nature']
    new_videos = []
    
    # Loop through each query
    for query in queryList:
        try:
            # Use pexel.search_videos() to filter videos by 'portrait' orientation
            response = pexel.search_videos(query=query, orientation='portrait', page=1, per_page=5)
            
            if response['videos']:  # Check if the response contains videos
                videos = response['videos']
                
                # Process each video
                for video in videos:
                    video_id = video['id']
                    video_file_name = f"videos/{video_id}.mp4"

                    # Check if the video already exists in the S3 bucket
                    try:
                        s3_client.head_object(Bucket=HIDDEN.BUCKET_NAME, Key=video_file_name)
                        print(f"Video {video_id} already exists in S3.")
                    except s3_client.exceptions.ClientError:
                        # Select the appropriate video file with a width >= 500px
                        minWidthIndex = 0
                        while video['video_files'][minWidthIndex]['width'] < 500:
                            minWidthIndex += 1
                        video_url = video['video_files'][minWidthIndex]['link']

                        # Download and upload the video to S3
                        video_content = requests.get(video_url)
                        if video_content.status_code == 200:
                            s3_client.put_object(Bucket=HIDDEN.BUCKET_NAME, Key=video_file_name, Body=video_content.content)
                            print(f"Uploaded new portrait video {video_id} to S3.")
                            new_videos.append(video_id)
        except Exception as e:
            print(f"Error fetching videos for query {query}: {str(e)}")

    # Return whether any new videos were added
    return bool(new_videos)


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
    prompt = quote + """
        Create a caption that expands on the quote, no more than one sentence.
        Also give me a quote title, no more than 2 words.
        Using this JSON scheme:
            Quote Title = {"quote_title", str}
            Caption Text = {"caption_text", str},
            Hashtags = {"hashtags": str}
        1. caption should only have text no hashtags
        2. hashtag should only have hashtags
    """
    
    try:
        response = model.generate_content(prompt).text
        quote_title, caption = parseMessageText(response)
    except UnicodeEncodeError:
        caption = "Follow for more daily quotes and motivation. #power #mind #peace #motivation"

    return quote_title, caption

def getRandomVideo():
    # Call checkForNewVideos first
    today = datetime.datetime.today().weekday()
    
    if today == 4:  # 4 represents Friday
        print("Today is Friday. Checking for new videos...")
        new_videos_added = checkForNewVideos()
    else:
        print("Today is not Friday. Skipping video check.")

    # List all video files in the 'videos' folder in S3
    response = s3_client.list_objects_v2(Bucket=HIDDEN.BUCKET_NAME, Prefix='videos/')

    if 'Contents' not in response:
        raise Exception("No videos found in the S3 bucket.")
    
    # Get list of all .mp4 files
    video_files = [item['Key'] for item in response['Contents'] if item['Key'].endswith('.mp4')]

    if not video_files:
        raise Exception("No video files found in the 'videos' folder.")
    
    # Select a random video
    random_video_file = random.choice(video_files)

    # # Lambda's /tmp directory to download the video
    # local_video_path = f"/tmp/{random_video_file.split('/')[-1]}"
    local_video_path = f"{pathToStaging}{random_video_file.split('/')[-1]}"
    
    # # Download the video from S3 into the /tmp directory
    s3_client.download_file(HIDDEN.BUCKET_NAME, random_video_file, local_video_path)

    return local_video_path  # Return local video path for processing

def getRandomMusic():
    return

################
#Builder Function
################
def build(randomQuote, randomVideoPath):
    # The build function is used to centralize the creation of new videos
    # based on quote recieved and video picked

    try:
        videoName = combineVideoText(randomQuote['q'], randomQuote['a'], randomVideoPath)
    except OSError:
        videoName = combineVideoText(randomQuote['q'], randomQuote['a'], randomVideoPath)

    return videoName

