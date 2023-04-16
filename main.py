import random
import cv2
from cvzone import HandTrackingModule, overlayPNG
import numpy as np
import os
import time
import mediapipe as mp


intro =cv2.imread("frames/img1.jpeg");
kill =cv2.imread("frames/img2.png")
winner =cv2.imread("frames/img3.png")
cam = cv2.VideoCapture(0);
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)

sqr_img = cv2.imread("img/sqr(2).png");
mlsa =  cv2.imread("img/mlsa.png");

gameOver = False
NotWon =True
game_time = 60
score_limit = 5
team_a_score = 0
team_b_score = 0
game_start_time = time.time()

while True:
    cv2.imshow("Intro", intro)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

while time.time() - game_start_time < game_time and team_a_score < score_limit and team_b_score < score_limit:
    
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    hands = detector.findHands(frame)

    # check if a hand is detected
    if hands:
        # get the first hand detected
        hand = hands[0]

        # get the hand position and check if it's within the square image
        hand_pos = hand["lmList"][8] # assuming hand is open and thumb is up
        if sqr_img.shape[1] > hand_pos[0] > 0 and sqr_img.shape[0] > hand_pos[1] > 0:
            # move the ball based on the hand position
            ball_pos = (int(hand_pos[0] * mlsa.shape[1] / sqr_img.shape[1]), int(hand_pos[1] * mlsa.shape[0] / sqr_img.shape[0]))

            # check if ball collides with the goal for Team A
            if ball_pos[0] > 0 and ball_pos[0] < mlsa.shape[1] / 2 and mlsa[ball_pos[1], ball_pos[0], 2] == 255:
                team_a_score += 1
                # reset ball position
                ball_pos = (mlsa.shape[1] // 2, mlsa.shape[0] // 2)

            # check if ball collides with the goal for Team B
            elif ball_pos[0] > mlsa.shape[1] / 2 and ball_pos[0] < mlsa.shape[1] and mlsa[ball_pos[1], ball_pos[0], 1] == 255:
                team_b_score += 1
                # reset ball position
                ball_pos = (mlsa.shape[1] // 2, mlsa.shape[0] // 2)

    # draw the ball and goals on the frame
    frame = overlayPNG(frame, mlsa, ball_pos)
    frame = overlayPNG(frame, sqr_img, (0,0))

    # draw the score on the frame
    cv2.putText(frame, "Team A: " + str(team_a_score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Team B: " + str(team_b_score), (frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # display the frame and wait for a key press
    cv2.imshow("Game", frame)
    
while not gameOver:
        continue
#LOSS SCREEN

if NotWon:
    for i in range(10):
        #show the loss screen from the kill image read before
        cv2.imshow("Loss Screen", kill)
        cv2.waitKey(100)
    while True:
        #show the loss screen from the kill image read before and end it after we press q
        cv2.imshow("Loss Screen", kill)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

else:

   while True:
    
    cv2.imshow("Winner Screen", winner)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()


