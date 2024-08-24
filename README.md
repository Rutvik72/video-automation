# Video Automation (NEW: Youtube Automation)

## Current Structure

### main.py - Builds data object that will be sent to publisher.py to be published. 


### builder.py - Contains helper functions that call necessary API's to return a video, and a caption.

### publisher.py - Right now it is configured to only post it as shorts, which will be updated to post full videos as well.

### upload_video.py - Youtube uploading video file, which sends request to google authentication and its apiclient to process the request.
Right now it is setup to post on Youtube, Instagram and TikTok, however it will be modified to upload and work with only Youtube. 


## Update Coming

- Integrate AWS Lambda for serverless computation. Although there will be a Lambda Invocation file that will invoke the Lambda function.
However, since lambda allows upto 10GB of onboard memory, we will only need S3 to store raw video files. 
The final video file can be pushed directly to youtube. We may require DynamoDB if we choose to store the raw videos locally. 
DynamoDB will be then used to store all the names of the raw video so that we can select a random video, 
functionally that is accomplished by a static list currently.

Once the AWS integration is complete, a front end will be hosted on amplify, because its free and for learning purposes.



## Helpful resources (incomplete see the Notion documentation)
GEN-AI = "pip install google-generativeai"
Pexel = "pip install pexels-api-py" link = https://pypi.org/project/pexels-api-py/