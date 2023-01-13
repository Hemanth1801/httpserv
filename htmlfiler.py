import os
import glob

# get a list of all the video and thumbnail files in the current directory
video_files = glob.glob('*.mp4')
thumbnail_files = glob.glob('*.jpg')

# create an empty list to store the video links
video_links = []

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
  f.write(html_output)
