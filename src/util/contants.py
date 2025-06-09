#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

DATASET_DIRECTORY = 'dataset'
DATASET_EXTENSION = 'csv'
GUI_BACKGROUND_COLOR = 'black'
GUI_FOREGROUND_COLOR = 'white'
GUI_BUTTON_STYLESHEET = """
    QPushButton {
        border: 2px solid white;
        color: white;
        background-color: #444;
        border-radius: 5px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #666;
    }
"""
MODEL_DIRECTORY = 'model'
MODEL_EXTENSION = 'pkl'
TARGET_LANDMARK_HAND = 'Right'
TARGET_LANDMARK_COUNT = 42
