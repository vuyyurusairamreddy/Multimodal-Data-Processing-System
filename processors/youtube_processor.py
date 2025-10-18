# youtube_processor placeholder
import yt_dlp
import os
from processors.audio_processor import process_audio

def download_youtube_audio(youtube_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_id = info['id']
            audio_file = os.path.join(output_dir, f"{video_id}.mp3")
            
            return audio_file, info
    
    except Exception as e:
        return None, None

def process_youtube_video(youtube_url, output_dir):
    audio_file, info = download_youtube_audio(youtube_url, output_dir)
    
    if audio_file and os.path.exists(audio_file):
        transcription, metadata = process_audio(audio_file)
        
        metadata.update({
            'title': info.get('title', 'Unknown'),
            'uploader': info.get('uploader', 'Unknown'),
            'duration': info.get('duration', 0),
            'url': youtube_url
        })
        
        return transcription, metadata
    else:
        return "Failed to download YouTube video", {}
