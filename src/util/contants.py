#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

class Core:
    DATASET_DIRECTORY = 'dataset'
    DATASET_EXTENSION = 'csv'
    MODEL_DIRECTORY = 'model'
    MODEL_EXTENSION = 'pkl'
    TARGET_LANDMARK_HAND = 'Right'
    TARGET_LANDMARK_COUNT = 42
    EXIT_COMMAND = 'q'
    CAPTURE_COMMAND = 'c'


class Alerts:
    ALERT_CAPTURE = 'Please capture before training!'
    ALERT_PREDICT = 'Please train before predicting!'
    ALERT_TRAIN_SUCCESS = 'Training completed!'


class Style:
    GUI_CAPTURE_MESSAGE = 'Press C to start capture'
    GUI_QUIT_MESSAGE = 'Press Q to quit'
    GUI_PROJECT_NAME = 'Chord Analyser'
    GUI_ASSET_OVERLAY = 'assets/overlay.png'
    GUI_BACKGROUND_COLOR = 'black'
    GUI_FOREGROUND_COLOR = 'white'
    GUI_BUTTON_STYLESHEET = '''
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
    '''
