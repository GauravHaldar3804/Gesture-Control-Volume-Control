import cv2 as cv
import handtrackingmodule as htm
import mediapipe as mp
import numpy as np
import time
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


cap = cv.VideoCapture(0)
wcam , hcam = 640 , 480
cap.set(3,wcam)
cap.set(4,hcam)

prev_time = 0
curr_time = 0

detector = htm.handDetector(detectConf=0.7,trackConf=0.7,maxHands=1)

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
volCol = (255,0,0)
voll = 0
prevArea = 0




while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    # Find Hands
    img = detector.findHands(img)
    lmlists,bbox = detector.findPosition(img,draw=True)

    # Frame Rate
    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time

    cv.putText(img,f"FPS:{str(int(fps))}",(40,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
        
        
        
        
        
        
         
        
    
    if len(lmlists) != 0: 
        # Filter based on size
        
        area = ((bbox[2]-bbox[0])*(bbox[3]-bbox[1]))//100
        
        if 50 < area < 1500 :
           
           # Find Distance between index and Thumb
           length , img ,lineInfo = detector.findlength(img,p1 = 4 , p2 = 8)
        
           # Convert Volume
           volBar = np.interp(length,[50,250],[400,100])
           volPer = np.interp(length,[50,250],[0,100])

           # Reduce resolution to make it smoother
           smoothness = 10
           volPer = smoothness*round(volPer/smoothness)

           
           # Check Fingers up
           fingers = detector.fingersUp()

           # If pinky is down set volume
           if not fingers[3]:
               volCol = (0,255,0)
               volume.SetMasterVolumeLevelScalar(volPer/100, None)
               voll = int(volume.GetMasterVolumeLevelScalar()*100)
               cv.circle(img,(lineInfo[4],lineInfo[5]),7,volCol,cv.FILLED)
           else:
               volCol = (255,0,0)
               
               
               
         # Drawings 
         
        cv.rectangle(img,(40,100),(85,400),(255,0,0),3)
        cv.rectangle(img,(40,int(volBar)),(85,400),(255,0,0),cv.FILLED)
        cv.putText(img,f"{str(int(volPer))}%",(40,450),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
        cv.putText(img,f"Volume Set:{str(int(voll))}",(400,50),cv.FONT_HERSHEY_SIMPLEX,1,volCol,3)



    
    cv.imshow("Image",img)
    cv.waitKey(1)