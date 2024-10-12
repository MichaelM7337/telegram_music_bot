from youtubesearchpython import VideosSearch

def search(message):
    video = VideosSearch(message)
    videos = []
    video.next()
    videos.append(video.result()['result'])
    return videos