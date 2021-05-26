# Author: Christopher Rossi
# Project Name: PushEZ - Pushup Counter
# Start Date: 5/2/2021
# End Date: 5/24/2021

# Import dependencies
import cv2 as cv
import mediapipe as mp
import numpy as np
import csv

# Variable setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
counter = 0
fieldnames = ["counter"]

# Pushup positions
up_pos = None
down_pos = None
pushup_pos = None
display_pos = None

# Webcam setup for opencv
cap = cv.VideoCapture(0)


# Function to calculate angle between 3 given landmarks/body points
def calculate_angle(first, mid, end):
    first = np.array(first)
    mid = np.array(mid)
    end = np.array(end)

    # end[1] - mid[1] --> Subtracting y values from endpoint to mid
    # end[0] - mid[0] --> Subtracting x values from end to mid
    radians = np.arctan2(end[1] - mid[1], end[0] - mid[0]) - np.arctan2(first[1] - mid[1], end[0] - first[0])
    
    # Calculates 360 degree angle
    angle = np.abs(radians * 180.0 / np.pi)

    # Converts angle between 0 and 180 (max angle we need is 180 for our arm)
    if angle > 180.0:
        angle = 360 - angle

    # Rounds the angle to 2 decimal places (looks nicer when we display this angle)
    output = round(angle, 2)

    return output

# Csv file setup
with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Set up mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # Loop through video feed
    while True:
        # Csv file setup
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            _, frame = cap.read()

            # Recolour Image
            # We want the format of RBG instead of the standard BGR
            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Pose detection
            results = pose.process(image)

            # Recolour back to BGR for opencv to render
            image.flags.writeable = True
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

            # Try block to not end the program if nothing is detected
            # Extracts landmarks / body positions
            try:
                landmarks = results.pose_landmarks.landmark

                # Left Arm Coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Right Arm Coordinates
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate Left/Right Angles
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize elbow/landmark angle
                cv.putText(
                    image, str(left_angle),
                    # Angle will render right next to elbow --> multiplies the elbow position by webcam screen size
                    tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA
                )

                cv.putText(
                    image, str(right_angle),
                    tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA
                )

                # Push up counter logic
                if left_angle > 160:
                    up_pos = "up"
                    display_pos = 'up'
                if left_angle < 110 and up_pos == "up":
                    down_pos = "down"
                    display_pos = "down"
                if left_angle > 160 and down_pos == "down":
                    pushup_pos = "up"
                    display_pos = "up"
                    counter += 1
                    info = {"counter": counter}
                    csv_writer.writerow(info)

                    # Reset positions after a push up is complete to stop multiple pushup registers
                    up_pos = None
                    down_pos = None
                    pushup_pos = None

                    # print(counter)

            except:
                pass

            # Render curl counter & Setup status box
            cv.rectangle(image, (0, 0), (270, 73), (203, 61, 170), -1)

            # Display repetition data
            cv.putText(image, 'Repetitions:', (15, 12),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(image, str(counter), (10, 60),
                       cv.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2, cv.LINE_AA)

            # Display position data
            cv.putText(image, 'Position:', (120, 12),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(image, display_pos, (100, 60),
                       cv.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2, cv.LINE_AA)

            # Render detections & draw image
            # results.pose_landmarks   ---> shows the x,y,z & visibility of each landmark
            # mp_pose.POSE_CONNECTIONS ---> shows each landmark connection, i.e. NOSE, RIGHT_SHOULDER, etc.
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # Display opencv to the monitor
            cv.imshow('Mediapipe Feed', image)

            # Exit program logic
            if cv.waitKey(10) & 0xFF == ord('q'):
                break

    # Closes all opencv windows
    cap.release()
    cv.destroyAllWindows()
