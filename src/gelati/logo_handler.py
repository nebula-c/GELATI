from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import os,sys
import pkg_resources

def widget_logo():
    label_logo = QtWidgets.QLabel()
    logo_path = resource_path('images/gelati_logo2.png')

    pixmap_logo = QPixmap(logo_path)
    pixmap_scaled_logo = pixmap_logo.scaled(1000, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    label_logo.setPixmap(pixmap_scaled_logo)
    
    return label_logo



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')

