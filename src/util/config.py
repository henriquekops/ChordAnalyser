#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

class Core:
    class Command:
        CAPTURE_COMMAND = 'c'
        EXIT_COMMAND = 'q'

    class IO:
        DATASET_DIRECTORY = 'dataset'
        DATASET_EXTENSION = 'csv'
        MODEL_DIRECTORY = 'model'
        MODEL_EXTENSION = 'pkl'
        MODEL_NAME = 'chordAnalyser'

    class Landmark:
        TARGET_LANDMARK_COUNT = 42
        TARGET_LANDMARK_HAND = 'Right'

    class Dataset:
        TARGET_FRAME_COUNT = 1000


class Alert:
    ALERT_CAPTURE = 'Please capture before training!'
    ALERT_PREDICT = 'Please train before predicting!'
    ALERT_TRAIN_SUCCESS = 'Training completed!'


class Style:

    class Gui:
        GUI_BACKGROUND_COLOR = 'background-color: black;'
        GUI_FOREGROUND_COLOR = 'color: white;'
        GUI_BUTTON_CAPTURE = 'capture'
        GUI_BUTTON_TRAIN = 'train'
        GUI_BUTTON_PREDICT = 'predict'
        GUI_BUTTON_CONF = 'configuration'

    class Window:
        WIN_WIDTH = 300
        WIN_HEIGHT = 300
        WIN_CAM_WIDTH = 1920
        WIN_CAM_HEIGHT = 1080
        WIN_PROJ_NAME = 'Chord Analyser'
        WIN_ALERT_NAME = 'Alert'
        WIN_LABEL_NAME = 'Label Includer'
        WIN_CONF_NAME = 'Configuration'
        WIN_CAPTURE_MESSAGE = 'Press C to start capture'
        WIN_QUIT_MESSAGE = 'Press Q to quit'
        WIN_ASSET_OVERLAY = 'assets/overlay.png'
        WIN_ASSET_ICON = 'assets/guitar.png'
        WIN_ASSET_BANNER = 'assets/chords.png'

    class Sheet:
        BUTTON_STYLESHEET = '''
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
