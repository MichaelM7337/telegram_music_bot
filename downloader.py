import yt_dlp


def youtubeSongDownloader(video_link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '.\\Music\\%(title)s.%(ext)s',
        'ffmpeg_location': r'C:\ffmpeg\bin',  # Specify the location of ffmpeg
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])