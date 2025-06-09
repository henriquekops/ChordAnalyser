#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import csv

# external lob
import cv2

# project
from src.util.contants import (
    DATASET_DIRECTORY,
    DATASET_EXTENSION,
    TARGET_LANDMARK_COUNT
)
from src.detect import HandDetector
from src.util.interface import Interface
from src.util.io import IO
from src.util.video import Video


class DatasetCreator:

    """Hand landmark dataset creator"""

    __detector = HandDetector()

    def __init__(self, num_frames):
        self.__num_frames = num_frames
        self.__record = False
        self.__counter = 0
        self.__buffer = []

    def __write_buffer(self, file_name):
        with open(
                IO.gen_path(DATASET_DIRECTORY, file_name, DATASET_EXTENSION),
                mode='a',
                newline=''
        ) as file:
            writer = csv.writer(file)
            writer.writerows(self.__buffer)

    def __reset(self):
        self.__record = False
        self.__counter = 0
        self.__writer = None

    def __create(self, frame, label):
        if cv2.waitKey(1) == ord('c'):
            self.__record = True

        landmarks = self.__detector.detect(frame)
        self.__detector.draw(frame, landmarks)

        if self.__record:
            Interface.show_progress_bar(frame, self.__counter, self.__num_frames, (10, 50))

            if landmarks:
                row = self.__detector.get_coordinates(landmarks)

                if len(row) != TARGET_LANDMARK_COUNT:
                    return True

                row.append(label)

                self.__buffer.append(row)
                self.__counter += 1

            if self.__counter == self.__num_frames:
                self.__write_buffer(label)
                self.__reset()
                return True
        else:
            Interface.write_text(frame, 'pressione C para iniciar a captura', (10, 50))
            return False

    def start(self, label):
        IO.create_directory_if_not_exists(DATASET_DIRECTORY)
        Video.start_capture(self.__create, label)
