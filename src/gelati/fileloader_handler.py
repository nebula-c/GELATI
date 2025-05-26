from PyQt6 import QtWidgets
from gelati import file_reader

class fileloader_handler:
    filetype = None
    list_raw_time = None
    list_raw_amp = None
    print_terminal = None
    print_terminal_colored = None

    # def __init__(self,):

    def set_callback(self, name, func):
        setattr(self, name, func)

    def layout_file_load(self,):
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
        
        return layout_file_load

    def combomox_filetype(self,):
        combomox_filetype = QtWidgets.QComboBox()
        combomox_filetype.addItems(["Abches","Anzai"])
        combomox_filetype.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
            }
        """)
        combomox_filetype.currentTextChanged.connect(lambda text: setattr(self,'filetype', text))
        self.filetype =  combomox_filetype.itemText(0)
        # layout_file_load.addWidget(combomox_filetype)
        return combomox_filetype

    def open_file_dialog(self,):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select file", "", "All files (*)")

        if file_path:
            if self.filetype == "Abches":
                self.list_raw_time, self.list_raw_amp = file_reader.read_abches(file_path)
                if self.list_raw_time is not None and self.list_raw_amp is not None:
                    self.print_terminal("File {} is opened".format(file_path))
                else:
                    self.print_terminal_colored("Cannot read file {}.".format(file_path), color='#ff0000')    
                    return
            elif self.filetype == "Anzai":
                self.list_raw_time, self.list_raw_amp = file_reader.read_anzai(file_path)
                if self.list_raw_time is not None and self.list_raw_amp is not None:
                    self.print_terminal("File {} is opened".format(file_path))
                else:
                    self.print_terminal_colored("Cannot read file {}.".format(file_path), color='#ff0000')    
                    return
            else:
                self.print_terminal_colored("Undefined file type", color='#ff0000')
                return
            
            self.filename = file_path
            self.set_raw_chart_title()
            self.set_rawchart_raw_data()
            self.Show_raw_chart()

            self.set_bridge_raw_data()

        
        else:
            return
    
    def get_filename(self,):
        return self.filename

    def get_filetype(self,):
        return self.filetype
        
    def get_raw_data(self,):
        return self.list_raw_time, self.list_raw_amp
