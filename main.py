from builder import build, getCaption, getRandomVideo, getQuote
from publisher import youtube

# quote = "Prefer to be defeated in the presence of the wise than to excel among fools. - Dogen"
videoID = getRandomVideo()
quote = getQuote()
quoteStr = quote['q'] + " - " + quote['a']
# for i in idList:
#      clip = me.VideoFileClip(pathToVideos + str(i) + ".mp4")
#      print(i, clip.size)
quote_title, caption = getCaption(quoteStr)

videoName = build(quote, videoID)

video_data = {
    "video_title": quote_title,
    "video_name": "./src/readytopost/" + videoName,
    "quote": quoteStr,
    "caption": caption
}


youtube(video_data)

# print(videoName)
# print(caption)