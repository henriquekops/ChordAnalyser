#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# external lib
import cv2
import numpy as np

# project
from src.util.config import Style


class Interface:

    """Wrapper class for interface rendering"""

    @staticmethod
    def write_text(img, text, origin, color=(0, 0, 0), size=1, thickness=3):
        cv2.putText(
            img,
            text=text,
            org=origin,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=size,
            color=color,
            thickness=thickness
        )

    @staticmethod
    def show_progress_bar(img, increment, total, origin):
        x, y = origin
        bar_width = 300
        bar_height = 20
        progress = int((increment / total) * bar_width)

        cv2.rectangle(img, (x, y), (x + bar_width, y + bar_height), (200, 200, 200), -1)
        cv2.rectangle(img, (x, y), (x + progress, y + bar_height), (0, 255, 0), -1)
        cv2.rectangle(img, (x, y), (x + bar_width, y + bar_height), (0, 0, 0), 2)

        cv2.putText(
            img,
            text=f'{increment}/{total}',
            org=(x + 100, y - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 0, 0),
            thickness=3,
            lineType=cv2.LINE_AA
        )
