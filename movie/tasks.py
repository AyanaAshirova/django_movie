
import subprocess
import os
import json
from celery import shared_task
from time import sleep
from celery import Celery
from movie.models import VideoStream, Movie
from utils.utils import get_video_thumbnail
from django.core.files import File
from django.conf import settings

@shared_task
def set_thumbnail(duration, stream_id):
    sleep(duration)

    stream = VideoStream.objects.filter(id=stream_id).first()
    if stream:
        if stream.video and not stream.movie.thumbnail:
            thumbnail_path = get_video_thumbnail(stream.video.path)
            if thumbnail_path and os.path.exists(thumbnail_path):
                print('thumbnail created')
                with open(thumbnail_path, 'rb') as f:
                    stream.movie.thumbnail.save(f'{stream.movie.id}-thumbnail.jpg', File(f))   
                os.remove(thumbnail_path)


@shared_task
def save_recommended_movies(duration, movie_id):
    sleep(duration)

    movie = Movie.objects.filter(id=movie_id).first()
    if movie:
        movie.recommendations.set(movie.get_recommended_movies())
        print("Recommendations saved for: ", movie.title)


@shared_task
def video_encode(duration, steam_id):
    print('Video Encode')

    try:
        sleep(duration)

        stream = VideoStream.objects.filter(id=steam_id).first()
        if stream:
            stream.status = VideoStream.PROCESSING
            stream.is_running = True
            stream.save()
            print('Video Encode')


            input_video_path = os.path.join(settings.MEDIA_ROOT, stream.video.path)
            output_dir = os.path.join(settings.MEDIA_ROOT, f"{settings.HLS_DIR_NAME}/{stream.movie.id}/{stream.resolution}")
            os.makedirs(output_dir, exist_ok=True)

            output_hls_path = os.path.join(output_dir, 'playlist.m3u8')
            if os.path.exists(output_hls_path):
                stream.status = VideoStream.COMPLETED
                stream.hls_path = output_hls_path
                stream.is_running = False
                stream.save()
                return
            
    # ffmpeg -i "{input_path}" -vf scale=-2:{video.resolution.replace('p', '')} \
    # -c:a aac -ar 48000 -b:a 128k -c:v h264 -profile:v main -crf 20 -sc_threshold 0 \
    # -g 48 -keyint_min 48 -hls_time 4 -hls_playlist_type vod \
    # -hls_segment_filename "{output_dir}/segment_%03d.ts" "{output_path}"

        # cmd = [
        #     'ffmpeg',
        #     '-i', input_video_path,
        #     '-c:v', 'h264',
        #     '-c:a', 'aac',
        #     '-hls_time', '5',
        #     '-hls_list_size', '0',
        #     '-hls_base_url', '{{ dynamic_path }}/',
        #     '-movflags',
        #     '+faststart',
        #     '-y',
        #     output_hls_path
        # ]
            cmd = [
                '/usr/bin/ffmpeg',
                '-i', input_video_path,
                '-vf', f'scale=-2:{stream.resolution}',
                '-c:a', 'aac',
                '-ar', '48000',
                '-b:a', '128k',
                '-c:v', 'h264',
                '-profile:v', 'main',
                '-crf', '20',
                '-sc_threshold', '0',
                '-g', '48',
                '-keyint_min', '48',
                '-hls_time', '4',
                '-hls_playlist_type', 'vod',
                '-hls_segment_filename', f'{output_dir}/segment_%03d.ts',
                output_hls_path
            ]

            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


            stream.hls_path = f"{settings.HLS_DIR_NAME}/{stream.movie.id}/{stream.resolution}/playlist.m3u8"
            stream.status = VideoStream.COMPLETED
            stream.is_running = False
            stream.save()
            stream.movie.generate_master_playlist()
            print(stream.status)



    except Exception as e:
        print("Error while encode Video: ", e)



