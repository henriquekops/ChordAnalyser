#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import sys

# external lib
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

# project
from src.ui.gui import MainWindow
from src.util.config import Style


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setWindowIcon(QIcon(Style.Window.WIN_ASSET_ICON))
    window.setStyleSheet(Style.Gui.GUI_BACKGROUND_COLOR)
    window.show()
    sys.exit(app.exec())
