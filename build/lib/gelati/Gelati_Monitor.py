import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtCore import QTimer, Qt, QPointF, QMargins
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from datetime import datetime
import os,sys
import pkg_resources
import logging
import time

from gelati import core_bridge
from gelati import file_reader


class Gelati_Monitor(QtWidgets.QMainWindow):
    filetype = None
    list_raw_time = None
    list_raw_amp = None
    list_guide_time = None
    list_guide_amp = None
    min_raw_val = None
    max_raw_val = None
    sliced_min_time = None
    sliced_max_time = None

    def __init__(self,):
        super().__init__()
        self.Basic_Framing()
        self.Bridge = core_bridge.Bridge()


    def Basic_Framing(self,):
        self.setWindowTitle("GELATI")
        self.setGeometry(100, 100, 800, 600)

        self.widget_central = QtWidgets.QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout = QtWidgets.QVBoxLayout(self.widget_central)
        self.layout.setSpacing(0)
        self.widget_central.setStyleSheet("background-color: white;")



        layout_top = QtWidgets.QHBoxLayout()
        layout_top.setContentsMargins(10, 0, 10, 0)

        ### ---------------------------------------------
        ### Logo(temp)
        ### ---------------------------------------------
        layout_logo = QtWidgets.QHBoxLayout()
        layout_logo.setSpacing(0)
        label_logo = QtWidgets.QLabel()
        # logo_path = pkg_resources.resource_filename('gelati', 'images/gelati_logo2.png')
        logo_path = self.resource_path('gelati', 'images/gelati_logo2.png')
        pixmap_logo = QPixmap(logo_path)
        pixmap_scaled_logo = pixmap_logo.scaled(1000, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label_logo.setPixmap(pixmap_scaled_logo)
        layout_logo.addWidget(label_logo)
        
        layout_top.addLayout(layout_logo)


        ### ---------------------------------------------
        ### Button to load file
        ### ---------------------------------------------
        layout_file_load = QtWidgets.QVBoxLayout()
        button_file_load = QtWidgets.QPushButton("Open file")
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

        button_file_load.clicked.connect(lambda: self.open_file_dialog())
        layout_file_load.addWidget(button_file_load)
        layout_file_load.setSpacing(0)
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
        layout_chart.setContentsMargins(0,0,0,0)
        layout_chart.setSpacing(0)
        self.chart_raw = QChart()
        self.chart_raw.setMargins(QMargins(0, 0, 0, 0))
        self.chart_raw.setTitle("TEST")

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


        self.chart_raw_view = QChartView(self.chart_raw)
        self.chart_raw_view.setContentsMargins(100, 100, 100, 100)
        self.chart_raw_view.setStyleSheet("padding:0px; margin:0px; border:0px;")

        
        self.chart_raw_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        layout_chart.addWidget(self.chart_raw_view,stretch=2)


        ### ---------------------------------------------
        ### CHART - modeling
        ### ---------------------------------------------
        self.chart_modeling = QChart()
        self.chart_modeling.setMargins(QMargins(0, 0, 0, 0))
        self.chart_modeling.setTitle("Modeling")


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
        
        layout_chart.setContentsMargins(0, 0, 0, 0)
        self.chart_modeling_view = QChartView(self.chart_modeling)
        self.chart_modeling_view.setContentsMargins(0, 0, 0, 0)
        
        self.chart_modeling_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        layout_chart.addWidget(self.chart_modeling_view, stretch=1)
        
        charts_widget = QtWidgets.QWidget(self)        
        charts_widget.setLayout(layout_chart)

        self.layout.addWidget(charts_widget, stretch=4)
        self.layout.addStretch()
        # self.layout.addLayout(layout_chart)
        # self.layout.setStretchFactor(layout_chart, 4)

        ### ---------------------------------------------
        ### LineEdit to set range for chart-raw
        ### ---------------------------------------------
        layout_settings = QtWidgets.QHBoxLayout()
        layout_settings.setContentsMargins(0,0,0,0)
        layout_settings.setSpacing(0)
        layout_raw_setting = QtWidgets.QVBoxLayout()
        layout_raw_setting.setSpacing(1)
        layout_raw_setting.setContentsMargins(0,0,0,0)
        layout_raw_setting_label = QtWidgets.QHBoxLayout()
        layout_raw_setting_label.setContentsMargins(0,0,0,0)
        layout_raw_setting_lineedit = QtWidgets.QHBoxLayout()
        layout_raw_setting_lineedit.setContentsMargins(0,0,0,0)

        setting_comp_height = 30

        label_xmin = QtWidgets.QLabel("xmin")
        label_xmax = QtWidgets.QLabel("xmax")
        label_ymin = QtWidgets.QLabel("ymin")
        label_ymax = QtWidgets.QLabel("ymax")

        self.lineedit_xmin = QtWidgets.QLineEdit(self)
        self.lineedit_xmax = QtWidgets.QLineEdit(self)
        self.lineedit_ymin = QtWidgets.QLineEdit(self)
        self.lineedit_ymax = QtWidgets.QLineEdit(self)

        for widget in [label_xmin, label_xmax,label_ymin, label_ymax]:
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_raw_setting_label.addWidget(widget)

        for widget in [self.lineedit_xmin, self.lineedit_xmax,self.lineedit_ymin, self.lineedit_ymax]:
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_raw_setting_lineedit.addWidget(widget)
            widget.setFixedHeight(setting_comp_height)

        layout_raw_setting.addLayout(layout_raw_setting_label)
        layout_raw_setting.addLayout(layout_raw_setting_lineedit)
        layout_raw_setting.addStretch()


        
        
        button_range_reset = QtWidgets.QPushButton("Reset", self)
        button_range_reset.clicked.connect(lambda: self.raw_chart_range_reset())
        layout_raw_setting_label.addWidget(button_range_reset)
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

        button_range_submit = QtWidgets.QPushButton("Submit", self)
        button_range_submit.clicked.connect(lambda: self.raw_chart_range_submit())
        layout_raw_setting_lineedit.addWidget(button_range_submit)
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

        for widget in [button_range_reset, button_range_submit]:
            widget.setFixedSize(80, setting_comp_height)
        
        raw_widget = QtWidgets.QWidget(self)        
        raw_widget.setLayout(layout_raw_setting)
        raw_widget.setStyleSheet("""
            QLabel {
                font-size: 14px;
                border: 2px solid #333333;
                background-color: #f0f0f0;
            }
            QLineEdit {
                font-size: 14px;
                border: 1px solid #333333;
                background-color: #f0f0f0;
            }
        """)
        
        layout_settings.addWidget(raw_widget,stretch=2)
        



        ### ---------------------------------------------
        ### LineEdit to set range for chart-modeling
        ### ---------------------------------------------
        layout_modeling_setting = QtWidgets.QVBoxLayout()
        layout_modeling_setting.setContentsMargins(10,0,0,10)

        button_modeling_run = QtWidgets.QPushButton("Run", self)
        button_modeling_run.clicked.connect(lambda: self.guide_modeling_run())
        button_modeling_run.setStyleSheet("""
            QPushButton {
                background-color: #aaaaaa;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;xw
            }
            QPushButton:hover {
                background-color: #888888;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        layout_modeling_setting.addWidget(button_modeling_run)        

        button_modeling_specific = QtWidgets.QPushButton("Specific", self)
        button_modeling_specific.clicked.connect(lambda: self.not_dev())
        button_modeling_specific.setStyleSheet("""
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
        layout_modeling_setting.addWidget(button_modeling_specific)        

        button_modeling_export = QtWidgets.QPushButton("Export", self)
        button_modeling_export.clicked.connect(lambda: self.file_export())
        button_modeling_export.setStyleSheet("""
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
        layout_modeling_setting.addWidget(button_modeling_export)        


        layout_modeling_setting.addStretch()
        layout_modeling_setting.setSpacing(1)
        modeling_widget = QtWidgets.QWidget(self)        
        modeling_widget.setLayout(layout_modeling_setting)
        layout_settings.addWidget(modeling_widget,stretch=1)
        
        
        settings_widget = QtWidgets.QWidget(self)        
        settings_widget.setLayout(layout_settings)
    
        self.layout.addWidget(settings_widget,stretch=1)
        # self.layout.addLayout(layout_settings)
        # self.layout.setStretchFactor(layout_settings, 1)

        
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
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.terminal_output)
        self.layout.setContentsMargins(10, 10, 10, 20)
        self.print_terminal("You can find the full code here. https://github.com/nebula-c/GELATI (suchoi9709@gmail.com, Sungwoon Choi)")
        self.print_terminal("")
        self.terminal_output.setFixedHeight(100)

    def open_file_dialog(self,):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", "All files (*)")
        if file_path:
            if self.filetype == "ANZAI":
                self.list_raw_time, self.list_raw_amp = file_reader.read_anzai(file_path)
                if self.list_raw_time is not None and self.list_raw_amp is not None:
                    self.print_terminal("File {} is opened".format(file_path))
                else:
                    self.print_terminal_colored("Cannot read file {}.".format(file_path), color='#ff0000')    
                    return
            else:
                self.print_terminal_colored("Undefined file type", color='#ff0000')
                return
            self.chart_raw.setTitle("File : {}".format(file_path))
            self.Show_raw_chart()
            self.Bridge.set_raw_data(self.list_raw_time,self.list_raw_amp)
        
        else:
            return
                
    def Show_raw_chart(self,):
        
        try:
            series_file = QLineSeries()
            for x, y in zip(self.list_raw_time, self.list_raw_amp):
                series_file.append(QPointF(float(x), float(y)))
            
            for series in self.chart_raw.series():
                self.chart_raw.removeSeries(series)
            
            self.chart_raw.addSeries(series_file)
            series_file.attachAxis(self.axis_x_raw)
            series_file.attachAxis(self.axis_y_raw)
            xmin = min(self.list_raw_time)
            xmax = max(self.list_raw_time)
            ymin = min(self.list_raw_amp)
            ymax = max(self.list_raw_amp)
            self.min_raw_val = ymin
            self.max_raw_val = ymax
            self.sliced_min_time = xmin
            self.sliced_max_time = xmax

            self.axis_x_raw.setRange(xmin,xmax)
            self.axis_y_raw.setRange(ymin,ymax)
            self.lineedit_xmin.setText(str(xmin))
            self.lineedit_xmax.setText(str(xmax))
            self.lineedit_ymin.setText(str(ymin))
            self.lineedit_ymax.setText(str(ymax))

            self.print_terminal("Successed to load data from the file")

        except:
            self.print_terminal("Failed to show data from the file")

    def print_terminal(self, text):
        self.terminal_output.appendPlainText("{}".format(text))
    
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

    def raw_chart_range_submit(self,):
        try:
            xmin = float(self.lineedit_xmin.text())
            xmax = float(self.lineedit_xmax.text())
            ymin = float(self.lineedit_ymin.text())
            ymax = float(self.lineedit_ymax.text())
        except:
            self.print_terminal_colored("Cannot read values!")
            return

        self.min_raw_val = ymin
        self.max_raw_val = ymax
        self.sliced_min_time = xmin
        self.sliced_max_time = xmax


        self.axis_x_raw.setRange(xmin,xmax)
        self.axis_y_raw.setRange(ymin,ymax)

        self.Bridge.range_slicing(xmin,xmax)
        self.axis_y_modeling.setRange(self.min_raw_val,self.max_raw_val)
        self.print_terminal("Range is changed: {}-{} / {}-{}".format(xmin,xmax,ymin,ymax))

    def raw_chart_range_reset(self,):
        try:
            xmin = min(self.list_raw_time)
            xmax = max(self.list_raw_time)
            ymin = min(self.list_raw_amp)
            ymax = max(self.list_raw_amp)
        except:
            self.print_terminal_colored("No data")
            return
        
        self.min_raw_val = ymin
        self.max_raw_val = ymax
        self.sliced_min_time = xmin
        self.sliced_max_time = xmax

        self.axis_x_raw.setRange(xmin,xmax)
        self.axis_y_raw.setRange(ymin,ymax)

        self.lineedit_xmin.setText(str(xmin))
        self.lineedit_xmax.setText(str(xmax))
        self.lineedit_ymin.setText(str(ymin))
        self.lineedit_ymax.setText(str(ymax))

        self.Bridge.reset_slicing()
        self.axis_y_modeling.setRange(self.min_raw_val,self.max_raw_val)
        self.print_terminal("Range is reseted")

    def show_message(self, mytext):
        msg = QtWidgets.QMessageBox()
        msg.setText(mytext)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()

    def not_dev(self,):
        self.show_message("Not developed yet")

    def guide_modeling_run(self,):
        if self.filetype=="ANZAI":
            self.list_guide_time, self.list_guide_amp = self.Bridge.run_anzai()

            if self.list_guide_time is None or self.list_guide_amp is None:
                self.print_terminal_colored("Modeling is not working!!!")
                return
            else:
                self.Show_modeling_chart()
        
    def Show_modeling_chart(self,):
        series_modeling = QLineSeries()
        try:
            for x, y in zip(self.list_guide_time, self.list_guide_amp):
                series_modeling.append(QPointF(float(x), float(y)))
            for series in self.chart_modeling.series():
                self.chart_modeling.removeSeries(series)
            
            self.chart_modeling.addSeries(series_modeling)
            series_modeling.attachAxis(self.axis_x_modeling)
            series_modeling.attachAxis(self.axis_y_modeling)
            self.axis_x_modeling.setRange(min(self.list_guide_time),max(self.list_guide_time))
            self.axis_y_modeling.setRange(self.min_raw_val,self.max_raw_val)

            self.chart_modeling.setTitle("Modeling(range: {}-{})".format(self.sliced_min_time, self.sliced_max_time)) 
            self.print_terminal("Successed to generate guide-signal")

        except:
            self.print_terminal("Failed to show guide-signal")

    def file_export(self,):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")

        try:
            if file_path:
                with open(file_path, 'w') as f:
                    for iter in range(len(self.list_guide_time)):
                        temp_time = self.list_guide_time[iter]
                        temp_amp = self.list_guide_amp[iter]

                        f.write("{}, {}\n".format(temp_time, temp_amp))
            self.print_terminal("File({}) is saved".format(file_path))

        except:
            self.print_terminal_colored("Failed to export as file")



    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

