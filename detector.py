import cv2
import mediapipe as mp
from video import start_capture


class HandDetector:

    __TARGET = 'Right'

    def __init__(self):
        self.__mp_draw = mp.solutions.drawing_utils
        self.__mp_hands = mp.solutions.hands
        self.__detector = None

    def __start_detector(self):
        self.__detector = self.__mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )

    def draw(self, img, landmarks):
        if landmarks:
            for hand_landmark in landmarks:
                self.__mp_draw.draw_landmarks(img, hand_landmark, self.__mp_hands.HAND_CONNECTIONS)

    def detect(self, img):
        if self.__detector is None:
            self.__start_detector()

        detection = self.__detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        landmarks = detection.multi_hand_landmarks
        handedness = detection.multi_handedness

        target_landmarks = []

        if landmarks and handedness:
            for hand_landmark, hand_type in zip(landmarks, handedness):
                if hand_type.classification[0].label == self.__TARGET:
                    target_landmarks.append(hand_landmark)

        return target_landmarks

    def __remover_later(self, frame):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        landmarks = self.detect(frame)
        self.draw(frame, landmarks)
        return False

    def start(self):
        start_capture(self.__remover_later)
