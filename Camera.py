
#samanyu : http://172.20.10.2:8084/?action=stream

import cv2
import time
import os

def capture_images(video_source, capture_interval=1, output_directory="images"):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("lavde link galaat hai bhai yaar")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    photo_counter = 0
    last_capture_time = time.time()
    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Frames are not coming in as expected in order [TCP error moaybe].")
            break

        current_time = time.time()

        if current_time - last_capture_time >= capture_interval:
            photo_counter += 1
            filename = f"{output_directory}/{photo_counter}.jpeg"
            cv2.imwrite(filename, frame)
            last_capture_time = current_time
            print(f"Photo {photo_counter} captured.")

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    end_time = time.time() - start_time
    print(f"Total Runtime: {end_time} seconds")

    cap.release()
    cv2.destroyAllWindows()


# Example usage:

