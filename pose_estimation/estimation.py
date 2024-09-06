import cv2
import mediapipe as mp
from exercises.hammer_curl import HammerCurl

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def estimate_pose(self, frame, exercise_type):
        # BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Pose estimate
        results = self.pose.process(rgb_frame)

        # Draw landmarks and specific connections based on exercise type
        if results.pose_landmarks:
            # Draw specific landmarks and connections based on exercise_type
            if exercise_type == "squat":
                self.draw_squat_lines(frame, results.pose_landmarks.landmark)
            elif exercise_type == "push_up":
                self.draw_push_up_lines(frame, results.pose_landmarks.landmark)
            elif exercise_type == "hammer_curl":
                self.draw_hammerl_curl_lines(frame, results.pose_landmarks.landmark)

        return results
    def draw_hammerl_curl_lines(self, frame, landmarks):

        shoulder_right = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_right = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        hip_right = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        wrist_right = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        # Left arm landmarks (shoulder, elbow, hip, wrist)
        shoulder_left = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_left = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        hip_left = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        wrist_left = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        # Draw lines with improved style
        cv2.line(frame, shoulder_left, elbow_left, (0, 0, 255), 4,2)
        cv2.line(frame, elbow_left, wrist_left, (0, 0, 255), 4,2)

        cv2.line(frame, shoulder_right, elbow_right, (0, 0, 255), 4,2)
        cv2.line(frame, elbow_right, wrist_right, (0, 0, 255), 4,2)



    def draw_squat_lines(self, frame, landmarks):
        # Squat specific lines (hip, knee, shoulder)
        hip = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        knee = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
        shoulder = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]

        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]

        # Draw lines for squat
        cv2.line(frame, shoulder, hip, (178, 102, 255), 2)
        cv2.line(frame, hip, knee, (178, 102, 255), 2)
        cv2.line(frame, shoulder_right, hip_right, (51, 153, 255), 2)
        cv2.line(frame, hip_right, knee_right, (51, 153, 255), 2)

    def draw_push_up_lines(self, frame, landmarks):
        # Push-up specific lines (shoulder, elbow, wrist)
        shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_left = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        wrist_left = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_right = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        wrist_right = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        # Draw lines for push-up
        cv2.line(frame, shoulder_left, elbow_left, (0, 0, 255), 2)
        cv2.line(frame, elbow_left, wrist_left, (0, 0, 255), 2)
        cv2.line(frame, shoulder_right, elbow_right, (102, 0, 0), 2)
        cv2.line(frame, elbow_right, wrist_right, (102, 0, 0), 2)
