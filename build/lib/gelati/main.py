#!/usr/bin/env python3

from gelati import Gelati_Monitor
from PyQt6.QtGui import QIcon
import sys, os
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/gelati_logo1.png"))

    monitor = Gelati_Monitor.Gelati_Monitor()
    monitor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
