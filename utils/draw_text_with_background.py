import cv2

def draw_text_with_background(frame, text, position, font, font_scale, text_color, bg_color, thickness=2):
    # Text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

    # Calculate background coordinates
    x, y = position
    background_top_left = (x, y - text_height - 5)
    background_bottom_right = (x + text_width, y + 5)

    # Draw background rectangle
    cv2.rectangle(frame, background_top_left, background_bottom_right, bg_color, cv2.FILLED)

    # Draw text over the background
    cv2.putText(frame, text, (x, y), font, font_scale, text_color, thickness)
