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


class DataTable(QTableWidget, object):

    """Give user a nice way to view the information requested."""

    completed = pyqtSignal(str)

    def __init__(self, parent):
        super(DataTable, self).__init__(parent)
        self.parent = parent

        self.stat = None
        self.player_id = None

        self.setWordWrap(True)
        self.setRowCount(10)
        self.setColumnCount(20)
        self.setCornerButtonEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setDefaultAlignment(Qt.AlignCenter)
        self.horizontal_header.setSectionsMovable(True)
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)

        self.vertical_header = self.verticalHeader()
        self.vertical_header.setDefaultAlignment(Qt.AlignCenter)
        self.vertical_header.setSectionsMovable(True)
        self.vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        # Signals
        self.horizontal_header.sectionDoubleClicked.connect(self.set_horizontal_headers)
        self.vertical_header.sectionDoubleClicked.connect(self.set_vertical_headers)
        self.completed[str].connect(self.display_data)

        self.set_default_categories()
        self.set_default_players()

    def set_default_categories(self):
        """Set the default values for horizontal headers."""
        for index in range(self.columnCount()):
            header = QTableWidgetItem()
            if index == 0:
                header.setText("PTS")

            if index == 1:
                header.setText("AST")

            if index == 2:
                header.setText("REB")

            elif index > 2:
                header.setText("Category {}".format(index + 1))

            self.setHorizontalHeaderItem(index, header)

    def set_default_players(self):
        """Set the default values for vertical headers."""
        for index in range(self.rowCount()):
            header = QTableWidgetItem()
            header.setText("Player {}".format(index + 1))
            self.setVerticalHeaderItem(index, header)


    def set_horizontal_headers(self):
        """Set the horizontal headers, user requested.

        :param list headers:
            List of categories user wishes to see.

        """
        header = QTableWidgetItem()
        accepted = CategoryDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.category_cache.category)
            self.setHorizontalHeaderItem(self.currentColumn(), header)
            self.completed.emit('category')

    def set_vertical_headers(self):
        """Set the vertical headers, user requested.

        :param list headers:
            List of players user wishes to see.

        """
        header = QTableWidgetItem()
        accepted = PlayerDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.player_cache.player)
            self.setVerticalHeaderItem(self.currentRow(), header)
            self.completed.emit('player')

    def display_data(self, text):
        """Update cell according to user input.

        Handles updating all data for each player and category requested.
        If the sender is a category, scan the list of currently active players, and
        for each of the categories specified, then list that data. If the sender is
        a player, scan the list of currently active categories and apply them to the
        player.

        :param str text:
            Position of header that changed, vertical or horizontal.

        """
        category = []
        col_count = self.columnCount()
        for i in range(col_count):
            try:
                name = self.horizontalHeaderItem(i).text()
            except AttributeError:
                name = None
            category.append(name)

        player = []
        row_count = self.rowCount()
        for i in range(row_count):
            try:
                player_id = self.verticalHeaderItem(i).text()
            except AttributeError:
                player_id = None
            player.append(player_id)

        if text == 'player':
            for id_of_player in player:
                try:
                    self.player_id = self.parent.all_players.player_and_id_dict[id_of_player]
                except Exception:
                    print('Break here')
                else:
                    player_object = RetrievePlayer(self.parent)
                    # TODO finished signal not going off
                    for column, item in enumerate(category, start=0):
                        if item in player_object:
                            item = str(player_object[item])
                            self.setItem(self.currentRow(), column, QTableWidgetItem(item))