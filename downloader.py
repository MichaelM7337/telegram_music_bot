import os
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch


# Function to search YouTube for a song
def search_youtube(song_name):
    try:
        # Perform the search on YouTube
        videos_search = VideosSearch(song_name, limit=1)
        result = videos_search.result()

        if result and result['result']:
            video_info = result['result'][0]
            video_url = video_info['link']
            print(f"Found YouTube video: {video_info['title']} ({video_url})")
            return video_url
        else:
            print("No video found for the song name.")
            return None
    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return None


# Function to download YouTube video
def download_youtube_video(youtube_link):
    try:
        yt = YouTube(youtube_link)
        # Download the highest quality audio stream
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=".")

        print(f"Downloaded video: {out_file}")
        return out_file
    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None


# Function to convert video to MP3
def convert_to_mp3(video_file):
    try:
        base, ext = os.path.splitext(video_file)
        mp3_file = base + '.mp3'

        # Convert to mp3 using pydub
        audio = AudioSegment.from_file(video_file)
        audio.export(mp3_file, format="mp3")

        # Optionally delete the original video file
        os.remove(video_file)

        print(f"Converted to MP3: {mp3_file}")
        return mp3_file
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None


# Main function to search, download, and convert
def download_music_by_name(song_name):
    # Search for the song on YouTube
    youtube_link = search_youtube(song_name)

    if youtube_link:
        # Download the YouTube video
        video_file = download_youtube_video(youtube_link)

        if video_file:
            # Convert to MP3
            mp3_file = convert_to_mp3(video_file)

            if mp3_file:
                print(f"Music downloaded and saved as MP3: {mp3_file}")
            else:
                print("Failed to convert video to MP3.")
        else:
            print("Failed to download video.")
    else:
        print("No YouTube link found for the song.")

download_youtube_video('')