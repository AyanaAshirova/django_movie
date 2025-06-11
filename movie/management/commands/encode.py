import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from movie.models import Movie


class Command(BaseCommand):
    help = 'Optimize Video'

    def handle(self, *args, **options):

        try:
            # id 5
            obj = Movie.objects.filter(status='pending').first
            if obj:
                print(obj.id)
                obj.status = 'processing'
                obj.is_running = True
                obj.save()
                input_video_path = obj.video_4k.path

                output_dir = os.path.join(os.path.dirname(input_video_path), 'hls_output')
                os.makedirs(output_dir, exist_ok=True)
                output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
                output_hls_path = os.path.join(output_dir, output_filename)

                cmd = [
                    'ffmpeg',
                    '-i',
                    input_video_path,
                    '-c:v', 'h264',
                    '-c:a', 'aac',
                    '-hls_time', '5',
                    '-hls_list_size', '0',
                    '-hls_base_url', '{{ dynamic_path }}/',
                    '-movflags',
                    '+faststart',
                    '-y',
                    output_hls_path
                ]

                subprocess.run(cmd, check=True)

                obj.hls = output_hls_path
                obj.status = 'completed'
                obj.is_running = False
                obj.save()

        except Exception as e:
            raise CommandError(e)

    
