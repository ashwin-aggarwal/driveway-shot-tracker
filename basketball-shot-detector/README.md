# 🏀 Basketball Shot Detector (YOLOv8)

This is a YOLOv8 model trained to detect basketballs and hoops. It's used to power a shot tracker system that counts makes and misses in real-time.

## Files
- `yolov8_model/model.pt` – Trained YOLOv8 weights
- `yolov8_model/data.yaml` – Class labels
- `runs/` – Training logs and evaluation plots

## Example Usage

```python
from ultralytics import YOLO
model = YOLO("yolov8_model/model.pt")
results = model("your_video.mp4")
results.show()
