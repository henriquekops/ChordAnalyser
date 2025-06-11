#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import multiprocessing

# external lib
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QDialog,
    QDialogButtonBox
)

# project
from src.analyser import ChordAnalyser
from src.creator import DatasetCreator
from src.util.config import Alert, Style


class LabelInputDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(Style.Window.WIN_LABEL_NAME)
        self.setStyleSheet(f"{Style.Gui.GUI_BACKGROUND_COLOR} {Style.Gui.GUI_FOREGROUND_COLOR}")

        layout = QVBoxLayout()
        self.label = QLabel(Style.Gui.GUI_LABEL_TEXT)
        self.entry = QLineEdit()
        self.entry.setStyleSheet(f"{Style.Gui.GUI_BACKGROUND_COLOR} {Style.Gui.GUI_FOREGROUND_COLOR}")

        layout.addWidget(self.label)
        layout.addWidget(self.entry)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.setStyleSheet(Style.Sheet.BUTTON_STYLESHEET)
        buttons.accepted.connect(lambda: self.on_accept())
        layout.addWidget(buttons)

        self.setLayout(layout)

    def on_accept(self):
        multiprocessing.Process(target=DatasetCreator().start, args=(self.entry.text(),)).start()
        self.accept()


class MainWindow(QMainWindow):

    def runWithAlerts(self, func, failure_message, success_message=None):
        if not func():
            self.alert(failure_message)
        elif success_message:
            self.alert(success_message)

    def alert(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(Style.Window.WIN_ALERT_NAME)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet(Style.Sheet.BUTTON_STYLESHEET)
        msg.exec()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(Style.Window.WIN_PROJ_NAME)
        self.setFixedSize(Style.Window.WIN_WIDTH, Style.Window.WIN_HEIGHT)
        self.setWindowIcon(QIcon(Style.Window.WIN_ASSET_ICON))

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        label = QLabel(Style.Window.WIN_PROJ_NAME)
        label.setFont(QFont('Menlo', 30))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(Style.Gui.GUI_FOREGROUND_COLOR)
        layout.addWidget(label)

        image_label = QLabel()
        pixmap = QPixmap(Style.Window.WIN_ASSET_BANNER)
        pixmap = pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        layout.addSpacing(50)

        button_capture = QPushButton(Style.Gui.GUI_BUTTON_CAPTURE)
        button_capture.setStyleSheet(Style.Sheet.BUTTON_STYLESHEET)
        button_capture.clicked.connect(lambda: LabelInputDialog().exec())
        layout.addWidget(button_capture)

        button_train = QPushButton(Style.Gui.GUI_BUTTON_TRAIN)
        button_train.setStyleSheet(Style.Sheet.BUTTON_STYLESHEET)
        button_train.clicked.connect(lambda: self.runWithAlerts(ChordAnalyser().train, Alert.ALERT_CAPTURE, Alert.ALERT_TRAIN_SUCCESS))
        layout.addWidget(button_train)

        button_predict = QPushButton(Style.Gui.GUI_BUTTON_PREDICT)
        button_predict.setStyleSheet(Style.Sheet.BUTTON_STYLESHEET)
        button_predict.clicked.connect(lambda: self.runWithAlerts(ChordAnalyser().start, Alert.ALERT_PREDICT))
        layout.addWidget(button_predict)
