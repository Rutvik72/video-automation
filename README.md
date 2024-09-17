# Automated YouTube Video Creator and Publisher

This project automates the process of creating, editing, and publishing videos to YouTube by leveraging multiple APIs and cloud services. The goal is to streamline video production, combining inspirational quotes, video footage, and captions into a polished, shareable video, which is automatically uploaded to a YouTube channel. The project is designed to run in a serverless environment using AWS Lambda and Docker for scalability and efficiency.

## Key Components:

### 1. Video Generation
- **MoviePy** is used to process and edit videos. The code automatically combines stock video footage from Pexels with text overlays (quotes) and background effects.
- **FFmpeg** and **ImageMagick** are integrated for video encoding and image manipulation, ensuring high-quality output for YouTube-ready content.

### 2. APIs for Content
- **Pexels API**: Automatically retrieves video footage based on predefined themes like "peaceful," "cars," and "nature" to serve as the background for the generated videos.
- **ZenQuotes API**: Dynamically fetches inspirational or motivational quotes, which are added as text overlays to the videos.
- **Gemini AI API**: Used to generate captions and hashtags for YouTube uploads, with custom logic to handle API limitations and ensure well-formatted responses.

### 3. Automation and Orchestration
The project is structured into three primary workflows:
- **Video Builder**: Manages the logic for assembling the video, including fetching videos, adding quotes, and rendering the final output.
- **Video Publisher**: Publishes videos to YouTube, handling metadata like titles, descriptions, and privacy settings.
- **Orchestration**: Coordinates between the video builder and publisher, ensuring that the appropriate content is used and formatted correctly.

### 4. Cloud Infrastructure
- **AWS S3** is used to store both the raw video footage and the final processed videos. Videos are retrieved and processed dynamically from S3, ensuring scalability and data integrity.
- **AWS Lambda**: The serverless compute engine that processes and uploads the videos. Initially, there were challenges with Lambda’s deployment size limits, but Docker was integrated to package dependencies into a container hosted in **AWS ECR**. This approach allowed for more complex video processing workflows while staying within Lambda’s execution environment constraints.

### 5. YouTube Integration (OAuth2 Authentication)
- The **YouTube Data API** is used to upload videos directly to YouTube. Authentication is handled using **OAuth2**. Initially, browser-based authentication posed issues in the serverless environment, but the solution was to store OAuth tokens securely and reuse them in AWS Lambda to avoid repeated manual authentication.

### 6. Docker Integration
- The final deployment uses a **Docker container** to manage dependencies and overcome AWS Lambda’s size limitations. The Docker image, once built and tested locally, is pushed to **Amazon ECR**, where Lambda can pull the image to execute the video generation and upload tasks.

### 7. Scalability and Modularity
- The system is designed to handle multiple video types and automate the workflow from content generation to publishing. The architecture can be further scaled by breaking each task (e.g., fetching videos, generating captions, uploading) into individual Lambda functions if memory constraints arise.
- This modular approach ensures that as more features (like background music generation) are added, the project remains efficient and scalable.

## Summary
This project is a fully automated video creation and publishing pipeline, integrating various APIs for content generation, video processing tools like MoviePy and FFmpeg, and cloud services like AWS Lambda and S3. The project is deployed using Docker to manage dependencies and runs seamlessly in a serverless environment. It is capable of generating polished, customized YouTube videos without manual intervention, making it ideal for content creators looking to scale their video production workflows.

## Resources
- [Best way to choose a random file from a directory](https://stackoverflow.com/questions/701402/best-way-to-choose-a-random-file-from-a-directory)
- [ZenQuotes API Documentation](https://docs.zenquotes.io/bring-peace-to-your-telegram-channel-with-zenquotes-and-python/)
- [Pyright Configuration Guide](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingImports)
- [Google AI API Key Setup](https://aistudio.google.com/app/u/5/apikey)
- [Gemini AI JSON Mode Documentation](https://ai.google.dev/gemini-api/docs/json-mode?lang=python)
- [Python String to JSON Conversion](https://www.freecodecamp.org/news/python-json-how-to-convert-a-string-to-json/)
- [Python pprint Module Documentation](https://docs.python.org/3/library/pprint.html)
- [Combining video files with text using MoviePy](https://stackoverflow.com/questions/64630555/python-adding-text-and-combining-video-files)
- [MoviePy Composite Video and Cross Fade-In Effects](https://www.geeksforgeeks.org/moviepy-composite-video-adding-cross-fade-in-effect/)
- [Colab Example: ImageMagick and Video Processing](https://colab.research.google.com/drive/1PLYFiE0q3dySe-LLzj7oGmpLQksczu__?usp=sharing#scrollTo=Qq1-cjkilSif)
- [ImageMagick Download](https://imagemagick.org/script/download.php#windows)
- [Handling MoviePy and ImageMagick Errors](https://stackoverflow.com/questions/65136644/getting-error-about-imagemagick-with-python-moviepy-when-i-try-add-text-clip)
- [MoviePy Documentation: Compositing](https://zulko.github.io/moviepy/getting_started/compositing.html)
- [Text Wrapping with MoviePy](https://stackoverflow.com/questions/75727968/wrap-text-or-add-padding-to-not-touch-video-edges-with-moviepy)
- [Text Wrapping in Python](https://www.w3schools.in/python/examples/text-wrapping-in-python)
- [Pillow Documentation: ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html)
- [Gemini AI Safety Settings](https://ai.google.dev/gemini-api/docs/safety-settings)
- [Generate Content with Google AI](https://ai.google.dev/api/generate-content)
- [YouTube Video on OAuth2 and Google APIs](https://www.youtube.com/watch?v=UPkDjhhfVcY)
- [MoviePy Issue Tracker](https://github.com/Zulko/moviepy/issues/1966)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2/web-server#python_3)


## Other 
GEN-AI = "pip install google-generativeai"
Pexel = "pip install pexels-api-py" link = https://pypi.org/project/pexels-api-py/