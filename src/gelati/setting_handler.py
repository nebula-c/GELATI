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
        self.order_sigma = [100,100,100]
        self.selec_order = ["None","None","None"]
    
    def set_callback(self, name, func):
        setattr(self, name, func)

    def open_setting_window(self):
        self.Window_Setting = Window_Setting()
        self.my_interpolation_step, self.my_time_for_1breath, self.my_datarate, self.order_sigma, self.selec_order = self.get_parameter()
        self.Window_Setting.set_widget(self.widget_total_setting())
        self.Window_Setting.show()
    


    def widget_total_setting(self,):
        layout_settings = QtWidgets.QVBoxLayout()
        layout_setting_main = QtWidgets.QHBoxLayout()
        layout_labels = QtWidgets.QVBoxLayout()
        layout_lineedits = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels)
        layout_setting_main.addLayout(layout_lineedits)

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



        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        line1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout_setting_main.addWidget(line1)



        
        layout_labels2 = QtWidgets.QVBoxLayout()
        layout_lineedits2 = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels2)
        layout_setting_main.addLayout(layout_lineedits2)

        labels_sigma_first_selection = QtWidgets.QLabel("Sigma for first selection")
        self.lineedit_sigma_first_selection = QtWidgets.QLineEdit()
        self.lineedit_sigma_first_selection.setText(str(self.order_sigma[0]))
        layout_labels2.addWidget(labels_sigma_first_selection)
        layout_lineedits2.addWidget(self.lineedit_sigma_first_selection)

        labels_sigma_second_selection = QtWidgets.QLabel("Sigma for second selection")
        self.lineedit_sigma_second_selection = QtWidgets.QLineEdit()
        self.lineedit_sigma_second_selection.setText(str(self.order_sigma[1]))
        layout_labels2.addWidget(labels_sigma_second_selection)
        layout_lineedits2.addWidget(self.lineedit_sigma_second_selection)

        labels_sigma_third_selection = QtWidgets.QLabel("Sigma for third heights")
        self.lineedit_sigma_third_selection = QtWidgets.QLineEdit()
        self.lineedit_sigma_third_selection.setText(str(self.order_sigma[2]))
        layout_labels2.addWidget(labels_sigma_third_selection)
        layout_lineedits2.addWidget(self.lineedit_sigma_third_selection)


        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout_setting_main.addWidget(line2)






        layout_labels3 = QtWidgets.QVBoxLayout()
        layout_lineedits3 = QtWidgets.QVBoxLayout()
        layout_setting_main.addLayout(layout_labels3)
        layout_setting_main.addLayout(layout_lineedits3)

        label_sel_first = QtWidgets.QLabel("First selection")
        layout_labels3.addWidget(label_sel_first)
        self.combomox_first_sel = QtWidgets.QComboBox()
        self.combomox_first_sel.addItems(["Period","Baseline","Peak_height","None"])
        self.combomox_first_sel.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
            }
        """)
        myindex = self.combomox_first_sel.findText(self.selec_order[0])
        self.combomox_first_sel.setCurrentIndex(myindex)
        layout_lineedits3.addWidget(self.combomox_first_sel)

        label_sel_second = QtWidgets.QLabel("Second selection")
        layout_labels3.addWidget(label_sel_second)
        self.combomox_second_sel = QtWidgets.QComboBox()
        self.combomox_second_sel.addItems(["Period","Baseline","Peak_height","None"])
        self.combomox_second_sel.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
            }
        """)
        myindex = self.combomox_second_sel.findText(self.selec_order[1])
        self.combomox_second_sel.setCurrentIndex(myindex)
        self.selec_order[1] = self.combomox_second_sel.currentText()
        layout_lineedits3.addWidget(self.combomox_second_sel)

        label_sel_third = QtWidgets.QLabel("Third selection")
        layout_labels3.addWidget(label_sel_third)
        self.combomox_third_sel = QtWidgets.QComboBox()
        self.combomox_third_sel.addItems(["Period","Baseline","Peak_height","None"])
        self.combomox_third_sel.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
            }
        """)
        myindex = self.combomox_third_sel.findText(self.selec_order[2])
        self.combomox_third_sel.setCurrentIndex(myindex)
        self.selec_order[2] = self.combomox_third_sel.currentText()
        layout_lineedits3.addWidget(self.combomox_third_sel)

        
        
        
        
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

        try:
            self.order_sigma[0] = float(self.lineedit_sigma_first_selection.text())
            self.order_sigma[1] = float(self.lineedit_sigma_second_selection.text())
            self.order_sigma[2] = float(self.lineedit_sigma_third_selection.text())

            self.selec_order[0] = self.combomox_first_sel.currentText()
            self.selec_order[1] = self.combomox_second_sel.currentText()
            self.selec_order[2] = self.combomox_third_sel.currentText()

            self.set_parameter(my_interpolation_step,my_time_for_1breath,my_datarate,self.order_sigma,self.selec_order)
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