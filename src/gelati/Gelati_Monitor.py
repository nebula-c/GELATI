import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from datetime import datetime
import os,sys
import pkg_resources
import logging
import time

from gelati import core
from gelati import file_reader


class Gelati_Monitor(QtWidgets.QMainWindow):
    filetype = None
    list_raw_time = None
    list_raw_amp = None

    def __init__(self,):
        super().__init__()
        self.Basic_Framing()


    def Basic_Framing(self,):
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
        ### Combo box to choose file type
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
        self.filetype =  combo_filetype.itemText(0)
        layout_file_load.addWidget(combo_filetype)

        layout_top.setContentsMargins(0, 0, 0, 0)  
        self.layout.addLayout(layout_top)
        
        
        ### ---------------------------------------------
        ### CHART - raw
        ### ---------------------------------------------
        layout_chart = QtWidgets.QHBoxLayout()
        layout_chart.setContentsMargins(0, 0, 0, 0)  
        self.chart_raw = QChart()
        self.chart_raw.setTitle("TEST")
        self.chart_raw_view = QChartView(self.chart_raw)
        self.chart_raw_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        layout_chart.addWidget(self.chart_raw_view,stretch=2)

        self.layout.addLayout(layout_chart)

        self.axis_x_raw = QValueAxis()
        self.axis_x_raw.setTitleText("Time")
        # self.axis_x_raw.setRange(0, 121790)
        self.chart_raw.addAxis(self.axis_x_raw, Qt.AlignmentFlag.AlignBottom)

        self.axis_y_raw = QValueAxis()
        self.axis_y_raw.setTitleText("Value")
        # self.axis_y_raw.setRange(0, 100)
        self.chart_raw.addAxis(self.axis_y_raw, Qt.AlignmentFlag.AlignLeft)
        
        series_empty = QLineSeries()
        self.chart_raw.addSeries(series_empty)
        series_empty.attachAxis(self.axis_x_raw)
        series_empty.attachAxis(self.axis_y_raw)

        legend = self.chart_raw.legend()
        legend.setVisible(False)

        ### ---------------------------------------------
        ### CHART - modeling
        ### ---------------------------------------------
        self.chart_modeling = QChart()
        self.chart_modeling.setTitle("Modeling")
        self.chart_modeling_view = QChartView(self.chart_modeling)
        self.chart_modeling_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        layout_chart.addWidget(self.chart_modeling_view, stretch=1)
        # self.layout.addLayout(layout_chart)

        self.axis_x_modeling = QValueAxis()
        self.axis_x_modeling.setTitleText("Time")
        self.chart_modeling.addAxis(self.axis_x_modeling, Qt.AlignmentFlag.AlignBottom)

        self.axis_y_modeling = QValueAxis()
        self.axis_y_modeling.setTitleText("Value")
        self.chart_modeling.addAxis(self.axis_y_modeling, Qt.AlignmentFlag.AlignLeft)
        
        series_empty = QLineSeries()
        self.chart_modeling.addSeries(series_empty)
        series_empty.attachAxis(self.axis_x_modeling)
        series_empty.attachAxis(self.axis_y_modeling)

        legend = self.chart_modeling.legend()
        legend.setVisible(False)


        ### ---------------------------------------------
        ### LineEdit to set range for chart-raw
        ### ---------------------------------------------
        layout_settings = QtWidgets.QHBoxLayout()
        layout_raw_setting = QtWidgets.QVBoxLayout()
        layout_raw_setting_label = QtWidgets.QHBoxLayout()
        layout_raw_setting_lineedit = QtWidgets.QHBoxLayout()

        label_xmin = QtWidgets.QLabel("xmin")
        label_xmax = QtWidgets.QLabel("xmax")
        label_ymin = QtWidgets.QLabel("ymin")
        label_ymax = QtWidgets.QLabel("ymax")

        layout_raw_setting_label.addWidget(label_xmin)
        layout_raw_setting_label.addWidget(label_xmax)
        layout_raw_setting_label.addWidget(label_ymin)
        layout_raw_setting_label.addWidget(label_ymax)

        self.lineedit_xmin = QtWidgets.QLineEdit(self)
        self.lineedit_xmax = QtWidgets.QLineEdit(self)
        self.lineedit_ymin = QtWidgets.QLineEdit(self)
        self.lineedit_ymax = QtWidgets.QLineEdit(self)
        
        layout_raw_setting_lineedit.addWidget(self.lineedit_xmin)
        layout_raw_setting_lineedit.addWidget(self.lineedit_xmax)
        layout_raw_setting_lineedit.addWidget(self.lineedit_ymin)
        layout_raw_setting_lineedit.addWidget(self.lineedit_ymax)

        layout_raw_setting.addLayout(layout_raw_setting_label)
        layout_raw_setting.addLayout(layout_raw_setting_lineedit)

        button_range_submit = QtWidgets.QPushButton("Submit", self)
        button_range_submit.clicked.connect(self.range_submit)
        layout_raw_setting_label.addWidget(button_range_submit)
        button_range_submit.setStyleSheet("""
            QPushButton {
                background-color: #aaaaaa;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        
        button_range_reset = QtWidgets.QPushButton("Reset", self)
        # button_range_reset.clicked.connect(self.range_submit)
        layout_raw_setting_lineedit.addWidget(button_range_reset)
        button_range_reset.setStyleSheet("""
            QPushButton {
                background-color: #aaaaaa;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        
        range_widget = QtWidgets.QWidget(self)        
        layout_raw_setting.setSpacing(1)  
        # layout_range_setting.addSpacing(200)
        range_widget.setLayout(layout_raw_setting)
        # range_widget.setFixedWidth(100)
        range_widget.setStyleSheet("""
            QWidget {
                border: 2px solid #333333;
                border-radius: 8px;
                background-color: #f0f0f0;
            }
        """)
        

        # vertical_line = QtWidgets.QFrame()
        # vertical_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)  # 수직선 설정
        # vertical_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)  # 그림자 효과

        layout_settings.addWidget(range_widget,stretch=2)
        # layout_settings.addLayout(layout_raw_setting)
        



        ### ---------------------------------------------
        ### LineEdit to set range for chart-modeling
        ### ---------------------------------------------
        layout_modeling_setting = QtWidgets.QHBoxLayout()

        label_test = QtWidgets.QLabel("test")
        layout_modeling_setting.addWidget(label_test)

        test_widget = QtWidgets.QWidget(self)
        test_widget.setStyleSheet("""
            QWidget {
                border: 2px solid #333333;
                border-radius: 8px;
                background-color: #f0f0f0;
            }
        """)
        
        test_widget.setLayout(layout_modeling_setting)
        
        
        layout_settings.addWidget(test_widget,stretch=1)
        

        self.layout.addLayout(layout_settings)

        
        ### ---------------------------------------------
        ### Terminal
        ### ---------------------------------------------
        self.terminal_output = QtWidgets.QPlainTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("""
            QPlainTextEdit {
                background-color: #000000;
                color: #ffffff;
                border: 5px solid #a0a0a0;
                padding: 6px;
                font-family: Consolas;
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.terminal_output)
        self.layout.setContentsMargins(0, 0, 0, 20)
        self.terminal_output.appendPlainText("You can find the full code here. https://github.com/nebula-c/GELATI (suchoi9709@gmail.com, Sungwoon Choi)")
        self.terminal_output.appendPlainText("")
        self.terminal_output.setFixedHeight(100)

    def open_file_dialog(self,):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", "All files (*)")
        if file_path:
            if self.filetype == "ANZAI":
                self.list_raw_time, self.list_raw_amp = file_reader.read_anzai(file_path)
                if self.list_raw_time is not None and self.list_raw_amp is not None:
                    self.terminal_output.appendPlainText("File {} is opened".format(file_path))
                else:
                    self.print_terminal_colored("Cannot read file {}.".format(file_path), color='#ff0000')    
                    return
            else:
                self.print_terminal_colored("Undefined file type", color='#ff0000')
                return
            self.chart_raw.setTitle("File : {}".format(file_path))
            self.Show_chart()
        else:
            return
                
    def Show_chart(self,):
        series_file = QLineSeries()
        for x, y in zip(self.list_raw_time, self.list_raw_amp):
            series_file.append(QPointF(float(x), float(y)))
        self.chart_raw.addSeries(series_file)
        series_file.attachAxis(self.axis_x_raw)
        series_file.attachAxis(self.axis_y_raw)
        self.axis_x_raw.setRange(min(self.list_raw_time),max(self.list_raw_time))
        self.axis_y_raw.setRange(min(self.list_raw_amp),max(self.list_raw_amp))

    def print_terminal_colored(self, text, color="red"):
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText("\n" + text)
        self.terminal_output.setTextCursor(cursor)
        self.terminal_output.ensureCursorVisible()
        fmt.setForeground(QColor("black"))
        cursor.setCharFormat(fmt)
        self.terminal_output.setTextCursor(cursor)

    def range_submit(self,):
        self.axis_x_raw.setRange(0,1)
        self.axis_y_raw.setRange(0,1)