import cv2
import numpy as np
import os
import HandTracking as htm
from collections import deque
import pyautogui
import google.generativeai as genai
import random
import time  # Added time module for animations


###################
brush = 5
eraser = 50
questions=["1","2","3"]

folderPath = "Test_Header"
final=""
myList = os.listdir(folderPath)
print(myList)
genai.configure(api_key="AIzaSyD8Po9zcWq2-91EJ_9aHlDmgMvE13xzqhY")
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

drawColor = (76, 0, 255)  # Purple color

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandTrackingModule(detectionCon=0.85)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

points = deque(maxlen=5)  # Store last 5 points for smoothing
question=random.choice(questions)

# Create futuristic UI elements
def create_hex_pattern(img, x, y, size=20, color=(0, 0, 255)):  # Blue color
    points = []
    for i in range(6):
        angle_rad = i * 2 * np.pi / 6
        point_x = int(x + size * np.cos(angle_rad))
        point_y = int(y + size * np.sin(angle_rad))
        points.append((point_x, point_y))
    
    for i in range(6):
        cv2.line(img, points[i], points[(i+1)%6], color, 1)
    return img

while True:
    # 1. Import image
    
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Apply a red/blue tint to the entire frame for a retro look
    retro_tint = img.copy()
    retro_tint[:, :, 0] = np.clip(retro_tint[:, :, 0] * 0.8, 0, 255)  # Reduce blue channel
    retro_tint[:, :, 2] = np.clip(retro_tint[:, :, 2] * 1.5, 0, 255)  # Boost red channel
    img = cv2.addWeighted(img, 0.7, retro_tint, 0.3, 0)

    # 2. Find hand landmarks
    img = detector.findHands(img)  # Draw on img and detect the hand
    lmList = detector.findPosition(img, draw=False)
    
    # Create a semi-transparent dark overlay for the sidebar
    sidebar_overlay = np.zeros_like(img)
    sidebar_overlay[:, 0:100, :] = (50, 20, 90)  # Dark purple-red
    img = cv2.addWeighted(img, 1, sidebar_overlay, 0.7, 0)
    
    # Add futuristic elements to the drawing area
    # Main border
    cv2.rectangle(img, (700, 50), (1200, 600), (0, 0, 255), 2)  # Blue color
    
    # Corner accents
    cv2.line(img, (700, 50), (720, 70), (76, 0, 255), 1)  # Purple
    cv2.line(img, (1200, 50), (1180, 70), (76, 0, 255), 1)  # Purple
    cv2.line(img, (700, 600), (720, 580), (76, 0, 255), 1)  # Purple
    cv2.line(img, (1200, 600), (1180, 580), (76, 0, 255), 1)  # Purple
    
    # Add scanner line (moving horizontal line)
    scan_line_y = (int(time.time() * 50) % 550) + 50
    cv2.line(img, (700, scan_line_y), (1200, scan_line_y), (0, 0, 255), 1)  # Blue color
    
    # Add hexagonal pattern to sidebar
    create_hex_pattern(img, 50, 350, 30, (0, 0, 255))  # Blue color
    
    # Display question with futuristic styling
    cv2.rectangle(img, (190, 170), (610, 230), (50, 0, 100), -1)  # Dark purple background
    cv2.rectangle(img, (190, 170), (610, 230), (0, 0, 255), 1)  # Blue border
    cv2.putText(img, f"TASK #{question}", (200, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)  # Blue text

    if len(lmList) != 0:
        # Tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()  # Correct function call
# Replace finger detection with keyboard input
        key = cv2.waitKey(100)
        if key == ord('s'):  # Press 'p' key to trigger the processing
            print(5)
            # Add processing effect
            process_overlay = np.zeros_like(img)
            cv2.rectangle(process_overlay, (700, 50), (1200, 600), (50, 0, 100), -1)  # Dark purple
            img = cv2.addWeighted(img, 0.7, process_overlay, 0.3, 0)
            cv2.putText(img, "PROCESSING...", (850, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)  # Blue text
            
            # screenshot = pyautogui.screenshot()
            cv2.imwrite("screenshot/myimg.png", imgCanvas)
            uploaded_file = genai.upload_file(path="screenshot/myimg.png", display_name="myimg.png")
            response = model.generate_content([uploaded_file, "what do you seen in the pink coloured line in one word "])
            final = response.text
            print(final)
            
        # 4. Selection mode
        elif fingers[1] and fingers[2]:
            print("Selection mode")
            # Add futuristic mode indicator
            cv2.putText(img, "SELECT MODE", (20, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)  # Blue text
            
            if x1 < 100:  # Detect clicks in the left-side header
                if 400 < y1 < 450:
                    header = overlayList[0]
                    drawColor = (76, 0, 255)  # Purple color
                    # Futuristic tool selection indicator
                    cv2.circle(img, (50, 425), 15, (50, 0, 100), -1)  # Darker purple
                    cv2.circle(img, (50, 425), 20, (0, 0, 255), 1)  # Blue outline
                elif 500 < y1 < 600:
                    header = overlayList[1]
                    drawColor = (0, 0, 0)
                    # Futuristic tool selection indicator
                    cv2.circle(img, (50, 550), 15, (50, 0, 100), -1)  # Darker purple
                    cv2.circle(img, (50, 550), 20, (0, 0, 255), 1)  # Blue outline

            # Draw futuristic crosshair cursor
            cv2.line(img, (x1-15, y1), (x1+15, y1), drawColor, 2)
            cv2.line(img, (x1, y1-15), (x1, y1+15), drawColor, 2)

        # 5. If drawing mode - Index finger is up
        elif fingers[1] and not fingers[2] and 700 < x1 < 1200 and 50 < y1 < 600:
            # Display mode
            cv2.putText(img, "DRAW MODE", (20, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)  # Blue text
            
            # Futuristic cursor
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)  # Blue outline
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
    else:
        # Clear points when hand is not detected
        points.clear()
                        
    # Display AI result with futuristic styling
    if final:
        cv2.rectangle(img, (190, 550), (610, 630), (50, 0, 100), -1)  # Dark purple background
        cv2.rectangle(img, (190, 550), (610, 630), (0, 0, 255), 1)  # Blue border
        cv2.putText(img, f"AI SCAN: {final}", (200, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (76, 0, 255), 2, cv2.LINE_AA)  # Purple text
   
    # Setting the header image
    img[50:600, 700:1200] = cv2.addWeighted(img[50:600, 700:1200], 0.5, np.full_like(img[50:600, 700:1200], (255, 255, 255), dtype=np.uint8), 0.5, 0)

    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)  # Merge
    
    # Resize header to fit the left-side placement
    header_resized = cv2.resize(header, (100, 720))  # Resize to (width=100, height=720)
    img[0:720, 0:100] = header_resized  # Place header on the left side

    img = cv2.addWeighted(img, 1.0, imgCanvas, 0.6, 0)
    
    # Add futuristic tool labels with red color
    cv2.putText(img, "<DRAW>", (25, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)  # Blue text
    cv2.putText(img, "<ERASE>", (25, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)  # Blue text
    
    # Add subtle grid pattern to drawing area
    for i in range(750, 1151, 50):
        alpha = 0.2  # Make lines subtle
        cv2.line(img, (i, 50), (i, 600), (0, 0, 255), 1, cv2.LINE_AA)  # Blue vertical lines
        cv2.line(img, (700, 50 + (i-750)), (1200, 50 + (i-750)), (76, 0, 255), 1, cv2.LINE_AA)  # Purple horizontal lines
    
    # Add app title with red color
    cv2.putText(img, "NEURO-DRAW v2.0", (1050, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)  # Blue text

    cv2.imshow("NEURO-DRAW v2.0", img)
    cv2.waitKey(1)