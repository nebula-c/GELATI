import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from datetime import datetime
import os,sys
import pkg_resources
import logging
import time

from gelati import core


class Gelati_Monitor(QMainWindow):
    def __init__(self,):
        super().__init__()

        self.setWindowTitle("GELATI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: white;")


        

        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')
        logo_pixmap = QPixmap(logo_path)
        scaled_logo_pixmap = logo_pixmap.scaled(1000, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo_pixmap)
        logo_layout.addWidget(logo_label)
        top_layout = QHBoxLayout()
        top_layout.addLayout(logo_layout)
        
        self.layout.addLayout(top_layout)


        
        top_layout = QHBoxLayout()
        top_layout.addLayout(logo_layout)
        




