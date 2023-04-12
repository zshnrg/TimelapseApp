import cv2
import numpy as np
import os
import pyautogui
import datetime

def process_video(dir):
    # Video frame
    frame_width, frame_height = pyautogui.size()

    # Target directory
    folder_path = dir
    video_name = dir + '\Timelapse' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.mp4'

    # Accessing image files with certain extensions in the directory
    extensions = ('.png', '.jpeg', '.jpg')
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(extensions)]
    image_files.sort()

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