# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from nba_api.stats.library import data
from nba_api.stats.endpoints import commonplayerinfo

# Relative Imports
from new_category import *
from new_player import *
from menu_status_bars import *
from restore import *


class PlayerEntry(QLineEdit, object):

    """Line edit to support auto-complete and other various methods needed for players."""

    def __init__(self, parent):
        super(PlayerEntry, self).__init__(parent)
        self.parent = parent

        list = []
        self.completer = QCompleter()
        self.setCompleter(self.completer)

        try:
            list = self.parent.all_players.last_names
        except AttributeError:
            list = parent.parent.all_players.last_names

        my_completer = QCompleter(list)
        my_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(my_completer)

    @staticmethod
    def test_text_cb(self, player):
        approved = True
        try:
            if not player in self.all_players.last_names:
                QMessageBox.about(self,
                                  'Notice!',
                                  'Player not loaded, please try again.')
                approved = False
        except AttributeError:
            if not player in self.parent.all_players.last_names:
                QMessageBox.about(self,
                                  'Notice!',
                                  'Player not loaded, please try again.')
                approved = False
        return approved