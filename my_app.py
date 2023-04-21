from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QRadioButton,
        QPushButton, QLabel, QListWidget, QLineEdit)

from instr import *
from second_win import *

       
class MainWin(QWidget):
    def __init__(self):
        ''' вікно, в якому розташовується привітання '''
        super().__init__()

        # створюємо та налаштовуємо графічні елементи:
        self.initUI()

        #Встановлює зв'язки між елементами
        self.connects()

        #Встановлює, як виглядатиме вікно (напис, розмір, місце)
        self.set_appear()

        # старт:
        self.show()

    def initUI(self):
        ''' створює графічні елементи '''
        self.btn_next = QPushButton(txt_next)
        self.hello_text = QLabel(txt_hello)
        self.instruction = QLabel(txt_instruction)

        self.layout_line = QVBoxLayout()
        self.layout_line.addWidget(self.hello_text, alignment = Qt.AlignLeft)
        self.layout_line.addWidget(self.instruction, alignment = Qt.AlignLeft) 
        self.layout_line.addWidget(self.btn_next, alignment = Qt.AlignCenter)          
        self.setLayout(self.layout_line)

    
    def next_click(self):
        self.hide()
        self.tw = TestWin()
        

    def connects(self):
        self.btn_next.clicked.connect(self.next_click)

    ''' встановлює, як виглядатиме вікно (напис, розмір, місце) '''
    def set_appear(self):
        self.setWindowTitle(txt_title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

app = QApplication([])
mw = MainWin()
app.exec_()