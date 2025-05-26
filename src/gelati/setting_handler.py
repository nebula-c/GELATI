from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

class Window_Setting(QtWidgets.QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Settings")
    
    def set_widget(self,mywidget):
        layout_setting = QtWidgets.QHBoxLayout()
        layout_setting.addWidget(mywidget)
        self.setLayout(layout_setting)
    
    
class setting_handler:
    def __init__(self,):
        self.Window_Setting = Window_Setting()
    
    def set_callback(self, name, func):
        setattr(self, name, func)

    def open_setting_window(self):
        self.Window_Setting.set_widget(self.widget_total_setting())
        self.Window_Setting.show()
    


    def widget_total_setting(self,):
        layout_settings = QtWidgets.QHBoxLayout()
        
        save_buttons = self.save_buttons()
        cancel_buttons = self.cancel_buttons()

        layout_settings.addWidget(save_buttons)
        layout_settings.addWidget(cancel_buttons)

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
        self.Window_Setting.close()
    
    def func_cancel(self):
        self.Window_Setting.close()
    
    
        