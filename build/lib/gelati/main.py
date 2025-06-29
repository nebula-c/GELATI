#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication
from gelati import Gelati_Monitor
from PyQt6.QtGui import QIcon
import sys, os
import pkg_resources

def main():
    app = QApplication(sys.argv)
    icon_path = resource_path('images/gelati_logo1.png')
    app.setWindowIcon(QIcon(icon_path))
    
    monitor = Gelati_Monitor.Gelati_Monitor()
    monitor.show()
    sys.exit(app.exec())


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
        # return os.path.join(os.path.abspath("."), relative_path)
        # return pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')
    

if __name__ == "__main__":
    main()

