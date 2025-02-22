import cv2
import numpy as np
import os
import HandTracking as htm

# Brush and Eraser Sizes
brush = 15
eraser = 50

# Load Header Images
folderPath = "virtual_painter"
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    if imPath.lower().endswith((".png", ".jpg", ".jpeg")):  # Ensure it's an image
        image = cv2.imread(f'{folderPath}/{imPath}')
        if image is not None:  # Check if image is loaded correctly
            image = cv2.resize(image, (1280, 250))  # Resize images to match header size
            overlayList.append(image)

# Ensure at least one image is loaded
if not overlayList:
    raise Exception("No valid images found in the 'virtual_painter' folder!")

virtual_painter = overlayList[0]  # Default header
drawColor = (0, 255, 0)

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = htm.HandTrackingModule(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import Image
    success, img = cap.read()
    if not success:
        continue
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)  # Detect the hand
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. Selection Mode (Two fingers up)
        if fingers[1] and fingers[2]:
            print("Selection mode")
            if y1 < 250:  # Ensure within virtual_painter range
                if 250 < x1 < 450:
                    virtual_painter = overlayList[0]
                    drawColor = (0, 255, 0)
                elif 550 < x1 < 750:
                    virtual_painter = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    virtual_painter = overlayList[2]
                    drawColor = (255, 0, 255)
                elif 1050 < x1 < 1250:
                    virtual_painter = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)

        # 5. Drawing Mode (Only Index Finger Up)
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing mode")

            if xp == 0 and yp == 0:  # Initialize previous point
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):  # Eraser Mode
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraser)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraser)
            else:  # Brush Mode
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brush)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brush)

            xp, yp = x1, y1  # Update previous point

    # Setting the header image
    img[0:250, 0:1280] = virtual_painter
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)  # Merge drawing and webcam

    # Display Windows
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
