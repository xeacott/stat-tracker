from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
import sys
import worker


class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel("0")
        self.label1 = QLabel("0")
        self.label2 = QLabel("0")
        self.label3 = QLabel("0")

        # 1 - create Worker and Thread inside the Form
        self.obj = worker.Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.obj.intReady.connect(self.onIntReady)

        # 3 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.obj.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj.procCounter)

        # * - Thread finished signal will close the app if you want!
        # self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        self.thread.start()

        # 7 - Start the form
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.label1, 0, 1)
        grid.addWidget(self.label2, 0, 2)
        grid.addWidget(self.label3, 0, 3)

        self.move(300, 150)
        self.setWindowTitle('thread test')
        self.show()

    def onIntReady(self, i):
        self.label.setText("{}".format(i))
        self.label1.setText("{}".format(i))
        self.label2.setText("{}".format(i))
        self.label3.setText("{}".format(i))
        # print(i)

app = QApplication(sys.argv)

form = Form()

sys.exit(app.exec_())