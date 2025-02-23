import cv2
import numpy as np
import os
import HandTracking as htm

###################
brush = 15
eraser = 50

folderPath = "Test_Header"
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    if imPath.lower().endswith((".png", ".jpg", ".jpeg")):  # Ensure it's an image
        image = cv2.imread(f'{folderPath}/{imPath}')
        if image is not None:  # Check if image is loaded correctly
            image = cv2.resize(image, (1280, 100))  # Resize to fit the bottom width
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
    # 1. Import image
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

        # 4. Selection mode
        if fingers[1] and fingers[2]:
            print("Selection mode")
            if x1 < 100:  # Detect clicks in the left-side header
                if 400 < y1 < 450:
                    header = overlayList[0]
                    drawColor = (0, 255, 0)
                elif 500 < y1 < 600:
                    header = overlayList[1]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1 - 15, y1), (x2 + 15, y2), drawColor, cv2.FILLED)

        # 5. If drawing mode - Index finger is up
        if fingers[1] and not fingers[2] and 700 < x1 < 1200 and 50 < y1 < 600:
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
    img[50:600, 700:1200] = (255, 255, 255)
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)  # Merge
    
    # Resize header to fit the left-side placement
    header_resized = cv2.resize(header, (100, 720))  # Resize to (width=100, height=720)
    img[0:720, 0:100] = header_resized  # Place header on the left side

    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)
    cv2.waitKey(1)