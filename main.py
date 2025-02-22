import cv2
import numpy as np
import os
import HandTracking as htm

###################
brush = 15
eraser = 50

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)

drawColor = (0, 255, 0)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandTrackingModule(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. importing image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find hand landmarks
    img = detector.findHands(img)  # Draw on img and detect the hand
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()  # Correct function call

        

        # 5. If drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False and x1>700 and x1<1200 and y1>50 and y1<600:
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            print("Drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraser)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraser)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brush)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brush)

            xp, yp = x1, y1

    # Setting the header image
    img[50:600, 700:1200] = (255,255,255)
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0) #merge 
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    cv2.waitKey(1)
