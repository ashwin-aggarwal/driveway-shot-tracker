import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/driveway basketball v2.v2-version1july16th.yolov8/runs/detect/train/weights/best.pt")

# Open the video file (replace with your video path)
cap = cv2.VideoCapture("/Users/ashwinaggarwal/CS_Projects/driveway-shot-tracker/outputs/splitclips_from_timestamps/cleaned_full_clip.mp4")

# Track previous ball center for motion analysis
prev_ball_center = None



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

#Taking three points and seeing if they are 'collinear' enough by calculating the area of the triangle they form, and
#if the area is less than a threshold called "tolerance", then they are collinear
def are_colinear_enough(p1, p2, p3, tolerance=0.25):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    area = abs((x1 * (y2 - y3) +
                x2 * (y3 - y1) +
                x3 * (y1 - y2)) / 2.0) / 100000
    
    print(f"Area of triangle formed by points {p1}, {p2}, {p3}: {area}")
    return area < tolerance


# === Main loop to process video ===
# Store history of ball centers (for plotting red dots)
above_hoopbox_points = []
in_hoopbox_points =[]
below_hoopbox_points = []
ball_history = []
MAX_HISTORY = 60

shot_started = False # Whether a shot has started
shot_logged = False  # Whether the shot has been logged
total_shots = 0
makes = 0
a,b,c = None, None, None  # Points for triangle method


while True:
    ret, frame = cap.read()

    if not ret:
        # No more frames, just wait for 'q' to quit
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        else:
            continue  # Keep waiting

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

        # drawing a green line under the hoop
        cv2.line(frame, (0 , int(hoop_bottom)), (frame.shape[1], int(hoop_bottom)), (0, 255, 0), thickness=5)
        # Draw hoop center as a big green dot
        # cv2.circle(frame, (int(hoop_x), int(hoop_y)), 20, (0, 255, 0), -1)

    #start tracking the shot if the ball is above the hoop box
    if not shot_started and len(above_hoopbox_points) > 0:
        shot_started = True
    
    #log the shot once it finishes, meaning the ball is below the hoop box
    if shot_started and not shot_logged and len(below_hoopbox_points) > 0:
        total_shots += 1
        shot_logged = True

    if shot_started and not shot_logged and not ball_center: #in case ball bricks so hard it is out of frame
        total_shots += 1
        shot_logged = True



        # now detect if it was a make using triangle method
        a = above_hoopbox_points[-1]  # last point above hoop
        b = (int(hoop_x), int(hoop_y))  # hoop center
        c = below_hoopbox_points[0]  # first point below hoop


        if are_colinear_enough(a, b, c):
            makes += 1
            print('🎯 Shot Made!')
        else:
            print('❌ Shot Missed!')

        # Reset shot tracking
        if shot_logged:
            above_hoopbox_points = []
            in_hoopbox_points =[]
            below_hoopbox_points = []
            ball_history = []
            shot_started = False # Whether a shot has started
            shot_logged = False  # Whether the shot has been logged
            total_shots = 0
            makes = 0
            a,b,c = None, None, None  # Points for triangle method


    #Show the shot making percentage on the frame
    fg_percent = (100 * makes / total_shots) if total_shots > 0 else 0    
    score_text = f"FG%: {makes} / {total_shots} = {fg_percent}" 
    cv2.putText(frame, score_text, (20, 130),
    cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 255), thickness=3)



# Draw the current frame with detected objects

    #Draw current ball center and update history
    if ball_center:
        cx, cy = int(ball_center[0]), int(ball_center[1])
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)  # red dot
        ball_history.append((cx, cy))
        prev_ball_center = (cx, cy)

        #Adding ball to correct sublist
        if hoop_top >= cy:
            above_hoopbox_points.append((cx, cy))
        elif hoop_left <= cx <= hoop_right and hoop_top > cy > hoop_bottom:
            in_hoopbox_points.append((cx, cy))
        elif cy > hoop_bottom:
            below_hoopbox_points.append((cx, cy))

        # Keep only last MAX_HISTORY dots in all the lists
        if len(ball_history) > MAX_HISTORY:
            ball_history.pop(0)

        if len(above_hoopbox_points) > 3:
            above_hoopbox_points.pop(0)

        if len(in_hoopbox_points) > 5:
            in_hoopbox_points.pop(0)

        if len(below_hoopbox_points) > 3:
            below_hoopbox_points.pop() # we want the first one in the list for the area of the triangle


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
    # for p in [a,b,c]:
    #     cv2.circle(frame, p, 20, (0, 255, 80), -1)



    # Show the frame
    cv2.imshow("Basketball Shot Tracker", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()


  # if prev_ball_center:
        #     prev_cx, prev_cy = int(prev_ball_center[0]), int(prev_ball_center[1])

        #     # Is the ball falling?
        #     falling = cy > prev_cy

        #     # --- SHOT TAKEN ---
        #     if not shot_in_progress and prev_cy < hoop_bottom and cy >= hoop_bottom:
        #         total_shots += 1
        #         shot_in_progress = True
        #         made_in_this_shot = False
        #         print("🎯 Shot Taken!")

        #     # --- SHOT MADE ---
        #     if shot_in_progress and not made_in_this_shot:
        #         if hoop_left <= cx <= hoop_right and hoop_top <= cy <= hoop_bottom:
        #             makes += 1
        #             made_in_this_shot = True
        #             print(" Shot Made!")

        #     # --- Reset when ball drops far below or disappears ---
        #     if shot_in_progress and cy > hoop_bottom + 100:
        #         shot_in_progress = False
        #         made_in_this_shot = False

        #the green line needs to go
        # old shots of red dots