import cv2
from pose_estimation.estimation import PoseEstimator
from exercises.squat import Squat
from exercises.hammer_curl import HammerCurl
from exercises.push_up import PushUp
from feedback.layout import layout_indicators
from feedback.information import get_exercise_info
from utils.draw_text_with_background import draw_text_with_background

def main():
    video_path = r"C:\Users\yakupzengin\Fitness-Trainer\data\dumbel-workout.mp4"
    video_path = r"C:\Users\yakupzengin\Fitness-Trainer\data\squat.mp4"
    video_path = r"C:\Users\yakupzengin\Fitness-Trainer\data\push_up.mp4"

    exercise_type = "push_up"  # Egzersiz türünü belirleyin ("hammer_curl", "squat", "push_up")

    cap = cv2.VideoCapture(video_path)
    pose_estimator = PoseEstimator()

    if exercise_type == "hammer_curl":
        exercise = HammerCurl()
    elif exercise_type == "squat":
        exercise = Squat()
    elif exercise_type == "push_up":
        exercise = PushUp()
    else:
        print("Invalid exercise type.")
        return

    exercise_info = get_exercise_info(exercise_type)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_file = r"C:\Users\yakupzengin\Fitness-Trainer\output\push-up.avi"
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = pose_estimator.estimate_pose(frame, exercise_type)
        if results.pose_landmarks:
            if exercise_type == "squat":
                counter, angle, stage = exercise.track_squat(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage))
            elif exercise_type == "hammer_curl":
                (counter_right, angle_right, counter_left, angle_left,
                 warning_message_right, warning_message_left, progress_right, progress_left, stage_right, stage_left) = exercise.track_hammer_curl(
                    results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type,
                                  (counter_right, angle_right, counter_left, angle_left,
                                   warning_message_right, warning_message_left, progress_right, progress_left, stage_right, stage_left))
            elif exercise_type == "push_up":
                counter, angle, stage = exercise.track_push_up(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage))

        draw_text_with_background(frame, f"Exercise: {exercise_info.get('name', 'N/A')}", (40, 50),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255,), (118, 29, 14, 0.79), 1)
        draw_text_with_background(frame, f"Reps: {exercise_info.get('reps', 0)}", (40, 80),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255,), (118, 29, 14, 0.79), 1)
        draw_text_with_background(frame, f"Sets: {exercise_info.get('sets', 0)}", (40, 110),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255,), (118, 29, 14, 0.79),1 )

        out.write(frame)

        cv2.namedWindow(f"{exercise_type.replace('_', ' ').title()} Tracker", cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f"{exercise_type.replace('_', ' ').title()} Tracker", 1920, 1080)
        cv2.imshow(f"{exercise_type.replace('_', ' ').title()} Tracker", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
