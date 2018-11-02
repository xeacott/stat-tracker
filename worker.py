# Standard Library
from datetime import datetime

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from nba_api.stats.library import data

from nba_api.stats.endpoints import scoreboardv2

TIMER = 3000

class RefreshGames(QObject, object):

    """Thread and worker object to control updating live game data."""

    def __init__(self, parent):
        super(RefreshGames, self).__init__(parent)

        # Variables to control updating labels
        self.games_started = False
        self.games_initilzed = False

        # Create thread and worker object
        self.parent = parent
        self.thread = QThread()
        self.worker = Worker()

        # Create timer to allow for 30 second refresh
        self.timer = QTimer()
        self.timer.setInterval(TIMER)

        # Set direct connection thread-safe signal
        self.timer.timeout.connect(self.worker.update_live_games)
        self.worker.list_signal.connect(self.refresh_game_data_cb)

        # Move the worker to the thread
        self.timer.moveToThread(self.thread)
        self.worker.moveToThread(self.thread)

        # Connect on-start signal
        self.thread.started.connect(self.timer.start)

        # Start the thread
        self.thread.start()

    def init_game_info(self, boxscore):
        """Initialize all labels to show game information."""

        self.times = []
        self.game_info_list = []
        self.game_score_list = []

        self.total_games = len(boxscore)

        for start_time in range(0, self.total_games):
            self.times.append(boxscore[start_time][4])

        for teams in range(0, self.total_games):
            self.game_info_list.append(boxscore[teams][5][-6:])

        for index in range(0, self.total_games):
            team_info = (self.game_info_list)[index]
            string_slice = int(len(team_info) / 2)
            team_1, team_2 = team_info[:string_slice], team_info[string_slice:]

            game = team_1 + "  |  " + team_2 + ' \n' + self.times[index]
            self.parent.main_window.game_list[index].setText(game)
            self.parent.main_window.statusbar.statusbar.showMessage(
                "Games initialized", 3000
            )

    def update_scoreboard_info(self, scoreboard):
        print("Update games here")



    def refresh_game_data_cb(self, data):
        """Update the game scores on the main window.

        :param data list:
            string that contains game data such as score, quarter, time remaining

        """

        scoreboard = data[0]
        boxscore = data[1]

        del data

        # Initialize all games
        # TODO : move this out of here with a singleShot QTimer
        if not self.games_initilzed:
            self.init_game_info(boxscore)
            self.games_initilzed = True

        # Check if the earliest game has started
        if (boxscore[0][9] == "1") | (boxscore[0][9] != "0"):
            # TODO : Remove the start time, replace with quarter and time remaining
            self.update_scoreboard_info(scoreboard)


class Worker(QObject):

    """Worker to collect live data."""

    list_signal = pyqtSignal([list])

    @pyqtSlot()
    def update_live_games(self):
        """Grab the latest live information based on current date.
        This method is to attempt to collect live information every 30 seconds
        to update the game information in the main window. If the data has not
        changed, do not send signal to update.
        """
        game_info = []
        current_scoreboard_info = None

        exceptions = (ConnectionError, ConnectionRefusedError, TimeoutError)
        date = str(datetime.now().date())
        date = "2018-10-30"
        id = '00'
        try:
            current_scoreboard_info = scoreboardv2.ScoreboardV2(
                day_offset=0,
                game_date=date,
                league_id=id
            )

        except exceptions:
            print("Request failed.")


        game_info.append(current_scoreboard_info.line_score.data['data'])
        game_info.append(current_scoreboard_info.data_sets[0].data['data'])
        self.list_signal.emit(game_info)
