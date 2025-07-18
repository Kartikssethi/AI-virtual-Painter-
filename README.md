# AI Virtual Painter

An interactive, AI-powered virtual drawing game that uses hand tracking and computer vision to let you draw in the air using your webcam. The AI then tries to guess what you drew! Inspired by Pictionary, this project combines gesture recognition, drawing, and generative AI for a futuristic, fun experience.

## Features
- **Hand Tracking Drawing:** Draw in the air using your index finger, with real-time gesture recognition (powered by MediaPipe and OpenCV).
- **AI Guessing Game:** Get a random prompt, draw it, and let Google Gemini AI guess your drawing.
- **Futuristic UI:** Modern, sci-fi inspired interface with overlays, scanner lines, and hex patterns.
- **Multiple Tools:** Switch between brush and eraser using hand gestures.
- **Prompt System:** Random drawing prompts for endless fun.
- **Test Scripts:** Several test scripts for experimenting with different features and UI layouts.

## Demo
![Demo Screenshot](screenshot/myimg.png)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd AI-virtual-Painter-
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   You may also need to install `mediapipe` manually:
   ```bash
   pip install mediapipe
   ```

## Usage
- **Main Game:**
  Run the main AI guessing game:
  ```bash
  python final.py
  ```
- **Classic Drawing Mode:**
  ```bash
  python main.py
  ```
- **Test Scripts:**
  Try out different features or UI layouts:
  ```bash
  python test1.py
  python test2.py
  python test3.py
  python test5.py
  ```

## Controls & Instructions
- **Drawing:** Use your index finger to draw in the air (in front of your webcam).
- **Selection Mode:** Hold up your index and middle fingers to select tools (brush/eraser) from the sidebar.
- **Submit Drawing:** Press `S` to submit your drawing for AI guessing.
- **New Prompt:** Press `N` for a new drawing prompt.
- **Quit:** Press `Q` to exit.

## File Structure
- `final.py` - Main AI guessing game with futuristic UI and prompt system.
- `main.py` - Classic virtual painter (no AI guessing).
- `HandTracking.py` - Hand tracking module using MediaPipe.
- `test1.py`, `test2.py`, `test3.py`, `test5.py` - Test/demo scripts.
- `Header/`, `Test_header/` - Toolbar/header images.
- `screenshot/` - Screenshots and output images.
- `requirements.txt` - Python dependencies.

## Dependencies
- opencv-python
- numpy
- mediapipe
- pyautogui
- google-generativeai

Install all with `pip install -r requirements.txt` (plus `mediapipe` if needed).

## Notes
- You need a webcam to use this project.
- For AI guessing, you need a valid Google Generative AI API key. Set it in `final.py` (see `genai.configure(api_key=...)`).
- The project is for educational and entertainment purposes.

## Credits
- Hand tracking powered by [MediaPipe](https://google.github.io/mediapipe/).
- AI guessing powered by [Google Gemini](https://ai.google.dev/).
- Developed by Kartik Sethi.
