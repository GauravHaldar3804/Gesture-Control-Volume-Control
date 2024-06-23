import cv2 as cv
import mediapipe as mp
import time
import math

class handDetector:
    def __init__(self, mode = False , maxHands = 2,complexity = 1 ,detectConf = 0.5,trackConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectConf = detectConf
        self.trackConf = trackConf

        self.tipIds = [4 , 8 , 12 , 16 , 20]
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.complexity,self.detectConf,self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLMS,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw = True):
        self.lmlists = []
        xlists = []
        ylists = []
        bbox = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w) , int(lm.y*h)
                # print(id,cx,cy)
                self.lmlists.append([id,cx,cy])
                xlists.append(cx)
                ylists.append(cy)
                xMin , xMax = min(xlists) , max(xlists)
                yMin , yMax = min(ylists) , max(ylists)
                bbox = [xMin , yMin , xMax , yMax]


                if draw :
                    cv.circle(img,(cx,cy),5,(0,0,255),cv.FILLED)
            if draw :
                cv.rectangle(img,(bbox[0]-20,bbox[1]-20),(bbox[2]+20,bbox[3]+20),(0,255,0),2)

        return self.lmlists,bbox
    
    def findlength(self,img,p1,p2,draw = True):
        x1 , y1 = self.lmlists[p1][1],self.lmlists[p1][2]
        x2 , y2 = self.lmlists[p2][1],self.lmlists[p2][2]
        cx , cy = (x1+x2)//2 , (y1+y2)//2
        
        if draw:
            cv.circle(img,(x1,y1),7,(255,0,0),cv.FILLED)
            cv.circle(img,(x2,y2),7,(255,0,0),cv.FILLED)
            cv.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            cv.circle(img,(cx,cy),7,(255,0,0),cv.FILLED)
        length = math.hypot(x2-x1,y2-y1)

        return length,img,[x1,y1,x2,y2,cx,cy]
    
    def fingersUp(self):
        fingers = []
        if self.lmlists[self.tipIds[1]][1] < self.lmlists[self.tipIds[4]][1]:
            if self.lmlists[self.tipIds[0]][1] < self.lmlists[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        elif self.lmlists[self.tipIds[1]][1] > self.lmlists[self.tipIds[4]][1]:
            if self.lmlists[self.tipIds[0]][1] > self.lmlists[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        for id in range(1,5):

            if self.lmlists[self.tipIds[id]][2] < self.lmlists[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    prev_time = 0
    curr_time = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()
    

    while True:
        success, img = cap.read()
        img = cv.flip(img,1)
        img = detector.findHands(img)
        
        lmlists = detector.findPosition(img)
        if len(lmlists) != 0: 
            print(lmlists[4])

        curr_time = time.time()
        fps = 1/(curr_time-prev_time)
        prev_time = curr_time

        cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_SIMPLEX,3,(0,255,255),3)
    
        cv.imshow("Image",img)
        cv.waitKey(1)


if __name__ == "__main__":
    main()

