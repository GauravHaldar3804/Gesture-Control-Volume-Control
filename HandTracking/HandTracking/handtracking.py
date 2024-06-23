import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
prev_time = 0
curr_time = 0

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            for id , lm in enumerate(handLMS.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w) , int(lm.y*h)
                print(id,cx,cy)
            mpDraw.draw_landmarks(img,handLMS,mpHands.HAND_CONNECTIONS)
    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time

    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_SIMPLEX,3,(0,255,255),3)
    
    cv.imshow("Image",img)
    cv.waitKey(1)