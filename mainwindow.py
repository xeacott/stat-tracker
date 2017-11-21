# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Relative Imports
from new_category import *
from new_player import *
from menu_status_bars import *
from restore import *


class MainWindow(QWidget, object):

    """Main window of Stat Tracker.

    MainWindow is parent to menubar and statusbar. Instantiates the main
    objects to be used by Tracker. It is the main window of QApplication.

    """

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent  # parent is CipExplorer

        # Menubar / Statusbar
        self.menubar = MenuBar(parent)
        self.statusbar = StatusBar(parent)

        # Declare layouts
        layout = QHBoxLayout()
        middle_table = QVBoxLayout()

        # Center Table Widget and Buttons
        self.table_widget = DataTable(self.parent)

        go_live_button = QPushButton("Go Live!")
        go_live_button.setToolTip("Allow for live stats to update.")
        go_live_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        go_live_button.setSizePolicy(go_live_policy)

        middle_table.addWidget(go_live_button, alignment=Qt.AlignCenter)
        middle_table.addSpacerItem(QSpacerItem(0, 25))
        middle_table.addWidget(self.table_widget)

        # Set layouts
        layout.addLayout(middle_table)

        # Set signals
        go_live_button.clicked.connect(self.go_live_cb)

        self.setLayout(layout)
        self.setMinimumSize(950, 450)

    # CALLBACKS----------
    def go_live_cb(self):
        """Handle updating the table with live data."""
        print('Go live!')


class DataTable(QTableWidget, object):

    """Give user a nice way to view the information requested."""

    completed = pyqtSignal(str)

    def __init__(self, parent):
        super(DataTable, self).__init__(parent)
        self.parent = parent

        self.wordWrap()
        self.setRowCount(10)
        self.setColumnCount(10)
        self.setCornerButtonEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

        self.vertical_header = self.verticalHeader()
        self.vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        # Signals
        self.horizontal_header.sectionDoubleClicked.connect(self.set_horizontal_headers)
        self.vertical_header.sectionDoubleClicked.connect(self.set_vertical_headers)
        self.completed[str].connect(self.display_data)


    def set_horizontal_headers(self, i):
        """Set the horizontal headers, user requested.

        :param list headers:
            List of categories user wishes to see.

        """
        i = self.currentColumn()
        header = QTableWidgetItem()
        accepted = CategoryDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.category_cache.category)
            self.setHorizontalHeaderItem(i, header)
            self.completed.emit('category')

    def set_vertical_headers(self, i):
        """Set the vertical headers, user requested.

        :param list headers:
            List of players user wishes to see.

        """
        i = self.currentRow()
        header = QTableWidgetItem()
        accepted = PlayerDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.player_cache.player)
            self.setVerticalHeaderItem(i, header)
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
        stat = None
        player_id = None
        category = []

        count = self.columnCount()
        for i in range(count):
            try:
                name = self.horizontalHeaderItem(i).text()
            except AttributeError:
                print('The header was empty, so dont display anything.')
                name = None
            try:
                player_id = self.verticalHeaderItem(i).text()
            except AttributeError:
                print('The header was empty, so dont display anything.')
            category.append(name)

        if text == 'player':
            player_id = self.parent.all_players.player_and_id_dict[player_id]
            player_stats = self.parent.all_players.get_player_stats(player_id)
            for item in category:
                if item in player_stats:
                    print(player_stats[item])
                    # data is (player_stats[item]) so put it in the right row
            # find the column where item came from


class Tracker(QMainWindow, object):

    """Display main window of CIP Object Explorer.

    This is the entry point for control of Explorer. This class handles
    reading the cached settings and properly restoring the state of GUI from
    last termination.

    """

    def __init__(self, parent=None):
        super(Tracker, self).__init__(parent)
        favicon = QIcon()
        self.setWindowIcon(favicon)
        self.setWindowTitle("NBA Stat Tracker")

        self.category_cache = CategoryDialogSettings()
        self.player_cache = PlayerDialogSettings()
        self.all_categories = Categories(self)
        self.all_players = Players(self)

        self.main_window = MainWindow(self)
        self.setCentralWidget(self.main_window)

    # CALLBACKS----------
    def on_start(self):
        print('on start')

    def quit_cb(self, quit_signal):
        """Terminate CipExplorer application.

        Cleanup activities related to termination of the application are
        located here.

        :param signal quit_signal:
            Quit signal.

        """
        self.close()
