import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def estimate_pose(self,frame):
        # BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Pose estimate
        results = self.pose.process(rgb_frame)

        # anahtar noktaları ve iskelet için
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame,results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)
        return results
