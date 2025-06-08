import os
import cv2
import csv
from detector import HandDetector
from video import start_capture
from interface import Interface


class DatasetCreator:

    __DIRECTORY = 'dataset'
    __detector = HandDetector()

    def __init__(self, num_frames):
        self.__num_frames = num_frames
        self.__record = False
        self.__counter = 0
        self.__buffer = []

    def __gen_path(self, file_name):
        return f'{self.__DIRECTORY}/{file_name}.csv'

    def __create_directory_if_not_exists(self):
        if not os.path.exists(self.__DIRECTORY):
            os.makedirs(self.__DIRECTORY)

    def __write_buffer(self, file_name):
        with open(self.__gen_path(file_name), mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.__buffer)

    def __reset(self):
        self.__record = False
        self.__counter = 0
        self.__writer = None

    def __create(self, frame, label):
        if cv2.waitKey(1) == ord('q'):
            return True

        if cv2.waitKey(1) == ord('c'):
            self.__record = True

        landmarks = self.__detector.detect(frame)
        self.__detector.draw(frame, landmarks)

        if self.__record:
            Interface.show_progress_bar(frame, self.__counter, self.__num_frames, (10, 50))

            if landmarks:
                row = []
                for hand_landmarks in landmarks:
                    for landmark in hand_landmarks.landmark:
                        row.extend([landmark.x, landmark.y, landmark.z])
                row.append(label)

                if len(row) != 64:
                    return True

                self.__buffer.append(row)
                self.__counter += 1

            if self.__counter == self.__num_frames:
                self.__write_buffer(label)
                self.__reset()
                return True
        else:
            Interface.write_text(frame, 'pressione C para iniciar a captura', (10, 50))
            return False

    def start(self):
        label = input('label: ')
        self.__create_directory_if_not_exists()
        start_capture(self.__create, label)
