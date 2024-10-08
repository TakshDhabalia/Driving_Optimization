import cv2
import threading
import time
import os
import numpy as np
import MQTT
import Camera as cam

count_lock = threading.Lock()  # Lock for count variable
car_count_lock = threading.Lock()  # Lock for car_count variable

count = 1
car_count = 1

def car_detection(image_path, batch_size):
    global car_count
    
    image = cv2.imread(image_path)
    image_arr = np.array(image)

    grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    dilated = cv2.dilate(blur, np.ones((3, 3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    car_cascade_src = 'cars.xml'
    car_cascade = cv2.CascadeClassifier(car_cascade_src)
    cars = car_cascade.detectMultiScale(closing, 1.1, 1)

    cnt = len(cars)
    print(f"{cnt} cars found for {image_path}")

    with car_count_lock:
        car_count += cnt

    # If batch is completed, reset car_count and return the count
    if count % batch_size == 0:
        with car_count_lock:
            ca = car_count
            car_count = 0
        return ca

def car_detection_repeated(batch_size, total_images):
    global count
    
    for i in range(total_images):
        image_path = f"images/{count}.jpeg"

        # Car detection
        car_count = car_detection(image_path, batch_size)

        # Increase count
        with count_lock:
            count += 1

        # Publish car count if it's not None
        if car_count is not None:
            client.publish("ESIOT", car_count)

        time.sleep(10)

if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")

    # Start capturing images
    t1 = threading.Thread(target=cam.capture_images, args=("http://192.168.1.14:8080/video", 3))

    # Start car detection
    t2 = threading.Thread(target=car_detection_repeated, args=(1, 100))

    # Initialize MQTT client
    client = MQTT.MQTTClient("172.28.66.244", 1993)
    client.connect()
    

    t2.start()
    print("t2 started")

    # Start threads
    t1.start()
    print("t1 started")
    
    # Join threads
    t1.join()
    t2.join()
