import os
import uuid
from yt_dlp import YoutubeDL
from datetime import datetime
from typing import Dict, Tuple
from app.Core.celery_worker.celery_worker import celery_app



QUALITY_MAP = {
    "360p": 360,
    "480p": 480,
    "720p": 720,
    "1080p": 1080,
    "4k": 2160
}


#var list=[360p, 480p, 720p, 1080p, 4K]

# Save to Desktop/Downloads
BASE_DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
os.makedirs(BASE_DOWNLOAD_DIR, exist_ok=True)

'''
if not in list:
    raise RuntimeError(f"Invalid quality value: {quality}. Must be 360, 480, 720, 1080, etc.")
'''

@celery_app.task(name="app.Core.Service.download.download_video")
def download_video(url: str, quality: str = '1080p', file_format: str = 'mp4') -> list:  #tuple
    # video_id = str(uuid.uuid4())
    extension = "mp3" if file_format == "mp3" else file_format
    output_path = os.path.join(BASE_DOWNLOAD_DIR, f"%(id)s.%(ext)s")
    result=[]

    if file_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': False,
            'quiet': True,
            'playlistend': 5,
            'match_filter': ('duration <= 18000 && (filesize <= 3221225472 || filesize_approx <= 3221225472)'),
        }
    else:
        if quality not in QUALITY_MAP:
            raise RuntimeError(f"Invalid quality value: {quality}. Must be 360p, 480p, 720p, 1080p, 4K etc.")
    
        int_quality = QUALITY_MAP[quality]

        format_string = (
            f"bestvideo[height<={int_quality}][ext={file_format}]+"
            f"bestaudio[ext=m4a]/best[ext={file_format}]/best"
        )

        ydl_opts = {
            'format': format_string,
            'outtmpl': output_path,
            'merge_output_format': file_format,
            'noplaylist': False,
            'quiet': True,
            'playlistend': 5,
            'match_filter': ('duration <= 18000 && (filesize <= 3221225472 || filesize_approx <= 3221225472)'),
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if not info:
                raise RuntimeError("Failed to extract video information.")
            entries=info.get("entries",[])
            if not entries:
                entries=[info]
            
            for entry in entries:
                video_id = str(uuid.uuid4())
                file_path = os.path.join(BASE_DOWNLOAD_DIR, f"{video_id}.{extension}")

                metadata = {
                    "id": video_id,
                    "title": entry.get("title"),
                    "duration": format_duration(entry.get("duration", 0)),
                    "views": entry.get("view_count", 0),
                    "likes": entry.get("like_count", 0),
                    "channel": entry.get("uploader"),
                    "thumbnail_url": entry.get("thumbnail"),
                    "published_date": datetime.strptime(entry.get("upload_date", "19700101"), "%Y%m%d").date()
                }

                result.append((file_path, metadata))

        # filepath = os.path.expanduser(f"~/Downloads/{video_id}.{extension}")
       
        # metadata = {
        #     "id": video_id,
        #     "title": info.get("title"),
        #     "duration": format_duration(info.get("duration", 0)),
        #     "views": info.get("view_count", 0),
        #     "likes": info.get("like_count", 0),
        #     "channel": info.get("uploader"),
        #     "thumbnail_url": info.get("thumbnail"),
        #     "published_date": datetime.strptime(info.get("upload_date", "19700101"), "%Y%m%d").date()
        # }

        # return filepath, metadata
        return result
    except Exception as e:
        raise RuntimeError(f"Download failed: {str(e)}")


def format_duration(seconds: int) -> str:
    mins, secs = divmod(seconds, 60)
    return f"{mins}m{secs}s"


# download_video("https://www.youtube.com/watch?v=-mgGnx1p3b8&list=RDMMcl0a3i2wFcc&index=3","1080","mp4")