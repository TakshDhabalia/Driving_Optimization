import cv2
import numpy as np
import threading
import time
import MQTT
import Camera as cam
import os

count = 1
car_count = 0  #had to make this glibal ik am dumb

def car_detection(image_path):
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
    return cnt

def car_detection_repeated(count, freq):
    global car_count  
    for i in range(freq):
        image_path = f"images/{count}.jpeg"
        car_count += car_detection(image_path)  
        count += 5
        time.sleep(5)

if __name__ == "__main__":

    if not os.path.exists("images"):
        os.makedirs("images")

    t1 = threading.Thread(target=car_detection_repeated, args=(count, 10))
    t2 = threading.Thread(target=cam.capture_images, args=("https://192.168.1.14:8080/video", 3))
    client = MQTT.MQTTClient("172.28.66.244", 1883)
    client.connect()
    t4 = threading.Thread(target=client.publish_loop, args=("ESIOT", car_count+, 10))

    t1.start()
    print("t1 started")
    t2.start()
    print("t2 started")
    t4.start()

    t1.join()
    t2.join()
    t4.join()
