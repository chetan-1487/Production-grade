import os
import uuid
from yt_dlp import YoutubeDL
from datetime import datetime
from typing import Dict, Tuple
from sqlalchemy.orm import Session

# Save to Desktop/Downloads
BASE_DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
os.makedirs(BASE_DOWNLOAD_DIR, exist_ok=True)

def download_video(url: str, quality: str = '1080', file_format: str = 'mp4') -> tuple:
    video_id = str(uuid.uuid4())
    extension = "mp3" if file_format == "mp3" else file_format
    output_path = os.path.join(BASE_DOWNLOAD_DIR, f"{video_id}.%(ext)s")

    if file_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
        }
    else:
        try:
            int_quality = int(quality)
        except ValueError:
            raise RuntimeError(f"Invalid quality value: {quality}. Must be 360, 480, 720, 1080, etc.")

        format_string = (
            f"bestvideo[height<={int_quality}][ext={file_format}]+"
            f"bestaudio[ext=m4a]/best[ext={file_format}]/best"
        )

        ydl_opts = {
            'format': format_string,
            'outtmpl': output_path,
            'merge_output_format': file_format,
            'noplaylist': True,
            'quiet': True,
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                raise RuntimeError("Failed to extract video information.")

        filepath = os.path.expanduser(f"~/Downloads/{video_id}.{extension}")

        metadata = {
            "id": video_id,
            "title": info.get("title"),
            "duration": format_duration(info.get("duration", 0)),
            "views": info.get("view_count", 0),
            "likes": info.get("like_count", 0),
            "channel": info.get("uploader"),
            "thumbnail_url": info.get("thumbnail"),
            "published_date": datetime.strptime(info.get("upload_date", "19700101"), "%Y%m%d").date(),
        }

        return filepath, metadata
    except Exception as e:
        raise RuntimeError(f"Download failed: {str(e)}")


def format_duration(seconds: int) -> str:
    mins, secs = divmod(seconds, 60)
    return f"{mins}m{secs}s"