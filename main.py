import http.server
from PIL import Image
import moviepy.editor as mpy
import os
import glob
import socketserver
def generate_thumbnail(video_path, thumbnail_path):
  # open the video file using moviepy
  clip = mpy.VideoFileClip(video_path)
  # get the first frame of the video
  frame = clip.get_frame(0)
  # convert the frame to an image
  image = Image.fromarray(frame)
  # save the image to the thumbnail path
  image.save(thumbnail_path)

# get a list of all the video and thumbnail files in the current directory
video_files = glob.glob('*.mp4')
for video_file in video_files:
  # create the thumbnail path
  thumbnail_path = video_file + '.jpg'
  # generate the thumbnail
  generate_thumbnail(video_file, thumbnail_path)

thumbnail_files = glob.glob('*.jpg')

# create an empty list to store the video links
video_links = []

# generate a thumbnail for each video in the directory

for video_file, thumbnail_file in zip(video_files, thumbnail_files):
  # create an HTML link for the video file, with the thumbnail image
  video_link = f'<li><a href="{video_file}"><img src="{thumbnail_file}" alt="{video_file}" />{video_file}</a></li>'
  # add the link to the list
  video_links.append(video_link)

# join the list of video links into a single string
video_links_str = '\n'.join(video_links)


# read the HTML template file
with open('template.html', 'r') as f:
  html_template = f.read()

# insert the video links into the template
html_output = html_template.format(video_links=video_links_str)

# write the final HTML output to a file
with open('index.html', 'w') as f:
    print("created html")
    f.write(html_output)


PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # check the request path
        if self.path == '/':
            # serve the index.html file
            self.path = '/index.html'
        # let the base class handle the request
        return super().do_GET()

# create a threaded server using the ThreadingMixIn class
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

# create the server using the threaded server class
server = ThreadedHTTPServer(("", PORT), CustomHTTPRequestHandler)

# start the server
server.serve_forever()