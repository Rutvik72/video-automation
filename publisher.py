#imports
from upload_video import upload_video


def tiktok():
    return

def youtube(video_data):
    video_data = {
        "file": video_data["video_name"],
        "title":  video_data["video_title"],
        "description": "#shorts\n" +  video_data["caption"],
        "keywords":"motivation, quotes",
        "privacyStatus":"private"
    }
    print(video_data)
    upload_video(video_data)
    return

def instagram():
    return

def publishToAll():
    return

def moveTo():
    return

if __name__ == "__main__":
    publishToAll()