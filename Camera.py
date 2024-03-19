import cv2
import time
import os as os


cap = cv2.VideoCapture("http://10.21.41.155:8080/video")


if not cap.isOpened():
    print("lavde link galat hai")
    exit()
if cap.isOpened():
    print("works")

capture_interval = 1


photo_counter = 0
last_capture_time = time.time()


while True:

    ret, frame = cap.read()


    if not ret:
        print("The fames are not comming in ")
        break


    current_time = time.time()


    if current_time - last_capture_time >= capture_interval:

        photo_counter += 1
        filename = "images/{}.jpeg".format(photo_counter)
        cv2.imwrite(filename, frame)
        

        last_capture_time = current_time

        print("Photo {} done.".format(photo_counter))

    


    cv2.imshow('Frame', frame)
    if cv2.waitKey(1)  == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
