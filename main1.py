import cv2
from cvzone import HandTrackingModule, overlayPNG
import numpy as np
intro =cv2.imread("frames\img1.png", cv2.IMREAD_UNCHANGED)
kill =cv2.imread("frames\img2.png", cv2.IMREAD_UNCHANGED)
winner = cv2.imread("frames\img3.png", cv2.IMREAD_UNCHANGED)
cam = cv2.VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)
sqr_img = cv2.imread("img\sqr(2).png", cv2.IMREAD_UNCHANGED)
mlsa = cv2.imread("img\mlsa.png", cv2.IMREAD_UNCHANGED)
sqr_img = cv2.resize(sqr_img, (270, 230), interpolation=cv2.INTER_AREA)
mlsa = cv2.resize(mlsa, (90, 80), interpolation=cv2.INTER_AREA)
pox, poy = 160,160
b,g,r = 27,74,114 
prevX,prevY =0,0
finishX,finishY =0,0
NotWon = True
smoothX ,smoothY = 0,0
canvas = np.zeros((480,640,3),np.uint8)
smoothing = 3
corners = [0,0,0,0]
mistakes =0 
while True:
    cv2.imshow('Squid Game', cv2.resize(intro, (640,480), interpolation=cv2.INTER_AREA))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
while NotWon:
    _, img = cam.read()
    img = cv2.flip(img,1)#mirror the camera
    hands,img = detector.findHands(img, flipType = False) #no need to flip the hands as the camera is already flipped
    h,w,_ = sqr_img.shape #gets the height,weight and ignores the colors
    img = overlayPNG(img,sqr_img,[pox,poy])#overlay the cookie image
    img = overlayPNG(img,mlsa,[0,0])#overlay the mlsa image to the top left corner
    if hands:
        lmList = hands[0]['lmList'] #get the landmarks 
        cursor = lmList[8]#set the tip of the index finger as the cursor
        smoothX = int(prevX + (cursor[0] - prevX) / smoothing)
        smoothY = int(prevY + (cursor[1] - prevY) / smoothing)
        if detector.fingersUp(hands[0]) == [0,1,0,0,0]: #if index finger is up
            if pox < smoothX < pox + w and poy < smoothY < poy + h:#when inside the cookie
                cb, cg, cr = img[smoothY, smoothX, 0], img[smoothY, smoothX, 1], img[smoothY, smoothX, 2]
                if cb == b and cg == g and cr == r: #check if on the path
                    if prevX!=cursor[0] and prevY!=cursor[1]:
                        if prevX == 0 and prevY == 0:
                            prevX, prevY = cursor[0], cursor[1]#set the initial cursor when inside cookie
                        if finishX == 0 and finishY == 0:
                            finishX, finishY = cursor[0], cursor[1] #set he end point
                        cv2.line(canvas,(prevX, prevY),(smoothX,smoothY),(255,255,0),thickness=9)
                        if(smoothX-10 <= finishX <= smoothX + 10 and smoothY-10 <= finishY <= smoothY): #when the pointer is around the end point
                            if corners == [1,1,1,1]:
                                print("Win")
                                NotWon = False 
                elif cb == 26 and cg == g and cr == r:#corner 0 check
                    corners[0] = 1
                    cv2.line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)
                elif cb == 28 and cg == g and cr == r:#corner 1 check 
                    corners[1] = 1
                    cv2.line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)
                elif cb == 29 and cg == g and cr == r:#corner 2 check
                    corners[2] = 1
                    cv2.line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)
                elif cb == 30 and cg == g and cr == r:#corner 3 check
                    corners[3] = 1
                    cv2.line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)
                else:
                    mistakes += 1
                    if mistakes == 100:
                        print("lose")
                        corners = [0, 0, 0, 0] #resets the checkpoints
                        canvas = np.zeros((480, 640, 3), np.uint8) # remove green lines
                        finishX, finishY = 0, 0
                        prevX, prevY = 0, 0
                        c = 0
                        mistakes = 0 #resets all the game presets
                        gameOver = True #can do try again in interactive interface
                cv2.circle(img, (smoothX, smoothY), 5, (255, 255, 0), cv2.FILLED)#green circle on the fingertip when finger is up
        else:
            prevX, prevY = 0, 0
            cv2.circle(img, (smoothX, smoothY), 5, (255, 255, 0), cv2.FILLED)#fingertip detection when finger is not only one up 
        prevX, prevY = smoothX, smoothY
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)#rgb->grayscale
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)#converts the black canvas to white
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)#gray->rgb
    img = cv2.bitwise_and(img, imgInv)#masking
    img = cv2.bitwise_or(img, canvas)#masking
    cv2.imshow('Squid Game', cv2.resize(img, (640,480), interpolation=cv2.INTER_AREA))
    cv2.waitKey(3)
if NotWon:
    for i in range(10):
        cv2.imshow('Squid Game', cv2.resize(kill, (640,480), interpolation=cv2.INTER_AREA))
    while True:
        cv2.imshow('Squid Game', cv2.resize(kill, (640,480), interpolation=cv2.INTER_AREA))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
else:

    cv2.imshow('Squid Game', cv2.resize(winner, (640,480), interpolation=cv2.INTER_AREA))
    cv2.waitKey(1)
    while True:
        cv2.imshow('Squid Game', cv2.resize(winner, (640,480), interpolation=cv2.INTER_AREA))
        # cv2.imshow('shit',cv2.resize(graphic[3], (0, 0), fx = 0.5, fy = 0.5))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()