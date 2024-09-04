import cv2
from pose_estimation.angle_calculation import calculate_angle
import time

class PushUp:
    def __init__(self):
        self.counter = 0
        self.stage = "Initial"  # 'up' or 'down'
        self.angle_threshold_up = 150  # Upper threshold for 'up' stage
        self.angle_threshold_down = 70  # Lower threshold for 'down' stage
        self.last_counter_update = time.time()  # Track the time of the last counter update

    def calculate_shoulder_elbow_hip_angle(self, shoulder, elbow, hip):
        """Calculate the angle between shoulder, elbow, and hip."""
        return calculate_angle(shoulder, elbow, hip)

    def track_push_up(self, landmarks, frame):
        # Right side landmarks (shoulder, elbow, hip)
        shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_left = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        wrist_left = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_right = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        wrist_right = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]


        # Calculate the angle for the right side (shoulder, elbow, hip)
        angle_left = self.calculate_shoulder_elbow_hip_angle(shoulder_left, elbow_left, wrist_left)
        angle_right = self.calculate_shoulder_elbow_hip_angle(shoulder_right, elbow_right, wrist_right)

        # Draw lines between landmarks and angle
        cv2.line(frame, shoulder_left, elbow_left, (0, 255, 0), 2)  # Shoulder - Elbow
        cv2.line(frame, elbow_left, wrist_left, (0, 255, 0), 2)  # Elbow - Wrist

        # draw lines between landmarks and angle for right side
        cv2.line(frame, shoulder_right, elbow_right, (0, 255, 0), 2)  # Shoulder - Elbow
        cv2.line(frame, elbow_right, wrist_right, (0, 255, 0), 2)  # Elbow - Wrist

        # Draw angle text
        angle_text_position = (elbow_left[0] + 10, elbow_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_left)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # draw angle text for right side
        angle_text_position_right = (elbow_right[0] + 10, elbow_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_left)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

        # Get current time
        current_time = time.time()

        # Update stage and counter
        if angle_left > self.angle_threshold_up:
            self.stage = "Starting position"
        elif self.angle_threshold_down < angle_left < self.angle_threshold_up and self.stage == "Starting position":
            self.stage = "Descent"
        elif angle_left < self.angle_threshold_down and self.stage == "Descent":
            self.stage = "Ascent"
            # Increment counter only if enough time has passed since last update
            if current_time - self.last_counter_update > 1:  # 1 second threshold
                self.counter += 1
                self.last_counter_update = current_time

        return self.counter, angle_left, self.stage
