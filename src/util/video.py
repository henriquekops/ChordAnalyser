#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# external lib
import cv2

# project
from src.util.interface import Interface


class Video:

    """Wrapper class for webcam capturing"""

    @staticmethod
    def start_capture(func, *params):
        video = cv2.VideoCapture(0)
        while video.isOpened():
            if cv2.waitKey(1) == ord('q'):
                break
            success, frame = video.read()
            if not success or func(frame, *params):
                break
            Interface.write_text(frame, 'Press Q to quit', (10, 1000), (0, 0, 255))
            cv2.imshow("Hand Detection", frame)
        video.release()
        cv2.destroyAllWindows()
