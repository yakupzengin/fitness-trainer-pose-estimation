import cv2
import numpy as np
from feedback.information import get_exercise_info

def draw_progress_bar(frame,exercise, value, max_value, position, size=(200, 20), color=(6, 112, 2)):
    x, y = position
    width, height = size

    # Progress bar background
    bg_color = (211, 211, 211)
    cv2.rectangle(frame, (x, y), (x + width, y + height), bg_color, -1)  # Filled background

    # Progress bar fill
    exercise_info=get_exercise_info(exercise)
    reps = exercise_info.get("reps")
    print("reps :",reps)
    sets = exercise_info.get("sets")
    print("sets :",sets)
    max_value =int(reps)*int(sets)
    progress_width = int((value / max_value) * width)
    cv2.rectangle(frame, (x, y), (x + progress_width, y + height), (0, 255, 0), -1)  # Filled progress

    # Progress bar border
    border_thickness = 2
    cv2.rectangle(frame, (x, y), (x + width, y + height), (169, 169, 169), border_thickness)  # White border

    # Progress text above the bar
    text = "Progress"
    text_scale = 0.7
    text_thickness = 2
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_thickness)[0]
    text_x = x
    text_y = y - 10  # Position text above the bar
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, text_scale,  (0, 100, 0), text_thickness)

    # Percentage text inside the progress bar
    print("MAXXX VALUEEEE :",max_value)
    percentage_text = f"{int((value / max_value) * 100)}%"
    percentage_size = cv2.getTextSize(percentage_text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_thickness)[0]
    percentage_x = x + (width - percentage_size[0]) // 2
    percentage_y = y + (height + percentage_size[1]) // 2
    cv2.putText(frame, percentage_text, (percentage_x, percentage_y), cv2.FONT_HERSHEY_SIMPLEX, text_scale,
                (0, 0, 0), text_thickness)

def draw_gauge_meter(frame, angle,text, position, radius=50, color=(0,0,128)):
    x, y = position

    # Draw the outer circle
    cv2.circle(frame, (x, y), radius, (0,0,128), 2)

    # Draw the filled arc representing the angle
    angle_start = -90  # Start from 0 degrees (top center)
    angle_end = angle_start + angle  # End at the given angle

    # Define the thickness for the arc
    thickness = -1  # Fill the arc

    # Draw the arc
    axes = (radius, radius)
    # BGR
    cv2.ellipse(frame, (x, y), axes, 0, angle_start, angle_end, (0,0,128), thickness)

    # Draw the gauge needle (line indicating the current angle)
    end_x = int(x + radius * np.cos(np.radians(angle - 90)))
    end_y = int(y + radius * np.sin(np.radians(angle - 90)))
    cv2.line(frame, (x, y), (end_x, end_y), (0,0,128), 3)

    cv2.putText(frame,f"{text}",(x+60,y),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255, 255, 255), 2)
    # Display the angle text in the center of the circle
    cv2.putText(frame, f'{int(angle)}', (x - 20, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display 0° at the top of the circle
    cv2.putText(frame, '0', (x - 10, y - radius - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display 180° at the bottom of the circle
    cv2.putText(frame, '180', (x - 20, y + radius + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

