import cv2
from cvzone.HandTrackingModule import HandDetector
import time

detector = HandDetector(detectionCon=0.8, maxHands=1)
time.sleep(2.0)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)
    cv2.rectangle(img, (0, 480), (300, 425), (50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425), (50, 50, 255), -2)
    
    #If hands are detected, fingerUp is assigned to a list which tells us
    #which fingers are raised and which aren't.
    if(hands):
        lmList = hands[0]
        print(lmList)
        fingerUp = detector.fingersUp(lmList)
        cv2.putText(frame, 'Finger count is:', (20, 460),
        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
        cv2.LINE_AA)       
        cv2.putText(frame,str(sum(fingerUp)), (420, 460),
        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
        cv2.LINE_AA)
        
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break    

video.release()
cv2.destroyAllWindows() 