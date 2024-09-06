import cv2
import numpy as np
from pose_estimation.angle_calculation import calculate_angle

class HammerCurl:
    def __init__(self):
        self.counter_right = 0
        self.counter_left = 0
        self.stage_right = None  # 'up' or 'down' for right arm
        self.stage_left = None  # 'up' or 'down' for left arm

        self.angle_threshold = 40  # Angle threshold for misalignment
        self.flexion_angle_up = 155  # Flexion angle for 'up' stage
        self.flexion_angle_down = 35  # Flexion angle for 'down' stage

        self.angle_threshold_up = 155  # Upper threshold for 'up' stage
        self.angle_threshold_down = 47  # Lower threshold for 'down' stage

    def calculate_shoulder_elbow_hip_angle(self, shoulder, elbow, hip):
        """Calculate the angle between shoulder, elbow, and hip."""
        return calculate_angle(elbow, shoulder, hip)

    def calculate_shoulder_elbow_wrist(self, shoulder, elbow, wrist):
        """Calculate the angle between shoulder, elbow, and wrist."""
        return calculate_angle(shoulder, elbow, wrist)

    def track_hammer_curl(self, landmarks, frame):
        # Right arm landmarks (shoulder, elbow, hip, wrist)
        shoulder_right = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_right = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        hip_right = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        wrist_right = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        # Left arm landmarks (shoulder, elbow, hip, wrist)
        shoulder_left = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_left = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        hip_left = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        wrist_left = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        # Calculate the angle for counting (elbow flexion angle)
        angle_right_counter = self.calculate_shoulder_elbow_wrist(shoulder_right, elbow_right, wrist_right)
        angle_left_counter = self.calculate_shoulder_elbow_wrist(shoulder_left, elbow_left, wrist_left)

        # Calculate the angle for the right arm (shoulder, elbow, hip)
        angle_right = self.calculate_shoulder_elbow_hip_angle(shoulder_right, elbow_right, hip_right)

        # Calculate the angle for the left arm (shoulder, elbow, hip)
        angle_left = self.calculate_shoulder_elbow_hip_angle(shoulder_left, elbow_left, hip_left)

        # Draw lines with improved style
        self.draw_line_with_style(frame, shoulder_left, elbow_left, (0, 0, 255), 4)
        self.draw_line_with_style(frame, elbow_left, wrist_left, (0, 0, 255), 4)

        self.draw_line_with_style(frame, shoulder_right, elbow_right, (0, 0, 255), 4)
        self.draw_line_with_style(frame, elbow_right, wrist_right, (0, 0, 255), 4)

        # Add circles to highlight key points
        self.draw_circle(frame, shoulder_left, (0, 0, 255), 8)
        self.draw_circle(frame, elbow_left, (0, 0, 255), 8)
        self.draw_circle(frame, wrist_left, (0, 0, 255), 8)

        self.draw_circle(frame, shoulder_right, (0, 0, 255), 8)
        self.draw_circle(frame, elbow_right, (0, 0, 255), 8)
        self.draw_circle(frame, wrist_right, (0, 0, 255), 8)

        # Convert the angles to integers and update the text positions
        angle_text_position_left = (elbow_left[0] + 10, elbow_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_left_counter)}', angle_text_position_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                     (255, 255, 255), 2)

        angle_text_position_right = (elbow_right[0] + 10, elbow_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_right_counter)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255), 2)

        warning_message_right = None
        warning_message_left = None

        # Check for misalignment based on shoulder-elbow-hip angle
        if abs(angle_right) > self.angle_threshold:
            warning_message_right = f"Right Shoulder-Elbow-Hip Misalignment! Angle: {angle_right:.2f}°"
        if abs(angle_left) > self.angle_threshold:
            warning_message_left = f"Left Shoulder-Elbow-Hip Misalignment! Angle: {angle_left:.2f}°"

        if angle_right_counter > self.angle_threshold_up:
            self.stage_right = "Flex"
        elif self.angle_threshold_down < angle_right_counter < self.angle_threshold_up and self.stage_right == "Flex":
            self.stage_right = "Up"
        elif angle_right_counter < self.angle_threshold_down and self.stage_right=="Up":
            self.stage_right = "Down"
            self.counter_right +=1

        if angle_left_counter > self.angle_threshold_up:
            self.stage_left = "Flex"
        elif self.angle_threshold_down < angle_left_counter < self.angle_threshold_up and self.stage_left == "Flex":
            self.stage_left = "Up"
        elif angle_left_counter < self.angle_threshold_down and self.stage_left == "Up":
            self.stage_left = "Down"
            self.counter_left +=1

        # Progress percentages: 1 for "up", 0 for "down"
        progress_right = 1 if self.stage_right == "up" else 0
        progress_left = 1 if self.stage_left == "up" else 0

        return self.counter_right, angle_right_counter, self.counter_left, angle_left_counter, warning_message_right, warning_message_left, progress_right, progress_left, self.stage_right, self.stage_left

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        """Draw a circle with specified style."""
        cv2.circle(frame, center, radius, color, -1)  # -1 to fill the circle
