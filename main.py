import http.server
from PIL import Image
import moviepy.editor as mpy
import os
import glob
import socketserver

def dir_update():
    video_files = glob.glob('*.mp4')
    thumbnail_files = glob.glob('thumbnails/*.jpg')

    for video_file in video_files:
        thumbnail_path = "thumbnails/"+video_file + '.jpg'
        if not os.path.exists(thumbnail_path):
            generate_thumbnail(video_file, thumbnail_path)
            video_link = f'<li><a href="{video_file}"><img src="{thumbnail_path}" alt="{video_file}" />{video_file}</a></li>'
            video_links.append(video_link)
            indexing()

def generate_thumbnail(video_path, thumbnail_path):
    clip = mpy.VideoFileClip(video_path)
    frame = clip.get_frame(0)
    image = Image.fromarray(frame)
    image.save(thumbnail_path)

video_links = []

# generate a thumbnail for each video in the directory
for video_file in glob.glob('*.mp4'):
    thumbnail_path = "thumbnails/"+video_file + '.jpg'
    if os.path.exists(thumbnail_path):
        video_link = f'<li><a href="{video_file}"><img src="{thumbnail_path}" alt="{video_file}" />{video_file}</a></li>'
        video_links.append(video_link)

def indexing():
    video_links_str = '\n'.join(video_links)
    with open('template.html', 'r') as f:
      html_template = f.read()
    html_output = html_template.format(video_links=video_links_str)
    with open('index.html', 'w') as f:
        print("created html")
        f.write(html_output)

indexing()

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        dir_update()
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

server = ThreadedHTTPServer(("", PORT), CustomHTTPRequestHandler)
server.serve_forever()
