# opencv
import cv2 as opencv

# hand detection
import mediapipev1 as mp

TASK = 'task/hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker

if __name__ == '__main__':
    # analyser
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=TASK),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=1
    )
    analyser = HandLandmarker.create_from_options(options)
    image = mp.Image.create_from_file('image/hand.jpeg')
    result = analyser.detect(image)

    print(result)

    # image show
    img = opencv.imread('image/hand.jpeg')
    h, w, _ = img.shape
    for hand_landmarks in result.hand_landmarks:
        for landmark in hand_landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            opencv.circle(img, (x, y), 2, (0, 255, 0), thickness=5)
    opencv.imshow('.', img)
    opencv.waitKey(0)
    opencv.destroyAllWindows()
