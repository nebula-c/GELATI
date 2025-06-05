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
        self.Window_Setting.set_widget(self.widget_total_setting())
        self.Window_Setting.show()
    


    def widget_total_setting(self,):
        layout_settings = QtWidgets.QVBoxLayout()
        layout_setting_main = QtWidgets.QHBoxLayout()
        layout_labels = QtWidgets.QVBoxLayout()
        layout_lineedits = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels)
        layout_setting_main.addLayout(layout_lineedits)

        self.my_interpolation_step, self.my_time_for_1breath, self.my_datarate = self.get_parameter()

        layout_labels_interpolation_step = QtWidgets.QLabel("Interpolation step")
        layout_lineedit_interpolation_step = QtWidgets.QLineEdit()
        layout_lineedit_interpolation_step.setText(str(self.my_interpolation_step))
        layout_labels.addWidget(layout_labels_interpolation_step)
        layout_lineedits.addWidget(layout_lineedit_interpolation_step)

        layout_labels_expected_time_1breath = QtWidgets.QLabel("Expected time for 1 breath (sec)")
        layout_lineedit_expected_time_1breath = QtWidgets.QLineEdit()
        layout_lineedit_expected_time_1breath.setText(str(self.my_time_for_1breath))
        layout_labels.addWidget(layout_labels_expected_time_1breath)
        layout_lineedits.addWidget(layout_lineedit_expected_time_1breath)

        layout_labels_datarate = QtWidgets.QLabel("Datarate(# of data for 1min)")
        layout_lineedit_datarate = QtWidgets.QLineEdit()
        layout_lineedit_datarate.setText(str(self.my_datarate))
        layout_labels.addWidget(layout_labels_datarate)
        layout_lineedits.addWidget(layout_lineedit_datarate)
        
        layout_settings.addLayout(layout_setting_main)



        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout_settings.addWidget(line1)




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
        self.print_terminal("Setting is changed")
        self.not_dev()
        self.Window_Setting.close()
    
    def func_cancel(self):
        self.Window_Setting.close()
    
    
    def read_setting_value(self,):
        return
    
    def save_setting_value(self,):
        return