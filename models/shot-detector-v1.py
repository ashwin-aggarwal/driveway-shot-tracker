import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/driveway basketball v2.v2-version1july16th.yolov8/runs/detect/train/weights/best.pt")

# Open the video file (replace with your video path)
cap = cv2.VideoCapture("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/outputs/splitclips_from_timestamps/batch2/clip_006.mp4")

# Track previous ball center for motion analysis
prev_ball_center = None

# Store history of ball centers (for plotting red dots)
ball_history = []
MAX_HISTORY = 60

# === Helper function to extract the most confident ball and hoop ===
def extract_ball_and_hoop(results):
    detections = results[0].boxes
    class_names = results[0].names

    ball_center = None
    hoop_box = None
    max_ball_conf = 0
    max_hoop_conf = 0

    for i in range(len(detections)):
        box = detections[i]
        cls_id = int(box.cls[0])
        label = class_names[cls_id]
        conf = float(box.conf[0])
        x, y, w, h = box.xywh[0]  # center x, center y, width, height

        if label == "ball" and conf > max_ball_conf:
            ball_center = (float(x), float(y))
            max_ball_conf = conf

        elif label == "hoop" and conf > max_hoop_conf:
            hoop_box = (float(x), float(y), float(w), float(h))
            max_hoop_conf = conf

    return ball_center, max_ball_conf, hoop_box, max_hoop_conf

# === Main loop to process video ===

total_shots = 0
makes = 0
shot_in_progress = False
made_in_this_shot = False


while True:
    ret, frame = cap.read()
    if not ret:
        break  # Video is finished

    # Run prediction on the current frame
    results = model.predict(frame, conf=0.4, verbose=False)

    # Extract the current frame's ball and hoop info
    ball_center, max_ball_conf, hoop_box, max_hoop_conf = extract_ball_and_hoop(results)

    if ball_center and hoop_box:
        cx, cy = int(ball_center[0]), int(ball_center[1])
        hoop_x, hoop_y, hoop_w, hoop_h = hoop_box

        hoop_left = hoop_x - hoop_w / 2
        hoop_right = hoop_x + hoop_w / 2
        hoop_top = hoop_y - hoop_h / 2
        hoop_bottom = hoop_y + hoop_h / 2

        if prev_ball_center:
            prev_cx, prev_cy = int(prev_ball_center[0]), int(prev_ball_center[1])

            # Is the ball falling?
            falling = cy > prev_cy

            # --- SHOT TAKEN ---
            if not shot_in_progress and prev_cy < hoop_bottom and cy >= hoop_bottom:
                total_shots += 1
                shot_in_progress = True
                made_in_this_shot = False
                print("🎯 Shot Taken!")

            # --- SHOT MADE ---
            if shot_in_progress and not made_in_this_shot:
                if hoop_left <= cx <= hoop_right and hoop_top <= cy <= hoop_bottom:
                    makes += 1
                    made_in_this_shot = True
                    print(" Shot Made!")

            # --- Reset when ball drops far below or disappears ---
            if shot_in_progress and cy > hoop_bottom + 100:
                shot_in_progress = False
                made_in_this_shot = False



    fg_percent = (100 * makes / total_shots) if total_shots > 0 else 0    
    score_text = f"FG%: {makes} / {total_shots} = {fg_percent}" 
    cv2.putText(frame, score_text, (20, 130),
    cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 255), thickness=3)









##################################
    #Draw current ball center and update history
    if ball_center:
        cx, cy = int(ball_center[0]), int(ball_center[1])
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)  # red dot
        ball_history.append((cx, cy))
        prev_ball_center = (cx, cy)

        # Keep only last MAX_HISTORY dots
        if len(ball_history) > MAX_HISTORY:
            ball_history.pop(0)

    # Draw current hoop bounding box
    if hoop_box:
        x, y, w, h = hoop_box
        top_left = (int(x - w / 2), int(y - h / 2))
        bottom_right = (int(x + w / 2), int(y + h / 2))
        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 10)  # blue 

        # Drawing confidence label
        label = f"HOOP {max_hoop_conf:.2f}"
        cv2.putText(frame, label, (top_left[0], top_left[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=3)

    # Draw history of red dots
    for (hx, hy) in ball_history:
        cv2.circle(frame, (hx, hy), 10, (0, 0, 255), -1)


    # Show the frame
    cv2.imshow("Basketball Shot Tracker", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) | 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
