from PIL import Image
import cv2
import numpy as np
import requests
import Detection_updated
import MQTT

image = cv2.imread('lmao_car_1.jpeg')

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
client = MQTT.connect_mqtt()
client.loop_start()
MQTT.publish(client, "main" , "69")
client.loop_stop()

annotated_image = Image.fromarray(image_arr)
annotated_image.show()

cv2.waitKey(0)
cv2.destroyAllWindows()