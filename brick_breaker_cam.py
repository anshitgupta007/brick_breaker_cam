from cvzone.HandTrackingModule import HandDetector
import random
import cv2

#game variables

screen_height, screen_width = 700, 840
ball_x, ball_y = screen_width//2, screen_height//2
box_size = 70
bat_x1 = 90
bat_x2 = bat_x1+150
bat_y = screen_height-50
vx, vy = 10, 9
box_x, box_y = 0, 0

boxes = 30
box_list = []
color = []

#creating list of boxes to plot

for i in range(boxes):
    color.append(random.randint(30, 250))
    box_list.append((box_x, box_y))

    box_x = box_x+box_size
    if box_x == screen_width:
        box_y += box_size
        box_x = 0


start = False  # variable for starting the game

#function to plot bricks and ball


def plot(gw):

    global vx, vy, ball_x, ball_y, box_x, box_y, box_list, color, bat_x1, bat_x2

    if start == True:

        ball_x += vx  # inreases speed of ball in x
        ball_y += vy  # inreases speed of ball iny

    cv2.circle(gw, ((ball_x), (ball_y)), 5, (0, 0, 0),
               cv2.FILLED)  # plots the ball
    cv2.line(gw, (bat_x1, bat_y), (bat_x2, bat_y),
             (0, 0, 0), 2)  # plots the bat

    # plotting the bricks
    for box_x, box_y in box_list:
        cv2.rectangle(gw, (box_x, box_y), (box_x+box_size, box_y+box_size),
                      (color[box_x//70], color[box_x//30], color[box_y//70]), cv2.FILLED)
        cv2.rectangle(gw, (box_x, box_y), (box_x+box_size,
                      box_y+box_size), (0, 0, 0), 1)
        if box_x <= ball_x <= box_x+box_size and box_y <= ball_y <= box_y+box_size:

            box_list.remove((box_x, box_y))  # remove bricks when ball hit them
        if box_x <= ball_x <= box_x+box_size and (box_y <= ball_y <= box_y+abs(vy) or box_y+box_size-abs(vy) <= ball_y <= box_y+box_size):

            vy = -vy  # changes velocity on collision
        if box_y <= ball_y <= box_y+box_size and (box_x <= ball_x <= box_x+abs(vx) or box_x+box_size-abs(vx) <= ball_x <= box_x+box_size):

            vx = -vx  # changes velocity on collision


#border constraints on the ball
    if ball_y < 3:
        vy = -vy
    if ball_x > screen_width-3 or ball_x < 3:
        vx = -vx
    if ball_y+abs(vy) >= bat_y >= ball_y and bat_x2 >= ball_x >= bat_x1:
        vy = -vy

    if len(box_list) == 0:
        cv2.putText(back, 'YOU WON', ((screen_width//2)-100,
                    (screen_height//2)-100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    if ball_y > screen_height:
        cv2.putText(back, 'GAME OVER', ((screen_width//2)-100,
                    screen_height//2), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


detector = HandDetector(detectionCon=0.8, maxHands=1)
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (screen_width, screen_height))
    hands, img = detector.findHands(frame, flipType=False)

    if(hands):
        start = True
        lmList = hands[0]

        # x coordinate of a specific point on a finger
        finger_x = lmList['lmList'][9][0]
        # y coordinate of a specific point on a finger
        finger_y = lmList['lmList'][9][1]
        cv2.circle(frame, ((finger_x), (finger_y)),
                   15, (0, 255, 0), cv2.FILLED)
        bat_x1 = ((finger_x)*2-250)  # syncronizing bat with the finger
        bat_x2 = bat_x1+150
        if bat_x1 < 0:
            bat_x1 = 10
            bat_x2 = bat_x1+150
        elif bat_x2 > screen_width:
            bat_x1 = screen_width-150
            bat_x2 = screen_width

    else:
        start = False  # game stops when hand is removed

    # background for the game
    back = cv2.imread("C:/Users/Nik/Desktop/CODES/PYTHON/background.png")
    back = cv2.resize(back, (screen_width, screen_height))
    plot(back)
    cv2.imshow('parameters', back)
    cv2.imshow('image', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    