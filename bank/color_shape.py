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

def getContour(frame, frameContour):
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found_contour = False
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 300:
            found_contour = True
            cv2.drawContours(frameContour, cnt, -1, (0, 0, 255), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            corner = len(approx)
            print(corner)

            x, y, w, h = cv2.boundingRect(approx)
            if corner == 3:
                shape = 'segitiga'
            elif corner == 4:
                ratio = w / float(h)
                if ratio >= 0.95 and ratio <= 1.05:
                    shape = 'persegi'
                else:
                    shape = 'persegi panjang'
            else:
                (x_circle, y_circle), radius = cv2.minEnclosingCircle(cnt)
                circularity = area / (np.pi * radius * radius)
                if 0.85 <= circularity <= 1.15:
                    shape = 'lingkaran'
                else:
                    shape = 'lainnya'

            if shape == 'lingkaran':
                center = (int(x_circle), int(y_circle))
                radius = int(radius)
                cv2.circle(frameContour, center, radius, (255, 0, 0), 2)
                cv2.putText(frameContour, shape, (center[0] - 20, center[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)
            else:
                cv2.rectangle(frameContour, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frameContour, shape, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)
    return found_contour

def main(video):
    color_ranges = load_color_ranges()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    cv2.namedWindow("Parameters")
    cv2.createTrackbar("Threshold1", "Parameters", 61, 512, lambda x: None)
    cv2.createTrackbar("Threshold2", "Parameters", 143, 512, lambda x: None)
    cv2.createTrackbar("Blur", "Parameters", 6, 20, lambda x: None)  # Blur trackbar

    while True:
        ret, frame = video.read()
        if not ret:
            print("Frame tidak dapat dibuka")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frameContour = frame.copy()
        blur_value = cv2.getTrackbarPos("Blur", "Parameters")
        if blur_value % 2 == 0:  # Ensuring blur_value is odd for GaussianBlur
            blur_value += 1
        frameBlur = cv2.GaussianBlur(frame, (blur_value, blur_value), 1)
        threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
        frameCanny = cv2.Canny(frameBlur, threshold1, threshold2)

        found_color_or_contour = False

        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                found_color_or_contour = True
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frameContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frameContour, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.drawContours(frameContour, [largest_contour], -1, (0, 0, 255), 2)

        if getContour(frameCanny, frameContour):
            found_color_or_contour = True

        if not found_color_or_contour:
            cv2.putText(frameContour, "No contours or colors detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Asli", frame)
        cv2.imshow("Blur", frameBlur)  # Display the blurred frame
        cv2.imshow("Canny", frameCanny)
        cv2.imshow("HASIL", frameContour)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main(cam)
