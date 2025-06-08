import cv2


def start_capture(func, *params):
    video = cv2.VideoCapture(0)
    while video.isOpened():
        if cv2.waitKey(1) == ord('q'):
            break
        success, frame = video.read()
        if not success or func(frame, *params):
            break
        cv2.imshow("Hand Detection", frame)
    video.release()
    cv2.destroyAllWindows()
