import cv2
import os
import datetime

def process_video(dir):
    # Directory containing images to be converted
    directory = dir

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(dir + 'Timelapse' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.mp4', fourcc, 25.0, (1920,1080))

    files = os.listdir(directory)

    # Loop through all files in the directory
    for file_name in files:
        # Check if file is an image
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            # Read the image
            img = cv2.imread(os.path.join(directory, file_name))
            # Resize the image if necessary
            img = cv2.resize(img, (1920, 1080))
            # Concatenate the image horizontally to form a frame
            if frame is None:
                frame = img
            else:
                frame = cv2.hconcat([frame, img])
        # Write the frame to the video
        out.write(frame)
    # Release the VideoWriter object
    out.release()