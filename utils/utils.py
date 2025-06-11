import os
import subprocess
import json
from django.conf import settings


def get_video_duration(file_path):
    cmd_duration = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-i', file_path
    ]
    result = subprocess.run(cmd_duration, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output_json = json.loads(result.stdout)
    video_length = None
    try:
        for stream in output_json['streams']:
            if stream['codec_type'] == 'video':
                video_length = float(stream['duration'])
                break
    except Exception as e:
        print('Catch Exception while get duration', e)

    return video_length


def get_video_thumbnail(video_path):
    output_dir = os.path.join(settings.MEDIA_ROOT, settings.HLS_DIR_NAME, 'thumbnails')
    output_thumbnail_path = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '_thumbnail.jpg')
    os.makedirs(output_dir, exist_ok=True)
    
    cmd_thumbnail = [
        'ffmpeg',
        '-ss', '1',
        '-i', video_path,
        '-frames:v', '1',
        '-q:v', '2',
        # '-s', '640x360',
        '-update', '1',
        '-y',
        output_thumbnail_path
    ]
    try:
        subprocess.run(cmd_thumbnail, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Thumbnail generation failed with return code {e.returncode}")
        print(f"Command: {e.cmd}")
        print(f"Output: {e.output}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    if os.path.exists(output_thumbnail_path):
        return output_thumbnail_path
    return None

