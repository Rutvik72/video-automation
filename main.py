from builder import build, getCaption, getRandomVideo, getQuote
from publisher import youtube

# quote = "Prefer to be defeated in the presence of the wise than to excel among fools. - Dogen"
videoPath = getRandomVideo()
quote = getQuote()
quoteStr = quote['q'] + " - " + quote['a']

quote_title, caption = getCaption(quoteStr)
print(videoPath)


videoName = build(quote, videoPath)

video_data = {
    "video_title": quote_title,
    "video_name": "./src/readytopost/" + videoName,
    "quote": quoteStr,
    "caption": caption
}

youtube(video_data)

# print(videoName)
# print(caption)