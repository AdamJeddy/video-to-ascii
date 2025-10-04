import os
import cv2
from PIL import Image
import ascii_magic
import time

def video_to_ascii(video_path, target_fps=30, target_width=100):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps == 0:
        original_fps = 30  # Default to 30 if unable to get FPS

    # calculate delay between frames for wanted fps
    frame_delay = 1.0 / target_fps

    # Clear terminal

    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # convert frame to grreyscale
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # convert OpenCV image to PIL image
        pil_image = Image.fromarray(grey_frame)

        # calculate new height to maintain aspect ratio
        width, height = pil_image.size
        aspect_ratio = height / width

        # aspect ratio correction for terminal characters
        new_height = int(target_width * aspect_ratio * 0.55)

        # resize image
        pil_image = pil_image.resize((target_width, new_height))

        # convert to ASCII
        ascii_art_obj = ascii_magic.from_pillow_image(pil_image)

        # render to terminal

        # ascii_frame = ascii_art_obj.to_terminal(monochrome=True, back=ascii_magic.Back.BLACK)
        ascii_frame = ascii_art_obj.to_terminal()
        clear_terminal() 
        print(ascii_frame)

        time.sleep(frame_delay)

    cap.release()

    print("Video processing complete.")


if __name__ == "__main__":

    video_file = "input_video_1.mp4"
    target_width = 1920
    target_fps = 60

    # Check if the video file exists
    if not os.path.isfile(video_file):
        raise FileNotFoundError(f"Video file '{video_file}' not found.")
    else:
        video_to_ascii(video_file, target_fps, target_width)