import cv2
import os
import time

# ASCII characters from dark to light
# ASCII_CHARS = "@%#*+=-:. " 
ASCII_CHARS = " .:-=+*#%@"
# ASCII_CHARS = "   -=+*#%@"


def frame_to_ascii(frame, new_width=100):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

    # Resize frame to fit terminal
    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.43)
    resized_gray = cv2.resize(gray, (new_width, new_height))

    # chars = ASCII_CHARS[::-1] if not invert else ASCII_CHARS

    # Convert pixels to ASCII
    ascii_frame = ""
    for row in resized_gray:
        line = "".join(
            ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
              for pixel in row
        )
        ascii_frame += line + "\n"

    return ascii_frame

def play_video_ascii(video_path, width=100, fps=60):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_frame = frame_to_ascii(frame, new_width=width)

            os.system("cls" if os.name == "nt" else "clear")  # clear terminal
            print(ascii_frame)

            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        cap.release()

if __name__ == "__main__":
    
    play_video_ascii("input_video_3.mp4", width=100)