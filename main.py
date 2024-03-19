import cv2 
import numpy as np 
cap = cv2.VideoCapture("http://10.21.41.155:8080/video")
#cap = cv2.VideoCapture("./video.mp4")
min_width = 80 
min_height = 80
count_line_posotion = 550 
algo  = cv2.createBackgroundSubtractorMOG2()
while True:
    ret, frame1 = cap.read()
    
    if not ret:  # Check if frame reading was successful
        print("Failed to read frame from capture.")
        break  # Exit the loop if reading fails
    
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernal)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernal)
    counterShape , h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, count_line_posotion), (1200, count_line_posotion), (255, 127, 0), 3)

    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_encounter = (w>= min_width) and (h>=min_height)
        if not validate_encounter:
            continue
        cv2.rectangle(frame1 , (x,y), (x+w , y+h) , (0,0,255) , 2)
