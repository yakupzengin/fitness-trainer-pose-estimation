from idlelib.configdialog import tracers

import cv2
from pose_estimation.estimation import PoseEstimator
from exercises.hammer_curl import HammerCurl

def main():
    # videoData = r"C:\Users\yakupzengin\Fitness-Trainer\data\dumbel-workout.mp4"
    videoData = (r"C:\Users\yakupzengin\Fitness-Trainer\data\dumbel-wrong-pose-workout.mp4")
    cap = cv2.VideoCapture(videoData)


    pose_estimator = PoseEstimator()
    hammer_curl = HammerCurl()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("---- BRO , VİDEO İS NOT READY ----")

        # poz tahmini
        results = pose_estimator.estimate_pose(frame)
        if results.pose_landmarks:
            # hammerl takipi
            counter_right  , angle_right , counter_left ,angle_left= hammer_curl.track_hammer_curl(results.pose_landmarks.landmark)

            # ekranda sayacı ve açıyı göster
            cv2.putText(frame, f'Counter: {counter_right}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Angle Right: {int(angle_right)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Counter: {counter_left}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Angle Left: {int(angle_left)}', (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Hammer Curl Tracker", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()