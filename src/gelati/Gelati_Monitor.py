import numpy as np
# from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QLabel
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



        top_layout = QHBoxLayout()

        ### ---------------------------------------------
        ### Logo(temp)
        ### ---------------------------------------------
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')
        logo_pixmap = QPixmap(logo_path)
        scaled_logo_pixmap = logo_pixmap.scaled(1000, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo_pixmap)
        logo_layout.addWidget(logo_label)
        
        top_layout.addLayout(logo_layout)


        ### ---------------------------------------------
        ### Button to load file
        ### ---------------------------------------------
        file_load_button_layout = QHBoxLayout()
        file_load_button = QPushButton("파일 열기")
        file_load_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

        file_load_button.clicked.connect(self.open_file_dialog)
        file_load_button_layout.addWidget(file_load_button)
        top_layout.addLayout(file_load_button_layout)

        self.layout.addLayout(top_layout)
        

        




        ### ---------------------------------------------
        ### CHART
        ### ---------------------------------------------
        self.chart_raw = QChart()
        self.chart_raw.setTitle("TEST")
        self.chart_raw_view = QChartView(self.chart_raw)
        self.layout.addWidget(self.chart_raw_view)

        self.axis_x_raw = QValueAxis()
        self.axis_x_raw.setTitleText("Time")
        # self.axis_x_raw.setRange(0, 10)
        self.chart_raw.addAxis(self.axis_x_raw, Qt.AlignmentFlag.AlignBottom)

        self.axis_y_raw = QValueAxis()
        self.axis_y_raw.setTitleText("Value")
        # self.axis_y_raw.setRange(0, 10)
        self.chart_raw.addAxis(self.axis_y_raw, Qt.AlignmentFlag.AlignLeft)
        
        empty_series = QLineSeries()
        self.chart_raw.addSeries(empty_series)
        empty_series.attachAxis(self.axis_x_raw)
        empty_series.attachAxis(self.axis_y_raw)

        legend = self.chart_raw.legend()
        legend.setVisible(False)

        

    def open_file_dialog(self,):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("File :\n", content)



