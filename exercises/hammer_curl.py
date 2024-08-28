from pose_estimation.angle_calculation import calculate_angle
import cv2
class HammerCurl:
    def __init__(self):
        self.counter_right = 0
        self.counter_left = 0
        # up or down for arms
        self.stage_right = None
        self.stage_left = None

    def track_hammer_curl(self,landmarks):
        # sağ kol için omuz dirsek ve bilek noktaları
        shoulder_right = [landmarks[11].x, landmarks[11].y]
        elbow_right = [landmarks[13].x, landmarks[13].y]
        wrist_right = [landmarks[15].x, landmarks[15].y]

        # sol kol için omuz dirsek ve bilek noktaları
        shoulder_left = [landmarks[12].x, landmarks[12].y]
        elbow_left = [landmarks[14].x, landmarks[14].y]
        wrist_left = [landmarks[16].x, landmarks[16].y]

        # sağ kol için açıyı hesapla
        angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
        # sol kol için açıyı hesapla
        angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)

        # Sağ kol için stage ve sayacı güncelle
        if angle_right > 160:
            self.stage_right = "down"
        if angle_right < 30 and self.stage_right == "down":
            self.stage_right = "up"
            self.counter_right += 1

        # Sol kol için stage ve sayacı güncelle
        if angle_left > 160:
            self.stage_left = "down"
        if angle_left < 30 and self.stage_left == "down":
            self.stage_left = "up"
            self.counter_left += 1

        return self.counter_right, angle_right, self.counter_left, angle_left
