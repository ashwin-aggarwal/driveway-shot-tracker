# 🏀 Basketball Shot Tracker (YOLOv8)

This project uses a custom-trained YOLOv8 model to detect basketball shots in video footage. It tracks the basketball and hoop in real time, determines whether a shot is made or missed, and displays field goal percentage (FG%) live on screen.

## 📦 Features

- ✅ Detects **ball** and **hoop** using a YOLOv8 model
- 🟢 Determines **makes vs. misses** using a triangle heuristic
- 📈 Calculates and displays **FG%** as you shoot
- 🔴 Tracks and visualizes **ball trajectory**
- 🎯 Logs shot outcomes with visual and console feedback
- 🧼 Includes FFmpeg-based script to **clean and re-encode videos** for smoother YOLO performance

<table>
  <tr>
    <td><img src="testvideos/make.gif" width="300"/></td>
    <td><img src="testvideos/miss.gif" width="300"/></td>
  </tr>
  <tr>
    <td align="center"><b>Made Shot</b></td>
    <td align="center"><b>Missed Shot</b></td>
  </tr>
</table>

## 🧠 Model Details

Custom YOLOv8 model trained on basketball video clips:

| Class | mAP50 |
|-------|-------|
| Ball  | 0.985 |
| Hoop  | 0.980 |

- Model path: `yolov8_model/model.pt`
- Classes defined in: `yolov8_model/data.yaml`

## 🗂️ File Structure
driveway-shot-tracker/
- detector.py # Core detection & tracking logic
- main.py # Main script to run everything
- ffmpeg_utils.py # FFmpeg-based video cleaner
- yolov8_model/
  -  model.pt # Trained YOLOv8 weights
  - data.yaml # Class labels
- requirements.txt # Python dependencies
-  README.md # This file
- testvideos has examples of an input before the cleaning, after the cleaning, and the output.


## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ashwin-aggarwal/driveway-shot-tracker.git
cd driveway-shot-tracker

pip install -r requirements.txt

Also install FFmpeg on your system to put the video into correct format: #takes a while

    macOS: brew install ffmpeg

    Ubuntu: sudo apt install ffmpeg

    Windows: Download FFmpeg

#Run the shot tracker
python main.py

🎯 Shot Logic

    A shot starts when the ball is seen above the hoop box

    A shot ends when the ball goes below the hoop or disappears

    A "make" is counted if the ball travels in a roughly collinear path through the hoop

    Otherwise, it's a miss

    All outcomes update the FG% in real time

📊 Output

    Blue bounding box around the hoop

    Red dot trail for ball movement

    Green line below the hoop

    On-screen FG%

    Console messages for each shot:
    🎯 Shot Made! or ❌ Shot Missed


Press the q key to end the shot tracking visual screen

    🧑‍💻 Author

    Ashwin Aggarwal
    Cornell University — CS & AI
    GitHub: @ashwin-aggarwal
    Linkedin: https://www.linkedin.com/in/ashwin-aggarwal/
