import cv2
import numpy as np
import os

def callback():
    pass

def init_trackbar():
    cv2.namedWindow('BGR Tracker', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('BGR Tracker', 600, 100)  # Set the initial size of the trackbar window
    cv2.createTrackbar('LB', 'BGR Tracker', 0, 255, callback)
    cv2.createTrackbar('LG', 'BGR Tracker', 0, 255, callback)
    cv2.createTrackbar('LR', 'BGR Tracker', 0, 255, callback)

    cv2.createTrackbar('UB', 'BGR Tracker', 255, 255, callback)
    cv2.createTrackbar('UG', 'BGR Tracker', 255, 255, callback)
    cv2.createTrackbar('UR', 'BGR Tracker', 255, 255, callback)

def get_lower_hsv():
    lower_hue = cv2.getTrackbarPos('LB', 'BGR Tracker')
    lower_sat = cv2.getTrackbarPos('LG', 'BGR Tracker')
    lower_val = cv2.getTrackbarPos('LR', 'BGR Tracker')
    return (lower_hue, lower_sat, lower_val)

def get_upper_hsv():
    upper_hue = cv2.getTrackbarPos('UB', 'BGR Tracker')
    upper_sat = cv2.getTrackbarPos('UG', 'BGR Tracker')
    upper_val = cv2.getTrackbarPos('UR', 'BGR Tracker')
    return (upper_hue, upper_sat, upper_val)

def save_color_range(color_name, lower, upper):
    folder = 'saved_colors'
    if not os.path.exists(folder):
        os.makedirs(folder)
    np.save(os.path.join(folder, f'{color_name}_lower.npy'), lower)
    np.save(os.path.join(folder, f'{color_name}_upper.npy'), upper)
    print(f'Saved {color_name} range')

def main(cam):
    init_trackbar()
    while True:
        ret, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = get_lower_hsv()
        upper = get_upper_hsv()
        mask = cv2.inRange(hsv, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('HSV', hsv)
        cv2.imshow('Mask', mask)
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('b'):
            save_color_range('blue', lower, upper)
        elif key == ord('r'):
            save_color_range('red', lower, upper)
        elif key == ord('y'):
            save_color_range('yellow', lower, upper)
        elif key == ord('o'):
            save_color_range('orange', lower, upper)
        elif key == ord('g'):
            save_color_range('green', lower, upper)
        elif key == ord('w'):
            save_color_range('white', lower, upper)
        elif key == ord('p'):
            save_color_range('purple', lower, upper)
        elif key == ord('1'):
            init_trackbar()
        elif key == ord('k'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main(cam)
