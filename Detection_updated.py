import cv2
import numpy as np
import threading
import Detection_updated
import MQTT
import Camera as cam
import time

count = 1

def car_detection(count):

    while True:
        image = cv2.imread(f"images/{count}.jpeg")
        
        image_arr = np.array(image)

        grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(grey, (5, 5), 0)

        dilated = cv2.dilate(blur, np.ones((3, 3)))

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

        car_cascade_src = 'cars.xml'
        car_cascade = cv2.CascadeClassifier(car_cascade_src)
        cars = car_cascade.detectMultiScale(closing, 1.1, 1)

        
        cnt = 0
        for (x, y, w, h) in cars:
            cv2.rectangle(image_arr, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cnt += 1
        print(cnt, " cars found")
        count += 15
        time.sleep(5)
        return cnt 
    

def annotated_images():
    annotated_image = image.fromarray(car_detection.image_arr)
    annotated_image.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    t1 = threading.Thread(target=car_detection, args=(count,))
    t2 = threading.Thread(target=cam.capture_images, args=("https://192.168.1.14:8080/video", 3))
    client = MQTT.MQTTClient("172.28.66.244", 1883)
    client.connect()
    status_number = car_detection(count=count)
    t4 = threading.Thread(target=MQTT.MQTTClient.publish_loop, args=(client, "ESIOT", status_number, 5))

    t1.start()
    print("t1 started")
    t2.start()
    print("t2 started")

    t4.start()
    t1.join()
    t2.join()
