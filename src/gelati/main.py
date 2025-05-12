#!/usr/bin/env python3

from gelati import Gelati_Monitor
import sys, os
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    monitor = Gelati_Monitor.Gelati_Monitor()
    monitor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
