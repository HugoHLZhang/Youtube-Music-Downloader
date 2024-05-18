import os
import subprocess
import re
from pytube import YouTube
from pytube import Playlist

def convert_mp4_to_m4a(input_file, output_file, video_data):
    try:
        metadata_args = []
        for key, value in video_data.items():
            metadata_args.extend(['-metadata', f'{key}={value}'])

        subprocess.run(['ffmpeg', '-i', input_file, '-c:a', 'aac', '-strict', 'experimental', '-b:a', '64k', *metadata_args, output_file])
        print('Conversion completed successfully!')
    except Exception as e:
        print(f'Error converting file: {str(e)}')

def download_and_convert(video_url, folder_path):
    try:
        # Create a YouTube object for the video
        video = YouTube(video_url)

        # Select the highest resolution available
        stream = video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').asc().first()
        title = re.sub(r'[^\w\-_\. ]', '_', video.title)
        f_name = f"{title}"
        
        # Check if the file already exists in the folder
        if os.path.exists(os.path.join(folder_path, f_name + '.m4a')):
            print(f"File '{f_name}.m4a' already exists. Skipping download and conversion.")
            return

        # Download the video
        print(f"Downloading: {video.title}")
        video_stream = stream.download(output_path=folder_path, filename=f_name + '.mp4')
        print(video_stream + " Download completed!")

        # Retrieve video data
        video_data = {
            'title': video.title,
            'artist': video.author,
        }

        # Convert the downloaded video to M4A
        m4a_output_path = os.path.join(folder_path, f_name + '.m4a')
        convert_mp4_to_m4a(video_stream, m4a_output_path, video_data)

        # Delete the downloaded MP4 file
        try:
            os.remove(video_stream)
            print("File deleted successfully!")
        except FileNotFoundError:
            print(f"File '{video_stream}' not found.")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")

    except Exception as e:
        print(f"Error processing video: {str(e)}")

# Enter the playlist URL here
playlist_url = input("Enter playlist URL: ")

# Create a Playlist object
playlist = Playlist(playlist_url)

# Enter the folder path where you want to save the videos
folder_path = re.sub(r'[^\w\-_\. ]', '_', playlist.title)

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Iterate over each video in the playlist
for video_url in playlist.video_urls:
    download_and_convert(video_url, folder_path)
