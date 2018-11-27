import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    EXIT_CODE_REBOOT = -123
    def __init__(self,parent=None):
        QMainWindow.__init__(self, parent)

    def keyPressEvent(self,e):
        if (e.key() == Qt.Key_R):
            qApp.exit( MainWindow.EXIT_CODE_REBOOT )


if __name__=="__main__":
    currentExitCode = MainWindow.EXIT_CODE_REBOOT
    while currentExitCode == MainWindow.EXIT_CODE_REBOOT:
        a = QApplication(sys.argv)
        w = MainWindow()
        w.show()
        currentExitCode = a.exec_()
        a = None  # delete the QApplication object