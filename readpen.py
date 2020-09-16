import cv2
import numpy as np
#computer vision


frameWidth=640
framHeight=480

cap = cv2.VideoCapture(0)
#to capture a video
cap.set(3,frameWidth) #height
cap.set(4,framHeight) #width
cap.set(10,150) #brightness

mycolors = [[44,65,59,90,255,186],#green
            #[57,76,0,100,255,255],
            [60,132,86,179,215,255], #blue
            #[90,48,0,118,255,255],
            [21,120,106,178,240,255]
#[5,107,0,19,255,255]
]#pink


myColorValues=[ [0,255,0],   #bgr   # green
               [255,0,0], #  blue
                   [0,0,255]]#pink

myPoints = []  ##   [x , y , coloutId]

def FindColor(img, mycolors, myColorValues):
            imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            count=0
            newpoints=[]
            for color in mycolors:
                    lower = np.array(color[0:3])
                    upper = np.array(color[3:6])
                    mask = cv2.inRange(imgHSV, lower, upper)
                    x,y=getContours(mask)
                    cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
                    if x!=0 and y!=0:
                        newpoints.append([x,y,count])
                    count+=1
                    #cv2.imshow(str(color[0]),mask)
            return newpoints
def getContours(img):
    contours,hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        #print(area)
        if area > 500:
               #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
               peri=cv2.arcLength(cnt,True)
               #print(peri)
               approx=cv2.approxPolyDP(cnt,0.02*peri,True)
               #print(len(approx))
               #objCor=len(approx)
               x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success , img = cap.read()
    imgResult = img.copy()
    newpoints = FindColor(img,mycolors,myColorValues)
    if len(newpoints)!=0:
        for newP in newpoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
