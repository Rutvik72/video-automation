from builder import build, getCaption, getRandomVideo, getQuote

# randomQuoteStr = "Prefer to be defeated in the presence of the wise than to excel among fools. - Dogen"
randomVideoID = getRandomVideo()
randomQuote = getQuote()
# for i in idList:
#      clip = me.VideoFileClip(pathToVideos + str(i) + ".mp4")
#      print(i, clip.size)
quoteCaption = getCaption(randomQuote)

videoName = build(randomQuote, randomVideoID)
print(videoName)