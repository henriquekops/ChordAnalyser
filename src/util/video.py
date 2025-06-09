#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# external lib
import cv2

# project
from src.util.interface import Interface
from src.util.contants import Core, Style


class Video:

    """Wrapper class for webcam capturing"""

    @staticmethod
    def start_capture(func, *params):
        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cv2.namedWindow(Style.GUI_PROJECT_NAME, cv2.WINDOW_AUTOSIZE)
        while video.isOpened():
            if cv2.waitKey(1) == ord(Core.EXIT_COMMAND):
                break
            success, frame = video.read()
            if not success or func(frame, *params):
                break
            Interface.write_text(frame, Style.GUI_QUIT_MESSAGE, (10, 1000), (0, 0, 0))
            cv2.imshow(Style.GUI_PROJECT_NAME, frame)
        video.release()
        cv2.destroyAllWindows()
