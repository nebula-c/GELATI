from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

class control_handler:
    setting_comp_height = 30
    layout_settings = None
    layout_raw_setting = None
    layout_raw_setting_label = None
    layout_raw_setting_lineedit = None

    label_xmin = None
    label_xmax = None
    label_ymin = None
    label_ymax = None

    lineedit_xmin = None
    lineedit_xmax = None
    lineedit_ymin = None
    lineedit_ymax = None


    def set_callback(self, name, func):
        setattr(self, name, func)
    
    def control_widget(self,):
        self.layout_settings = QtWidgets.QHBoxLayout()
        self.layout_raw_setting = QtWidgets.QVBoxLayout()
        self.layout_raw_setting_label = QtWidgets.QHBoxLayout()
        self.layout_raw_setting_lineedit = QtWidgets.QHBoxLayout()

        layout_settings = self.layout_settings
        layout_raw_setting = self.layout_raw_setting
        layout_raw_setting_label = self.layout_raw_setting_label
        layout_raw_setting_lineedit = self.layout_raw_setting_lineedit

        layout_settings.setContentsMargins(0,0,0,0)
        layout_settings.setSpacing(0)
        layout_raw_setting.setSpacing(1)
        layout_raw_setting.setContentsMargins(0,0,0,0)
        layout_raw_setting_label.setContentsMargins(0,0,0,0)
        layout_raw_setting_lineedit.setContentsMargins(0,0,0,0)

        self.rawchart_lineedit()
        

        layout_raw_setting.addLayout(layout_raw_setting_label)
        layout_raw_setting.addLayout(layout_raw_setting_lineedit)
        layout_raw_setting.addStretch()

        layout_settings.addWidget(self.widget_raw_settings(),stretch=2)
        

        widgets_modeling_buttons = self.widgets_modeling_buttons()
        layout_settings.addWidget(widgets_modeling_buttons,stretch=1)
        
        
        control_widget = QtWidgets.QWidget()        
        control_widget.setLayout(layout_settings)

        return control_widget
    
        



    def rawchart_lineedit(self,):
        self.label_xmin = QtWidgets.QLabel("xmin")
        self.label_xmax = QtWidgets.QLabel("xmax")
        self.label_ymin = QtWidgets.QLabel("ymin")
        self.label_ymax = QtWidgets.QLabel("ymax")

        self.lineedit_xmin = QtWidgets.QLineEdit()
        self.lineedit_xmax = QtWidgets.QLineEdit()
        self.lineedit_ymin = QtWidgets.QLineEdit()
        self.lineedit_ymax = QtWidgets.QLineEdit()

        for widget in [self.label_xmin, self.label_xmax, self.label_ymin, self.label_ymax]:
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout_raw_setting_label.addWidget(widget)

        for widget in [self.lineedit_xmin, self.lineedit_xmax,self.lineedit_ymin, self.lineedit_ymax]:
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout_raw_setting_lineedit.addWidget(widget)
            widget.setFixedHeight(self.setting_comp_height)
            


    def widget_raw_settings(self,):
        reset_buttons = self.reset_buttons()
        submit_buttons = self.submit_buttons()
        
        self.layout_raw_setting_label.addWidget(reset_buttons)
        self.layout_raw_setting_lineedit.addWidget(submit_buttons)

        for widget in [reset_buttons, submit_buttons]:
            widget.setFixedSize(80, self.setting_comp_height)
        
        raw_widget = QtWidgets.QWidget()        
        raw_widget.setLayout(self.layout_raw_setting)
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
        
        return raw_widget
        
        
        
    def reset_buttons(self,):
        button_range_reset = QtWidgets.QPushButton("Reset")
        button_range_reset.clicked.connect(lambda: self.raw_chart_range_reset())
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
        return button_range_reset

    def submit_buttons(self,):
        button_range_submit = QtWidgets.QPushButton("Submit")
        button_range_submit.clicked.connect(lambda: self.raw_chart_range_submit())
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
        return button_range_submit


    def widgets_modeling_buttons(self,):
        layout_modeling_setting = QtWidgets.QVBoxLayout()
        layout_modeling_setting.setContentsMargins(10,0,0,10)

        layout_modeling_setting_1 = QtWidgets.QHBoxLayout()
        layout_modeling_setting_2 = QtWidgets.QHBoxLayout()

        layout_modeling_setting_1.addStretch()
        layout_modeling_setting_2.addStretch()



        ### ----------------------
        ### Peaks button
        ### ----------------------
        button_modeling_peaks = QtWidgets.QPushButton("Peaks")
        button_modeling_peaks.clicked.connect(lambda: self.seeking_peak())
        button_modeling_peaks.setStyleSheet("""
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
        button_modeling_peaks.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_1.addWidget(button_modeling_peaks)        

        ### ----------------------
        ### Select button
        ### ----------------------
        button_modeling_select = QtWidgets.QPushButton("Select")
        button_modeling_select.clicked.connect(lambda: self.show_sel())
        button_modeling_select.setStyleSheet("""
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
        button_modeling_select.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_1.addWidget(button_modeling_select)     

        ### ----------------------
        ### Run button
        ### ----------------------
        button_modeling_run = QtWidgets.QPushButton("Run")
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
        button_modeling_run.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_1.addWidget(button_modeling_run)        


        ### ----------------------
        ### Phase button
        ### ----------------------
        button_modeling_phase = QtWidgets.QPushButton("Phase")
        button_modeling_phase.clicked.connect(lambda: self.Change_phase())
        button_modeling_phase.setStyleSheet("""
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
        button_modeling_phase.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_2.addWidget(button_modeling_phase)        



        ### ----------------------
        ### Setting button
        ### ----------------------
        button_modeling_setting = QtWidgets.QPushButton("Setting")
        button_modeling_setting.clicked.connect(lambda: self.open_setting_window())
        button_modeling_setting.setStyleSheet("""
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
        button_modeling_setting.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_2.addWidget(button_modeling_setting)


        ### ----------------------
        ### Export button
        ### ----------------------
        button_modeling_export = QtWidgets.QPushButton("Export")
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
        button_modeling_export.setFixedSize(80, self.setting_comp_height)
        layout_modeling_setting_2.addWidget(button_modeling_export)        



        

        layout_modeling_setting_1.addStretch()
        layout_modeling_setting_1.setSpacing(1)
        layout_modeling_setting_2.addStretch()
        layout_modeling_setting_2.setSpacing(1)
        layout_modeling_setting.addStretch()
        layout_modeling_setting.setSpacing(1)

        layout_modeling_setting.addLayout(layout_modeling_setting_1)
        layout_modeling_setting.addLayout(layout_modeling_setting_2)

        modeling_widget = QtWidgets.QWidget()        
        modeling_widget.setLayout(layout_modeling_setting)


        return modeling_widget
        

    def raw_chart_range_reset(self,):
        self.reset_raw_chart()
        self.Show_raw_chart()
        self.set_bridge_raw_data()
        self.print_terminal("Chart is reseted")

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

        self.set_axis_range()
        
        self.range_slicing(xmin,xmax)
        self.set_modeling_yaix_range_new()

        self.print_terminal("Range is changed: {}-{} / {}-{}".format(xmin,xmax,ymin,ymax))

    def file_export(self,):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "Text Files (*.txt);;All Files (*)")

        

        try:
            if file_path:
                list_guide_time, list_guide_amp = self.get_guide_data()

                with open(file_path, 'w') as f:
                    for iter in range(len(list_guide_time)):
                        temp_time = list_guide_time[iter]
                        temp_amp = list_guide_amp[iter]
                        f.write("{}, {}\n".format(temp_time, temp_amp))
            self.print_terminal("File({}) is saved".format(file_path))

        except:
            self.print_terminal_colored("Failed to export as file")



    def set_lineedit_raw_range(self):
        xmin,xmax,ymin,ymax = self.get_raw_chart_range()
        self.lineedit_xmin.setText(str(xmin))
        self.lineedit_xmax.setText(str(xmax))
        self.lineedit_ymin.setText(str(ymin))
        self.lineedit_ymax.setText(str(ymax))

    def get_sliced_range(self):
        return self.sliced_min_time, self.sliced_max_time, self.min_raw_val, self.max_raw_val

    def get_new_yrange(self):
        return self.min_raw_val,self.max_raw_val