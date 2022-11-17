import cv2
from PIL import Image
import tesserocr
import concurrent.futures

video = cv2.VideoCapture("/mnt/c/Users/danil/Desktop/day1.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
flag, frame = video.read()
if (flag):
  hMiddle = int(frame.shape[1] / 2)
  vMiddle = int(frame.shape[0] / 2)

  x_start_left = hMiddle - 230
  x_end_left = hMiddle - 60
  x_start_right = hMiddle + 60
  x_end_right = hMiddle + 230
  y_start_robot = vMiddle - 20
  y_end_robot = vMiddle + 15
  y_end_team = vMiddle + 35

frame_count = 59400
video.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

lastleft = None
lastRight = None

def detect(image):
  global lastleft
  global lastRight
  leftTeam = image[y_start_robot:y_end_robot ,x_start_left:x_end_left]
  rightTeam = image[y_start_robot:y_end_robot ,x_start_right:x_end_right]


  leftTeam = cv2.cvtColor(leftTeam, cv2.COLOR_BGR2GRAY)
  rightTeam = cv2.cvtColor(rightTeam, cv2.COLOR_BGR2GRAY)

  gray = Image.fromarray(leftTeam)
  left_text = tesserocr.image_to_text(gray)

  gray = Image.fromarray(rightTeam)
  right_text = tesserocr.image_to_text(gray)

  if ((left_text.strip() != "" and right_text.strip() != "") and (left_text.strip() != lastleft or right_text.strip() != lastRight)):

    secs = int(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
    mins = secs // 60
    secs = secs % 60
    hours = mins // 60
    mins = mins % 60
    lastleft = left_text.strip()
    lastRight = right_text.strip()
    print(f"{left_text.strip()} X {right_text.strip()} = {hours}:{mins}:{secs}")
with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
  while(video.isOpened()):
    flag, frame = video.read()
    frame_count += 1

    if (frame_count % 20 != 0): 
      continue
    
    if (flag):
      executor.submit(detect, image=frame)