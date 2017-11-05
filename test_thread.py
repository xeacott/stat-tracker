from PyQt5.QtWidgets import QApplication,QPushButton,QMainWindow,QLabel,QLineEdit,QCompleter
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPoint
import sys

class cssden(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #size
        self.setFixedSize(600,400)

        #LINE EDIT QCOMPLETER
        self.label = QLineEdit(self)
        self.label.setGeometry(100,100,300,30)
        self.label.setStyleSheet("color: red;"
                                "font: bold 15pt 'Arial';")

        self.label.textChanged.connect(self.to_upper)

        self.t = ["HELLO","HI","HEY"]
        my_completer = QCompleter(self.t, self)
        #my_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        my_completer.setCaseSensitivity(1)
        self.label.setCompleter(my_completer)

        #BUTTON
        self.buton = QPushButton(self)
        self.buton.setText("Click")
        self.buton.setGeometry(200,140,90,50)

        self.buton.clicked.connect(self.hangiButon)

        #SET LABEL
        self.set_label = QLabel(self)
        self.set_label.setGeometry(100,300,900,100)
        self.set_label.setStyleSheet("color: green;"
                                    "font: bold 18pt 'Times New Roman';")
        self.show()

    def to_upper(self, txt):
        self.label.setText(txt.upper())

    def hangiButon(self):
        print(self.label.text(), self.t.index(self.label.text())+1)
        self.set_label.setText("Pressed to --> {}.".format(self.label.text().rstrip()))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow{background-color: rgb(30,30,30);border: 2px solid rgb(20,20,20)}")

ex = cssden()
sys.exit(app.exec_())