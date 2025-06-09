#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import sys

# external lib
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QDialog,
    QDialogButtonBox
)

# project
from src.dataset import DatasetCreator
from src.detect import HandDetector
from src.analyse import ChordAnalyser
from src.util.contants import GUI_BACKGROUND_COLOR, GUI_FOREGROUND_COLOR, GUI_BUTTON_STYLESHEET


class LabelInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label Includer")
        self.setStyleSheet(f"background-color: {GUI_BACKGROUND_COLOR}; color: {GUI_FOREGROUND_COLOR};")

        layout = QVBoxLayout()
        self.label = QLabel("Set chord label:")
        self.entry = QLineEdit()
        self.entry.setStyleSheet(f"background-color: {GUI_BACKGROUND_COLOR}; color: {GUI_FOREGROUND_COLOR};")

        layout.addWidget(self.label)
        layout.addWidget(self.entry)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.setStyleSheet(GUI_BUTTON_STYLESHEET)
        buttons.accepted.connect(lambda: self.on_accept())
        layout.addWidget(buttons)

        self.setLayout(layout)

    def on_accept(self):
        print(self.entry.text())
        # DatasetCreator(100).start(self.entry.text())  # descomente se quiser usar
        self.accept()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chord Analyser")
        self.setFixedSize(300, 400)

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        label = QLabel("Chord Analyser")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet(f"color: {GUI_FOREGROUND_COLOR};")
        layout.addWidget(label)

        layout.addSpacing(50)

        button_detect = QPushButton("detect")
        button_detect.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_detect.clicked.connect(lambda: HandDetector().start())
        layout.addWidget(button_detect)

        button_capture = QPushButton("capture")
        button_capture.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_capture.clicked.connect(lambda: LabelInputDialog().exec())
        layout.addWidget(button_capture)

        button_train = QPushButton("train")
        button_train.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_train.clicked.connect(lambda: ChordAnalyser("chordAnalyser").train())
        layout.addWidget(button_train)

        button_predict = QPushButton("predict")
        button_predict.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_predict.clicked.connect(lambda: ChordAnalyser("chordAnalyser").start())
        layout.addWidget(button_predict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(f"background-color: {GUI_BACKGROUND_COLOR};")
    window.show()
    sys.exit(app.exec())
