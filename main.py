import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
frameFPS = 150

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,frameFPS)


colors = [[89,116,143,109,255,233], [119,94,174,179,114,225]] #h_min,s_min,v_min, h_max,s_max,v_max
colorValues = [[76,153,0],[0,0,204]] #Format BGR
points = [] # [x,y, colorId]

def findColor(img,colors,colorValues):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	count = 0
	newPoints = []
	for color in colors:
		lower = np.array(color[:3])
		upper = np.array(color[3:])
		mask = cv2.inRange(imgHSV,lower,upper) 
		x,y = getContours(mask) #use HSV mask to get location of specific color.
		#cv2.circle(imgResult, (x,y),15,colorValues[count],cv2.FILLED)
		if x != 0 and y != 0:
			newPoints.append([x,y,count])
		count += 1
	return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02 *peri, True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(points,colorValues):
	for point in points:
		x,y,count = point
		cv2.circle(imgResult,(x,y),10,colorValues[count],cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,colors,colorValues)
    if len(newPoints) != 0:
    	for newPoint in newPoints:
    		points.append(newPoint)
    if len(points) != 0:
    	drawOnCanvas(points,colorValues)


    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
