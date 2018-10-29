from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTimer
import time

TIMER = 30000

class RefreshGames(QObject, object):

    """Thread and worker object to control updating live game data."""

    def __init__(self, parent):
        super(RefreshGames, self).__init__(parent)

        # Create thread and worker object
        self.parent = parent
        self.thread = QThread()
        self.worker = Worker()

        # Create timer to allow for 30 second refresh
        self.timer = QTimer()
        self.timer.setInterval(TIMER)

        # Set direct connection thread-safe signal
        self.timer.timeout.connect(self.worker.update_live_games)
        self.worker.str_signal.connect(self.refresh_game_data_cb)

        # Move the worker to the thread
        self.timer.moveToThread(self.thread)
        self.worker.moveToThread(self.thread)

        # Connect on-start signal
        self.thread.started.connect(self.timer.start)

        # Start the thread
        self.thread.start()

    def refresh_game_data_cb(self, data):
        """Update the game scores on the main window.

        :param data str:
            string that contains game data such as score, quarter, time remaining

        """

        if not self.parent.main_window.go_live_button.text() == data:
            self.parent.main_window.go_live_button.setText("{}".format(data))
        else:
            self.parent.main_window.go_live_button.setText("Test")

class Worker(QObject):

    """Worker to collect live data."""

    str_signal = pyqtSignal([str])

    @pyqtSlot()
    def update_live_games(self):
        """Grab the latest live information based on current date.

        This method is to attempt to collect live information every 30 seconds
        to update the game information in the main window. If the data has not
        changed, do not send signal to update.
        """

        i = str("100000")
        print("Hit this")
        self.str_signal.emit(i)