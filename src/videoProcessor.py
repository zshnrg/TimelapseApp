import cv2
import numpy as np
import os
import pyautogui
import datetime

def process_video(targetDir, photoDir):
    # Video frame
    frame_width, frame_height = pyautogui.size()

    # Target directory
    folder_path = photoDir
    video_name = targetDir + '\Timelapse' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.mp4'

    # Accessing image files with certain extensions in the directory
    extensions = ('.jpg')
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(extensions)]
    image_files.sort()

    # FIltering with only images with screenshot prefix
    image_files = [f for f in image_files if f.startswith("screenshot")]

    # Creating a video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, 24, (frame_width, frame_height))

    # Processing all images
    for image_file in image_files:
        img = cv2.imread(os.path.join(folder_path, image_file))
        img = cv2.resize(img, (frame_width, frame_height))
        out.write(img)

    # Releasing the video file
    out.release()

    # Checking if the video file is created
    if os.path.exists(video_name):
        print("Video exported! Check your target directory")
        # Deleting all images
        for image_file in image_files:
            os.remove(os.path.join(folder_path, image_file))
    else:
        print("Video export failed")
        process_video(dir)