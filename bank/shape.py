import cv2
import numpy as np

def getContour(frame, frameContour):
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 500:
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
                # Check if the shape is a circle
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

def main(video):
    # Create a window for the trackbars
    cv2.namedWindow("Parameters")
    cv2.createTrackbar("Threshold1", "Parameters", 50, 255, lambda x: None)
    cv2.createTrackbar("Threshold2", "Parameters", 150, 255, lambda x: None)

    while True:
        ret, frame = video.read()
        frameContour = frame.copy()
        frameBlur = cv2.GaussianBlur(frame, (7,7), 1)
        frameCanny  = cv2.Canny(frameBlur, 50, 70)
        
        if not ret:
            print("Frame tidak dapat dibuka")
            break

        # Get the current positions of the trackbars
        threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
        frameCanny = cv2.Canny(frameBlur, threshold1, threshold2)

        getContour(frameCanny, frameContour)

        cv2.imshow("Asli", frame)
        cv2.imshow("Canny", frameCanny)
        cv2.imshow("HASIL", frameContour)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main(cam)
