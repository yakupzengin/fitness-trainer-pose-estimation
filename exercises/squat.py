import cv2
from pose_estimation.angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def calculate_angle(self, hip, knee, ankle):
        return calculate_angle(hip, knee, ankle)

    def track_squat(self, landmarks, frame):
        # Landmark coordinates
        hip = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        knee = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
        shoulder = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]

        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]

        # Calculate angles
        angle = self.calculate_angle(shoulder, hip, knee)
        angle_right = self.calculate_angle(shoulder_right, hip_right, knee_right)

        # Draw lines and circles to highlight key points
        self.draw_line_with_style(frame, shoulder, hip, (178, 102, 255), 2)
        self.draw_line_with_style(frame, hip, knee, (178, 102, 255), 2)
        self.draw_line_with_style(frame, shoulder_right, hip_right, (51, 153, 255), 2)
        self.draw_line_with_style(frame, hip_right, knee_right, (51, 153, 255), 2)

        self.draw_circle(frame, shoulder, (178, 102, 255), 8)
        self.draw_circle(frame, hip, (178, 102, 255), 8)
        self.draw_circle(frame, knee, (178, 102, 255), 8)
        self.draw_circle(frame, shoulder_right, (51, 153, 255), 8)
        self.draw_circle(frame, hip_right, (51, 153, 255), 8)
        self.draw_circle(frame, knee_right, (51, 153, 255), 8)

        # Display angles on screen
        angle_text_position = (knee[0] + 10, knee[1] - 10)
        cv2.putText(frame, f'Angle Left: {int(angle)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_right = (knee_right[0] + 10, knee_right[1] - 10)
        cv2.putText(frame, f'Angle Right: {int(angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Update exercise stage and counter
        if angle > 170:
            self.stage = "Starting Position"
        elif 90 < angle < 170 and self.stage == "Starting Position":
            self.stage = "Descent"
        elif angle < 90 and self.stage == "Descent":
            self.stage = "Ascent"
            self.counter += 1
        return self.counter, angle, self.stage

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        """Draw a line with specified style."""
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        """Draw a circle with specified style."""
        cv2.circle(frame, center, radius, color, -1)  # -1 to fill the circle
