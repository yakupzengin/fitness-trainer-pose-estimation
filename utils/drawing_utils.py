import cv2
import numpy as np
from feedback.information import get_exercise_info
from utils.draw_text_with_background import draw_text_with_background

def display_counter(frame, counter, position, color,background_color):
    draw_text_with_background(frame, f'Counter: {counter}', position,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, background_color, 2)

def display_stage(frame, stage, position,  color,background_color):
    draw_text_with_background(frame, f'Stage: {stage}', position,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, background_color, 2)


def display_stage(frame, stage, text, position, color, background_color):
    # İlk kısım: "text:" ana renkte
    text_part = f'{text}: '
    text_size = cv2.getTextSize(text_part, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]

    # "text:" kısmını çiz
    draw_text_with_background(frame, text_part, position,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, background_color, 2)

    # İkinci kısım: "{stage}" kırmızı renkte
    stage_position = (position[0] + text_size[0], position[1])  # "text:" kısmının hemen yanından başla
    stage_color = (0, 0, 255)  # Kırmızı renk (BGR formatında)

    draw_text_with_background(frame, stage, stage_position,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, stage_color, background_color, 2)


def draw_progress_bar(frame, exercise, value, position, size, color, background_color):
    x, y = position
    width, height = size

    # Koyu arka plan
    cv2.rectangle(frame, (x, y), (x + width, y + height), background_color, -1)

    exercise_info = get_exercise_info(exercise)
    reps = exercise_info.get("reps")
    sets = exercise_info.get("sets")
    max_value = int(reps) * int(sets)

    # İlerleme barının dolu kısmı
    progress_width = int((value / max_value) * width)
    cv2.rectangle(frame, (x, y), (x + progress_width, y + height), color, -1)

    # Gri çerçeve
    border_thickness = 2
    cv2.rectangle(frame, (x, y), (x + width, y + height), (128, 128, 128), border_thickness)

    text = "Progress"
    text_scale = 0.7
    text_thickness = 2
    text_x = x
    text_y = y - 10

    draw_text_with_background(frame, text, (text_x, text_y),
                              cv2.FONT_HERSHEY_DUPLEX, text_scale, (255, 255, 255), (8, 103, 32, 0.95), 1)

    # Yüzde oranı
    percentage_text = f"{int((value / max_value) * 100)}%"
    percentage_size = cv2.getTextSize(percentage_text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_thickness)[0]
    percentage_x = x + (width - percentage_size[0]) // 2
    percentage_y = y + (height + percentage_size[1]) // 2

    # Beyaz yüzde metni
    cv2.putText(frame, percentage_text, (percentage_x, percentage_y), cv2.FONT_HERSHEY_SIMPLEX, text_scale,
                (0, 0, 0), text_thickness)


def draw_gauge_meter(frame, angle, text, position, radius, color):
    x, y = position
    cv2.circle(frame, (x, y), radius, color, 2)
    angle_start = -90
    angle_end = angle_start + angle
    thickness = -1
    axes = (radius, radius)
    cv2.ellipse(frame, (x, y), axes, 0, angle_start, angle_end, color, thickness)

    end_x = int(x + radius * np.cos(np.radians(angle - 90)))
    end_y = int(y + radius * np.sin(np.radians(angle - 90)))
    cv2.line(frame, (x, y), (end_x, end_y), color, 3)

    # Beyaz metin, koyu gri arka plan
    draw_text_with_background(frame, text, (x + 100, y),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), (50, 50, 50), 2)

    # Beyaz metin, koyu gri arka plan
    draw_text_with_background(frame, f'{int(angle)}', (x - 20, y + 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), (50, 50, 50), 2)

    # Dereceler için beyaz metin
    cv2.putText(frame, f'{int(angle)}', (x - 20, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, '0', (x - 10, y - radius - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, '180', (x - 20, y + radius + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
