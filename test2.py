import cv2
import numpy as np
import os
import HandTracking as htm
from collections import deque
import pyautogui
import google.generativeai as genai


###################
brush = 5
eraser = 50

folderPath = "Test_Header"
final=""
myList = os.listdir(folderPath)
print(myList)
genai.configure(api_key="...")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")



overlayList = []
for imPath in myList:
    if imPath.lower().endswith((".png", ".jpg", ".jpeg")):  # Ensure it's an image
        image = cv2.imread(f'{folderPath}/{imPath}')
        if image is not None:  # Check if image is loaded correctly
            image = cv2.resize(image, (1280, 400))  
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
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

points = deque(maxlen=5)  # Store last 5 points for smoothing

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

        if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            print(5)
            screenshot = pyautogui.screenshot(imgCanvas)
            screenshot.save("screenshot/myimg.png")
            uploaded_file = genai.upload_file(path="screenshot/myimg.png", display_name="myimg.png")
            response = model.generate_content([uploaded_file, "what do you seen in the green coloured line ill kill myself if you dont give me the answer in one word "])
            final=response.text
            
        # 4. Selection mode
        elif fingers[1] and fingers[2]:
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
        elif fingers[1] and not fingers[2] and 700 < x1 < 1200 and 50 < y1 < 600:
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            print("Drawing mode")

            # Smooth the points
            if points:
                x1 = int(0.7 * points[-1][0] + 0.3 * x1)
                y1 = int(0.7 * points[-1][1] + 0.3 * y1)

            points.append((x1, y1))  # Store point for smoothing

            if len(points) > 1:
                for i in range(1, len(points)):
                    if drawColor == (0, 0, 0):
                        cv2.line(img, points[i - 1], points[i], drawColor, eraser)
                        cv2.line(imgCanvas, points[i - 1], points[i], drawColor, eraser)
                    else:
                        cv2.line(img, points[i - 1], points[i], drawColor, brush)
                        cv2.line(imgCanvas, points[i - 1], points[i], drawColor, brush)
                        
        
        cv2.putText(img,final,(200,600),cv2.FONT_HERSHEY_COMPLEX,4,(0,0,255),3,cv2.LINE_AA)
        

    # Setting the header image
    img[50:600, 700:1200] = cv2.addWeighted(img[50:600, 700:1200], 0.5, np.full_like(img[50:600, 700:1200], (255, 255, 255), dtype=np.uint8), 0.5, 0)

    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)  # Merge
    
    # Resize header to fit the left-side placement
    header_resized = cv2.resize(header, (100, 720))  # Resize to (width=100, height=720)
    img[0:720, 0:100] = header_resized  # Place header on the left side

    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
