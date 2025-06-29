from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor




class terminal_handler():
    terminal_output = None

    def widget_terminal_output(self):
        self.terminal_output = QtWidgets.QPlainTextEdit()
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

        return self.terminal_output

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
        fmt.setForeground(QColor("white"))
        cursor.setCharFormat(fmt)
        self.terminal_output.setTextCursor(cursor)