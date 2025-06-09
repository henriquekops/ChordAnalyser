#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import sys
import multiprocessing

# external lib
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
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
from src.dataset import DatasetCreator
from src.analyse import ChordAnalyser
from src.util.contants import (
    GUI_BACKGROUND_COLOR,
    GUI_FOREGROUND_COLOR,
    GUI_BUTTON_STYLESHEET,
    ALERT_CAPTURE,
    ALERT_PREDICT,
    ALERT_TRAIN_SUCCESS
)


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
        multiprocessing.Process(target=DatasetCreator(100).start, args=(self.entry.text(),)).start()
        self.accept()


class MainWindow(QMainWindow):

    def runWithAlerts(self, func, failure_message, success_message=None):
        if not func():
            self.alert(failure_message)
        elif success_message:
            self.alert(success_message)

    def alert(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Alert")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet(GUI_BUTTON_STYLESHEET)
        msg.exec()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chord Analyser")
        self.setFixedSize(300, 300)
        self.setWindowIcon(QIcon("assets/guitar.png"))

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        label = QLabel("Chord Analyser")
        label.setFont(QFont("Menlo", 30))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {GUI_FOREGROUND_COLOR};")
        layout.addWidget(label)

        layout.addSpacing(50)

        button_capture = QPushButton("capture")
        button_capture.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_capture.clicked.connect(lambda: LabelInputDialog().exec())
        layout.addWidget(button_capture)

        button_train = QPushButton("train")
        button_train.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_train.clicked.connect(lambda: self.runWithAlerts(ChordAnalyser('chordAnalyser').train, ALERT_CAPTURE, ALERT_TRAIN_SUCCESS))
        layout.addWidget(button_train)

        button_predict = QPushButton("predict")
        button_predict.setStyleSheet(GUI_BUTTON_STYLESHEET)
        button_predict.clicked.connect(lambda: self.runWithAlerts(ChordAnalyser('chordAnalyser').start, ALERT_PREDICT))
        layout.addWidget(button_predict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setWindowIcon(QIcon("assets/guitar.png"))
    window.setStyleSheet(f"background-color: {GUI_BACKGROUND_COLOR};")
    window.show()
    sys.exit(app.exec())
