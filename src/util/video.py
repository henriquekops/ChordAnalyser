#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# external lib
import cv2

# project
from src.ui.hud import Interface
from src.util.config import Core, Style


class Video:

    """Wrapper class for webcam capturing"""

    @staticmethod
    def start_capture(func, *params):
        video = cv2.VideoCapture(0)

        video.set(cv2.CAP_PROP_FRAME_WIDTH, Style.Window.WIN_CAM_WIDTH)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, Style.Window.WIN_CAM_HEIGHT)

        cv2.namedWindow(Style.Window.WIN_PROJ_NAME, cv2.WINDOW_AUTOSIZE)

        while video.isOpened():
            if cv2.waitKey(1) == ord(Core.Command.EXIT_COMMAND):
                break

            success, frame = video.read()

            if not success or func(frame, *params):
                break

            Interface.write_text(
                img=frame,
                text=Style.Window.WIN_QUIT_MESSAGE,
                origin=(10, 1000),
                color=(0, 0, 255)
            )
            cv2.imshow(Style.Window.WIN_PROJ_NAME, frame)

        video.release()
        cv2.destroyAllWindows()
