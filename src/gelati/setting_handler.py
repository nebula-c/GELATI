from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

class Window_Setting(QtWidgets.QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Settings")
    
    def set_widget(self,mywidget):
        layout_setting_total = QtWidgets.QHBoxLayout()
        layout_setting_total.addWidget(mywidget)
        self.setLayout(layout_setting_total)
    
    
class setting_handler:
    def __init__(self,):
        self.Window_Setting = Window_Setting()
    
    def set_callback(self, name, func):
        setattr(self, name, func)

    def open_setting_window(self):
        self.Window_Setting = Window_Setting()
        self.my_interpolation_step, self.my_time_for_1breath, self.my_datarate, self.sigma_selA, self.sigma_selC= self.get_parameter()
        self.Window_Setting.set_widget(self.widget_total_setting())
        self.Window_Setting.show()
    


    def widget_total_setting(self,):
        layout_settings = QtWidgets.QVBoxLayout()
        layout_setting_main = QtWidgets.QHBoxLayout()
        layout_labels = QtWidgets.QVBoxLayout()
        layout_lineedits = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels)
        layout_setting_main.addLayout(layout_lineedits)
        layout_labels2 = QtWidgets.QVBoxLayout()
        layout_lineedits2 = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels2)
        layout_setting_main.addLayout(layout_lineedits2)

        labels_interpolation_step = QtWidgets.QLabel("Interpolation step")
        self.lineedit_interpolation_step = QtWidgets.QLineEdit()
        self.lineedit_interpolation_step.setText(str(self.my_interpolation_step))
        layout_labels.addWidget(labels_interpolation_step)
        layout_lineedits.addWidget(self.lineedit_interpolation_step)

        labels_expected_time_1breath = QtWidgets.QLabel("Expected time for 1 breath (sec)")
        self.lineedit_expected_time_1breath = QtWidgets.QLineEdit()
        self.lineedit_expected_time_1breath.setText(str(self.my_time_for_1breath))
        layout_labels.addWidget(labels_expected_time_1breath)
        layout_lineedits.addWidget(self.lineedit_expected_time_1breath)

        labels_datarate = QtWidgets.QLabel("Datarate(# of data for 1min)")
        self.lineedit_datarate = QtWidgets.QLineEdit()
        self.lineedit_datarate.setText(str(self.my_datarate))
        layout_labels.addWidget(labels_datarate)
        layout_lineedits.addWidget(self.lineedit_datarate)
        
        layout_settings.addLayout(layout_setting_main)



        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout_settings.addWidget(line1)


        labels_sigma_selectionA = QtWidgets.QLabel("Sigma for the period selection")
        self.lineedit_sigma_selectionA = QtWidgets.QLineEdit()
        self.lineedit_sigma_selectionA.setText(str(self.sigma_selA))
        layout_labels2.addWidget(labels_sigma_selectionA)
        layout_lineedits2.addWidget(self.lineedit_sigma_selectionA)

        labels_sigma_selectionC = QtWidgets.QLabel("Sigma for the peak heights")
        self.lineedit_sigma_selectionC = QtWidgets.QLineEdit()
        self.lineedit_sigma_selectionC.setText(str(self.sigma_selC))
        layout_labels2.addWidget(labels_sigma_selectionC)
        layout_lineedits2.addWidget(self.lineedit_sigma_selectionC)

        layout_settings.addLayout(layout_setting_main)


        layout_bottom_buttons = QtWidgets.QHBoxLayout()
        save_buttons = self.save_buttons()
        cancel_buttons = self.cancel_buttons()
        layout_bottom_buttons.addWidget(save_buttons)
        layout_bottom_buttons.addWidget(cancel_buttons)
        layout_settings.addLayout(layout_bottom_buttons)


        widget_total = QtWidgets.QWidget()
        widget_total.setLayout(layout_settings)
        return widget_total


    
        
    def save_buttons(self,):
        button_range_save = QtWidgets.QPushButton("Save")
        button_range_save.clicked.connect(lambda: self.func_save())
        button_range_save.setStyleSheet("""
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
        return button_range_save
    
    def cancel_buttons(self,):
        button_range_cancel = QtWidgets.QPushButton("Cancel")
        button_range_cancel.clicked.connect(lambda: self.func_cancel())
        button_range_cancel.setStyleSheet("""
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
        return button_range_cancel

    def func_save(self):
        my_interpolation_step = self.lineedit_interpolation_step.text()
        my_time_for_1breath = self.lineedit_expected_time_1breath.text()
        my_datarate = self.lineedit_datarate.text()

        mysigma_A = self.lineedit_sigma_selectionA.text()
        mysigma_C = self.lineedit_sigma_selectionC.text()


        try:
            self.set_parameter(my_interpolation_step,my_time_for_1breath,my_datarate,mysigma_A,mysigma_C)
        except:
            self.print_terminal_colored("Please check values...")
            return

        self.reset_modeling_chart()
        self.print_terminal("Setting is changed")
        self.print_terminal("Modeing chart is reseted")
        self.Window_Setting.close()
    
    def func_cancel(self):
        self.Window_Setting.close()
    
    
    def read_setting_value(self,):
        return
    
    def save_setting_value(self,):
        return