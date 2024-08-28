from pose_estimation.angle_calculation import calculate_angle
import cv2
import math

class HammerCurl:
    def __init__(self):
        self.counter_right = 0
        self.counter_left = 0
        self.stage_right = None  # 'up' or 'down' for right arm
        self.stage_left = None   # 'up' or 'down' for left arm

    def calculate_shoulder_elbow_alignment(self, shoulder, elbow):
        """Omuz ve dirsek arasındaki sapmayı kontrol eden fonksiyon."""
        # Yatay eksenle omuz-dirsek doğrultusunun açısını hesapla
        delta_x = elbow[0] - shoulder[0]
        delta_y = elbow[1] - shoulder[1]
        angle = math.degrees(math.atan2(delta_y, delta_x))
        return angle

    def track_hammer_curl(self, landmarks):
        # Sağ kol için omuz, dirsek ve bilek noktaları
        shoulder_right = [landmarks[11].x, landmarks[11].y]
        elbow_right = [landmarks[13].x, landmarks[13].y]
        wrist_right = [landmarks[15].x, landmarks[15].y]

        # Sol kol için omuz, dirsek ve bilek noktaları
        shoulder_left = [landmarks[12].x, landmarks[12].y]
        elbow_left = [landmarks[14].x, landmarks[14].y]
        wrist_left = [landmarks[16].x, landmarks[16].y]

        # Sağ kol için açıyı hesapla
        angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
        # Sol kol için açıyı hesapla
        angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)

        # Omuz-dirsek arasındaki sapma açısını kontrol et (sağ kol)
        shoulder_elbow_angle_right = self.calculate_shoulder_elbow_alignment(shoulder_right, elbow_right)


        if not (40 <= shoulder_elbow_angle_right <= 110):
            print("Uyarı: Sağ omuz ve dirsek doğrultusu bozuldu! Açısı:", shoulder_elbow_angle_right)

        # Omuz-dirsek arasındaki sapma açısını kontrol et (sol kol)
        shoulder_elbow_angle_left = self.calculate_shoulder_elbow_alignment(shoulder_left, elbow_left)
        if not (40 <= shoulder_elbow_angle_left <= 110):
            print("Uyarı: Sol omuz ve dirsek doğrultusu bozuldu! Açısı:", shoulder_elbow_angle_left)

        is_shoulder_elbow_angle_right_ok = (40 <= shoulder_elbow_angle_right <= 110)
        is_shoulder_elbow_angle_left_ok = (40 <= shoulder_elbow_angle_left <= 110)

        print("is_shoulder_elbow_angle_left_ok", is_shoulder_elbow_angle_left_ok)
        print("is_shoulder_elbow_angle_right_ok", is_shoulder_elbow_angle_right_ok)
        # Sağ kol için stage ve sayacı güncelle

        if is_shoulder_elbow_angle_right_ok:

            if angle_right > 130:
                self.stage_right = "down"
            if angle_right < 85 and self.stage_right == "down":
                self.stage_right = "up"
                self.counter_right += 1
        if is_shoulder_elbow_angle_left_ok:
            # Sol kol için stage ve sayacı güncelle
            if angle_left > 130:
                self.stage_left = "down"
            if angle_left < 85 and self.stage_left == "down":
                self.stage_left = "up"
                self.counter_left += 1

        return self.counter_right, angle_right, self.counter_left, angle_left
