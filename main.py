from builder import build, getCaption, getRandomVideo, getQuote
from publisher import youtube

# quote = "Prefer to be defeated in the presence of the wise than to excel among fools. - Dogen"
def lambda_handler(event, context):
    try:
        # Get a random video from S3 or local source
        videoPath = getRandomVideo()

        # Get a random quote
        print("Grabbing Quote")
        quote = getQuote()
        quoteStr = quote['q'] + " - " + quote['a']

        # Generate caption and title
        print("Generating Title")
        quote_title, caption = getCaption(quoteStr)

        # Build the video with the quote
        print("Building Video")
        videoName = build(quote, videoPath)

        # Prepare the data to publish the video
        video_data = {
            "video_title": quote_title,
            "video_name": videoName,
            "quote": quoteStr,
            "caption": caption
        }

        # Publish the video to YouTube
        print("Publishing Video")
        youtube(video_data)

        return {
            'statusCode': 200,
            'body': f"Successfully created and published video: {videoName}"
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

lambda_handler(200, "test")