#INITIAL SETUP
#----------------------------------------------------------------
import cv2
from cvzone import HandTrackingModule, overlayPNG
import numpy as np
intro =# read frames\img 1 in the intro variable
kill =# read frames\img 2 in the kill variable
winner = # read frames\img 3 in the winner variable
cam = #read the camera
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)
#sets the minimum confidence threshold for the detection

#INITILIZING GAME COMPONENTS
#----------------------------------------------------------------
sqr_img = # read img\sqr (1) in the sqr_img variable
mlsa =  # read img\mlsa in the mlsa variable
#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
gameOver = False
NotWon =True
#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------
while not gameOver:
        continue
#LOSS SCREEN
if NotWon:
    for i in range(10):
       #show the loss screen from the kill image read before
    while True:
        #show the loss screen from the kill image read before and end it after we press q

else:
#WIN SCREEN
#show the win screen from the winner image read before

    while True:
        #show the win screen from the winner image read before and end it after we press q

#destroy all the windows

