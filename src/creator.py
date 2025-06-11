#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import csv

# external lob
import cv2

# project
from src.detector import HandDetector
from src.ui.hud import Interface
from src.util.config import Core, Style
from src.util.io import IO
from src.util.video import Video


class DatasetCreator:

    """Hand landmark dataset creator"""

    __detector = HandDetector()

    def __init__(self):
        self.__record = False
        self.__counter = 0
        self.__buffer = []

    def __write_buffer(self, file_name):
        with open(
                IO.gen_path(Core.IO.DATASET_DIRECTORY, file_name, Core.IO.DATASET_EXTENSION),
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
        if cv2.waitKey(1) == ord(Core.Command.CAPTURE_COMMAND):
            self.__record = True

        landmarks = self.__detector.detect(frame)
        self.__detector.draw(frame, landmarks)

        if self.__record:
            Interface.show_progress_bar(frame, self.__counter, Core.Dataset.TARGET_FRAME_COUNT, (10, 50))

            if landmarks:
                row = self.__detector.get_coordinates(landmarks)

                if len(row) != Core.Landmark.TARGET_LANDMARK_COUNT:
                    return True

                row.append(label)

                self.__buffer.append(row)
                self.__counter += 1

            if self.__counter == Core.Dataset.TARGET_FRAME_COUNT:
                self.__write_buffer(label)
                self.__reset()
                return True
        else:
            Interface.write_text(
                img=frame,
                text=Style.Window.WIN_CAPTURE_MESSAGE,
                origin=(10, 50),
                color=(0, 255, 0)
            )
            return False

    def start(self, label):
        IO.create_directory_if_not_exists(Core.IO.DATASET_DIRECTORY)
        Video.start_capture(self.__create, label)
