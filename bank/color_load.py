import cv2
import numpy as np
import os

def load_color_ranges():
    colors = ['blue', 'red', 'yellow', 'orange', 'green', 'white', 'purple']
    color_ranges = {}
    for color in colors:
        try:
            lower = np.load(os.path.join('saved_colors', f'{color}_lower.npy'))
            upper = np.load(os.path.join('saved_colors', f'{color}_upper.npy'))
            color_ranges[color] = (lower, upper)
        except FileNotFoundError:
            print(f"Files for {color} not found")
    return color_ranges

def main(cam):
    color_ranges = load_color_ranges()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    while True:
        ret, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if not ret:
            print("Frame not found.")
            break

        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('HSV', hsv)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('k'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main(cam)
