# Standard Library
# none

# Third Party Packages
import os
import operator
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

        self.last_sort_by = "Dec"
        self.last_category_sorted = None

        self.setWordWrap(True)
        self.setRowCount(13)
        self.setColumnCount(20)
        self.setCornerButtonEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setToolTip("Double click to change...")
        self.horizontal_header.setDefaultAlignment(Qt.AlignCenter)
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)
        self.horizontal_header.setSectionsMovable(True)
        self.horizontal_header.setDefaultSectionSize(50)
        self.horizontal_header.setContextMenuPolicy(Qt.CustomContextMenu)

        self.vertical_header = self.verticalHeader()
        self.vertical_header.setToolTip("Double click to change...")
        self.vertical_header.setDefaultAlignment(Qt.AlignCenter)
        self.vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        self.vertical_header.setSectionsMovable(True)
        self.vertical_header.setDefaultSectionSize(75)
        self.vertical_header.setContextMenuPolicy(Qt.CustomContextMenu)

        # Signals
        self.horizontal_header.customContextMenuRequested.connect(self.show_menu)
        self.vertical_header.customContextMenuRequested.connect(self.show_menu)

        # Sort
        # self.horizontal_header.sectionClicked.connect(self.sort_items)

        self.horizontal_header.sectionDoubleClicked.connect(self.set_horizontal_headers)
        self.vertical_header.sectionDoubleClicked.connect(self.set_vertical_headers)
        self.completed[str].connect(self.display_data)

        self.set_default_categories()
        self.set_default_players()

    # CALLBACKS
    # def sort_items(self):
    #     """Sort items in the user requested column."""
    #
    #     stat_name_dict = {}
    #     output_dict = {}
    #     category_list = []
    #     current_column = self.currentColumn()
    #     category_to_sort = self.horizontalHeaderItem(current_column).text()
    #
    #     # If the user hasn't sorted a category before, set it to the requested one
    #     if self.last_category_sorted is None:
    #         category_to_sort = self.last_category_sorted
    #
    #     # Retrieve players with loaded categories
    #     for row in range(0, self.rowCount()):
    #         stat_line = []
    #         current_name = str(self.verticalHeaderItem(row).text())
    #         if not current_name.find("Player") != -1:
    #             for column in range(0, self.columnCount()):
    #
    #                 # While we are here build a list of the categories
    #                 current_category = str(self.horizontalHeaderItem(column).text())
    #                 category_list.append(current_category)
    #
    #                 # Test if the stat is loaded or not
    #                 try:
    #                     if self.item(row, column).text():
    #                         stat_line.append(int(self.item(row, column).text()))
    #
    #                 # Pad the list
    #                 except AttributeError:
    #                     stat_line.append(0)
    #
    #             # Create a dictionary to store each stat line associated with a single player
    #             stat_name_dict[current_name] = stat_line
    #
    #     if self.last_sort_by == "Dec":
    #         output_dict = dict(sorted(stat_name_dict.items(), key=lambda x: x[1][current_column]))
    #         self.last_sort_by = "Asc"
    #
    #     else:
    #         output_dict = dict(sorted(stat_name_dict.items(), key=lambda x: x[1][current_column], reverse=True))
    #         self.last_sort_by = "Dec"
    #
    #     # Wipe all the information in the table before re-populating it
    #     self.clear()
    #
    #     row_index = 0
    #     for key, value in output_dict.items():
    #         header = QTableWidgetItem()
    #         header.setText(key)
    #         self.setVerticalHeaderItem(row_index, header)
    #         for sorted_column in range(0, self.columnCount()):
    #             if value[sorted_column] == 0:
    #                 pass
    #             else:
    #                 stat = QTableWidgetItem()
    #                 stat.setText(str(value[sorted_column]))
    #                 self.setItem(row_index, sorted_column, stat)
    #         row_index  = row_index + 1
    #
    #     # Back-fill the remaining empty information with the defaults
    #     unused_players = (1 + len(output_dict))
    #     self.set_default_players(unused_players)
    #     self.set_default_categories(category_list)


    def show_menu(self, pos):
        """Pop up menu to clear selection of specified header.

        :param int pos:
            Integer representation of header.

        """
        menu = QMenu()
        clear_action = menu.addAction("Clear Selection", self.clearSelection)
        action = menu.exec_(self.mapToGlobal(pos))

        if action == clear_action:
            self.clear_selection(self.sender().orientation(),
                                 self.sender().logicalIndexAt(pos))

    def clear_selection(self, orientation, header_num):
        """Reset the requested header to default value.

        :param int orientation:
            Specifies if requested is a row or column.

        :param int header_num:
            Specifies the position of the header relative to the row or column.

        """
        header = QTableWidgetItem()

        if orientation == 1:
            header.setText("Category {}".format(header_num + 1))
            self.setHorizontalHeaderItem(header_num, header)
        else:
            header.setText("Player {}".format(header_num + 1))
            self.setVerticalHeaderItem(header_num, header)

    def set_default_categories(self, category_list=None):
        """Set the default values for horizontal headers.

        :param list category_list:
            Used to back fill unused category slots if a user performs a sort.

        """
        if not category_list:
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

        else:
            for index in range(self.columnCount()):
                header = QTableWidgetItem()
                header.setText(category_list[index])
                self.setHorizontalHeaderItem(index, header)


    def set_default_players(self, unused_players=None):
        """Set the default values for vertical headers.

        :param int unused_players:
            Used to back fill unused player slots if a user performs a sort.

        """

        start_count = 0

        if unused_players:
            start_count = unused_players - 1

        for index in range(start_count, self.rowCount()):
            header = QTableWidgetItem()
            header.setText("Player {}".format(index + 1))
            self.setVerticalHeaderItem(index, header)

    def set_horizontal_headers(self):
        """Set the horizontal headers, user requested."""
        header = QTableWidgetItem()
        accepted = CategoryDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.category_cache.category)
            self.setHorizontalHeaderItem(self.currentColumn(), header)
            self.completed.emit('category')

    def set_vertical_headers(self):
        """Set the vertical headers, user requested."""
        header = QTableWidgetItem()
        accepted = PlayerDialog.get_settings(self.parent)
        if accepted:
            text = self.parent.player_cache.player
            last, first = text.split(',')
            header.setText("{}\n{}".format(first.strip(), last.strip()))
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