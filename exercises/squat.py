import cv2
from pose_estimation.angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def calculate_angle(self, hip, knee, ankle):
        return calculate_angle(hip, knee, ankle)

    def track_squat(self, landmarks, frame):
        # Landmark koordinatlarını al
        #kalça
        hip = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        knee = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
        shoulder = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]

        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]

        # Açı hesapla
        angle = self.calculate_angle(shoulder,hip, knee)
        angle_right = self.calculate_angle(shoulder_right, hip_right, knee_right)

        # Çizgilerle açıyı göster
        cv2.line(frame, hip, knee, (0, 255, 0), 2)  # Kalça - Diz
        cv2.line(frame, shoulder, hip, (0, 255, 0), 2)  # omuz - kalça

        cv2.line(frame, hip_right, knee_right,(0, 255, 0), 2)  # Kalça - Diz
        cv2.line(frame, shoulder_right, hip_right, (0, 255, 0), 2)  # omuz - kalça

        # Açıyı metin olarak ekrana yerleştir
        angle_text_position = (knee[0] + 10, knee[1] - 10)
        cv2.putText(frame, f'Angle Left: {int(angle)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_right = (knee_right[0] + 10, knee_right[1] - 10)
        cv2.putText(frame, f'Angle Right: {int(angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    2)

        # Egzersiz aşamasını güncelle

        if angle > 170:
            self.stage = "Ayakta"
        if 90< angle<170 and self.stage=="Ayakta":
            self.stage = "Descent"
        if angle<90 and self.stage=="Descent":
            self.stage = "Ascent"
            self.counter += 1

        #
        # if angle > 160:
        #     self.stage = "Descent"
        # if angle < 100 and self.stage == "Descent":
        #     self.stage = "Ascent"
        #     self.counter += 1

        return self.counter, angle, self.stage
