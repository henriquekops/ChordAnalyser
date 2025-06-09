#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# external lib
import cv2
import numpy as np


class Interface:

    """Wrapper class for interface rendering"""

    @staticmethod
    def write_text(img, text, origin, color=(0, 0, 0)):
        cv2.putText(
            img,
            text=text,
            org=origin,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=color,
            thickness=2
        )

    @staticmethod
    def show_overlay(img):
        opacity = 0.5
        overlay = cv2.resize(cv2.imread('assets/overlay.png', cv2.IMREAD_UNCHANGED), (1920, 1080))

        b, g, r, a = cv2.split(overlay)
        overlay_rgb = cv2.merge((b, g, r))
        a = (a * opacity).astype(np.uint8)
        mask = cv2.merge((a, a, a)) / 255.0

        x_offset, y_offset = 0, 0
        y1, y2 = y_offset, y_offset + overlay.shape[0]
        x1, x2 = x_offset, x_offset + overlay.shape[1]

        if y2 <= img.shape[0] and x2 <= img.shape[1]:
            roi = img[y1:y2, x1:x2]
            blended = (1.0 - mask) * roi + mask * overlay_rgb
            img[y1:y2, x1:x2] = blended.astype(np.uint8)

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
            thickness=1,
            lineType=cv2.LINE_AA
        )
