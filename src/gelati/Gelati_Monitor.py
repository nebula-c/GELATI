from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from gelati import core_bridge
from gelati import file_reader
from gelati import logo_handler
from gelati import fileloader_handler
from gelati import rawchart_handler
from gelati import modelingchart_handler
from gelati import terminal_handler
from gelati import setting_handler
from gelati import total_callback


class Gelati_Monitor(QtWidgets.QMainWindow):
    app = None
    filetype = None
    list_raw_time = None
    list_raw_amp = None
    list_guide_time = None
    list_guide_amp = None
    min_raw_val = None
    max_raw_val = None
    sliced_min_time = None
    sliced_max_time = None
    chart_raw = None
    

    def __init__(self,):
        super().__init__()
        self.terminal_handler = terminal_handler.terminal_handler()
        self.fileloader_handler = fileloader_handler.fileloader_handler()
        self.rawchart_handler = rawchart_handler.rawchart_handler()
        self.setting_handler = setting_handler.setting_handler()
        self.modelingchart_handler = modelingchart_handler.modelingchart_handler()
        
        self.Basic_Framing()
        self.Bridge = core_bridge.Bridge()

        total_callback.total_callback(self)
    


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
        ### Logo
        ### ---------------------------------------------
        layout_logo = QtWidgets.QHBoxLayout()
        layout_logo.setSpacing(0)
        widget_logo = logo_handler.widget_logo()
        layout_logo.addWidget(widget_logo)
        layout_top.addLayout(layout_logo)

        ### ---------------------------------------------
        ### Button to load file
        ### ---------------------------------------------
        layout_file_load = self.fileloader_handler.layout_file_load()
        layout_top.addLayout(layout_file_load)

        ### ---------------------------------------------
        ### Combo box to choose file type
        ### ---------------------------------------------
        combomox_filetype = self.fileloader_handler.combomox_filetype()
        layout_file_load.addWidget(combomox_filetype)
        layout_top.setContentsMargins(0, 0, 0, 0)  
        self.layout.addLayout(layout_top)

        
        ### ---------------------------------------------
        ### CHART - raw
        ### ---------------------------------------------
        layout_chart = QtWidgets.QHBoxLayout()
        layout_chart.setContentsMargins(0,0,0,0)
        layout_chart.setSpacing(0)

        chart_raw_view = self.rawchart_handler.chart_raw_view()
        layout_chart.setContentsMargins(0, 0, 0, 0)
        layout_chart.addWidget(chart_raw_view,stretch=2)


        ### ---------------------------------------------
        ### CHART - modeling
        ### ---------------------------------------------
        chart_modeling_view = self.modelingchart_handler.chart_modeling_view()
        layout_chart.addWidget(chart_modeling_view, stretch=1)
        
        charts_widget = QtWidgets.QWidget(self)        
        charts_widget.setLayout(layout_chart)

        self.layout.addWidget(charts_widget, stretch=4)
        self.layout.addStretch()

        # ### ---------------------------------------------
        # ### Settings_widget
        # ### ---------------------------------------------
        settings_widget = self.setting_handler.settings_widget()
        self.layout.addWidget(settings_widget,stretch=1)
        
        ### ---------------------------------------------
        ### Terminal
        ### ---------------------------------------------        
        self.terminal_output = self.terminal_handler.widget_terminal_output()
        self.layout.addWidget(self.terminal_output)
        self.layout.setContentsMargins(10, 10, 10, 20)

        self.terminal_handler.print_terminal("You can find the full code here. https://github.com/nebula-c/GELATI (suchoi9709@gmail.com, Sungwoon Choi)")
        self.terminal_handler.print_terminal("")
        self.terminal_output.setFixedHeight(100)



    def show_message(self, mytext):
        msg = QtWidgets.QMessageBox()
        msg.setText(mytext)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()

    def not_dev(self,):
        self.show_message("Not developed yet")
