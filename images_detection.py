
import cv2
print(cv2.__version__)

cascade_src = 'cars.xml'
for i in [1,2,3,4,5]:
    photocounter = i
#video_src = 'D:\Driving_Optimization\images\{}.jpeg'.format(photocounter)
video_src = 'lmao_car_1.jpeg '
#video_src = './images/2.jpeg'
cap = cv2.VideoCapture(video_src)
car_cascade = cv2.CascadeClassifier(cascade_src)

while True:
    ret, img = cap.read()
    if (type(img) == type(None)):
        break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x,y,w,h) in cars:
        x = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)  
        
        if x.any() == True :
            print('1')
        elif x.all() == False:
            print('0')
    print(type(x))
    cv2.imshow('video', img)
    print('works')
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()