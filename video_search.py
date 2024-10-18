from youtubesearchpython import VideosSearch


def search(message):
    video = VideosSearch(message)
    return video.result()['result']
