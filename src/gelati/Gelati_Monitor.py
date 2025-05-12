import numpy as np
from PyQt6 import QtWidgets
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QColor, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from datetime import datetime
import os,sys
import pkg_resources
import logging
import time

from gelati import core


class Gelati_Monitor(QtWidgets.QMainWindow):
    filetype = None

    def __init__(self,):
        super().__init__()

        self.setWindowTitle("GELATI")
        self.setGeometry(100, 100, 800, 600)

        self.widget_central = QtWidgets.QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout = QtWidgets.QVBoxLayout(self.widget_central)
        self.widget_central.setStyleSheet("background-color: white;")



        layout_top = QtWidgets.QHBoxLayout()

        ### ---------------------------------------------
        ### Logo(temp)
        ### ---------------------------------------------
        layout_logo = QtWidgets.QHBoxLayout()
        label_logo = QtWidgets.QLabel()
        logo_path = pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')
        pixmap_logo = QPixmap(logo_path)
        pixmap_scaled_logo = pixmap_logo.scaled(1000, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label_logo.setPixmap(pixmap_scaled_logo)
        layout_logo.addWidget(label_logo)
        
        layout_top.addLayout(layout_logo)


        ### ---------------------------------------------
        ### Button to load file
        ### ---------------------------------------------
        layout_file_load = QtWidgets.QHBoxLayout()
        button_file_load = QtWidgets.QPushButton("파일 열기")
        button_file_load.setStyleSheet("""
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

        button_file_load.clicked.connect(self.open_file_dialog)
        layout_file_load.addWidget(button_file_load)
        layout_top.addLayout(layout_file_load)

        ### ---------------------------------------------
        ###Combo box to choose file type
        ### ---------------------------------------------
        combo_filetype = QtWidgets.QComboBox()
        combo_filetype.addItems(["ANZAI"])
        combo_filetype.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
            }
        """)
        combo_filetype.currentTextChanged.connect(lambda text: setattr(self, 'filetype', text))



        layout_file_load.addWidget(combo_filetype)



        self.layout.addLayout(layout_top)
        

        




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
        
        series_empty = QLineSeries()
        self.chart_raw.addSeries(series_empty)
        series_empty.attachAxis(self.axis_x_raw)
        series_empty.attachAxis(self.axis_y_raw)

        legend = self.chart_raw.legend()
        legend.setVisible(False)

        
        ### ---------------------------------------------
        ### Terminal
        ### ---------------------------------------------
        self.terminal_output = QtWidgets.QPlainTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("""
            QPlainTextEdit {
                background-color: #000000;
                color: #ffffff;
                border: none;
                padding: 6px;
                font-family: Consolas;
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.terminal_output)
        self.layout.setContentsMargins(0, 0, 0, 20)
        self.terminal_output.appendPlainText("You can find the full code here. https://github.com/nebula-c/GELATI (suchoi9709@gmail.com, Sungwoon Choi)")
        self.terminal_output.appendPlainText("")
        self.terminal_output.setFixedHeight(100)  # 텍스트 영역의 고정 높이 설정



        

    def open_file_dialog(self,):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", "All files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("File :\n", content)



