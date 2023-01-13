from PIL import Image
import moviepy.editor as mpy

def generate_thumbnail(video_path, thumbnail_path):
  # open the video file using moviepy
  clip = mpy.VideoFileClip(video_path)
  # get the first frame of the video
  frame = clip.get_frame(0)
  # convert the frame to an image
  image = Image.fromarray(frame)
  # save the image to the thumbnail path
  image.save(thumbnail_path)

# generate a thumbnail for each video in the directory
for video_file in video_files:
  # create the thumbnail path
  thumbnail_path = video_file + '.jpg'
  # generate the thumbnail
  generate_thumbnail(video_file, thumbnail_path)
