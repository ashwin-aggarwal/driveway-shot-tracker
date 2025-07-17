# Part 1: Imports and setup
import cv2
from ultralytics import YOLO
print('Packages imported successfully.')
model = YOLO("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/driveway basketball v2.v2-version1july16th.yolov8/runs/detect/train/weights/best.pt")
# results = model.predict(source="/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/outputs/splitclips_from_timestamps/batch2/clip_005.mp4", save=True, conf=0.5)

def extract_ball_and_hoop(results):
    """
    Extracts the center of the highest-confidence ball detection,
    and the bounding box of the highest-confidence hoop detection.
    
    Returns:
        ball_center: tuple (cx, cy) or None
        hoop_box: tuple (x, y, w, h) or None
    """
    # Get the first frame’s detections (YOLOv8 supports batch, but you're only doing one frame)
    detections = results[0].boxes
    
    # Get class names (so we can convert class index → string label)
    class_names = results[0].names  # e.g., {0: 'ball', 1: 'hoop'}

    # Initialize variables to store best detections
    ball_center = None
    hoop_box = None
    max_ball_conf = 0
    max_hoop_conf = 0

    # Loop through all detected boxes in this frame
    for i in range(len(detections)):
        box = detections[i]

        # Get class index and convert to label
        cls_id = int(box.cls[0])  # e.g., 0 or 1
        label = class_names[cls_id]  # 'ball' or 'hoop'

        # Get confidence score
        conf = float(box.conf[0])

        # Get bounding box coordinates (xywh format)
        x, y, w, h = box.xywh[0]  # xywh = center_x, center_y, width, height

        # Extract data based on class label
        if label == "ball" and conf > max_ball_conf:
            # Save center of the ball
            ball_center = (float(x), float(y))
            max_ball_conf = conf

        elif label == "hoop" and conf > max_hoop_conf:
            # Save full box of the hoop
            hoop_box = (float(x), float(y), float(w), float(h))
            max_hoop_conf = conf

    return ball_center, hoop_box

cap = cv2.VideoCapture("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/outputs/splitclips_from_timestamps/batch2/clip_005.mp4")
ret, frame = cap.read()  # read the first frame
cap.release()
results = model.predict(frame)
ball_center, hoop_box = extract_ball_and_hoop(results)
print("Ball center:", ball_center)
print("Hoop box:", hoop_box)
cv2.circle(frame, (int(ball_center[0]), int(ball_center[1])), 5, (0, 0, 255), -1)
x, y, w, h = hoop_box
cv2.rectangle(frame, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (255, 0, 0), 2)
cv2.imshow("Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

