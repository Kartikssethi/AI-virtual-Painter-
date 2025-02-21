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

overlayList = []
for imPath in myList:
    if imPath.lower().endswith((".png", ".jpg", ".jpeg")):  # Ensure its an image
        image = cv2.imread(f'{folderPath}/{imPath}')
        if image is not None:  # Check if image is loaded correctly
            image = cv2.resize(image, (1280, 250))  # Resize images to match header size
            overlayList.append(image)

print(len(overlayList))
if overlayList:  # Ensure at least one image is loaded
    header = overlayList[0]  # Giving an initial value
else:
    raise Exception("No valid images found in the 'Header' folder!")

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

        # 4. If selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            print("Selection mode")
            # Checking for the click
            if y1 < 250:  # Ensure within header range
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (0, 255, 0)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (255, 0, 255)
                elif 1050 < x1 < 1250:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)

        # 5. If drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
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
    img[0:250, 0:1280] = header
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0) #merge 
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    cv2.waitKey(1)
