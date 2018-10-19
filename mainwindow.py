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


class MainWindow(QWidget, object):

    """Main window of Stat Tracker.

    MainWindow is parent to menubar and statusbar. Instantiates the main
    objects to be used by Tracker. It is the main window of QApplication.

    """

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent

        # Menubar / Statusbar
        self.menubar = MenuBar(parent)
        self.statusbar = StatusBar(parent)

        # Create main layout
        hbox = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.create_draft_table())
        splitter.addWidget(self.create_player_characteristics())
        splitter.setStretchFactor(0, 1)
        splitter.setSizes([1200, 250])

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        self.setMinimumSize(1450, 750)

    def create_draft_table(self):
        group_box = QGroupBox("&Draft Table")
        group_box.setStyleSheet("QGroupBox {  border: 4px solid gray;}")

        # Left side Table Widget and Button
        self.table_widget = DataTable(self.parent)
        table_size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.table_widget.setSizePolicy(table_size_policy)

        go_live_button = QPushButton("Go Live!")
        go_live_button.setToolTip("Allow for live stats to update.")
        go_live_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        go_live_button.setSizePolicy(go_live_policy)

        draft_table_layout = QVBoxLayout()

        draft_table_layout.addWidget(self.table_widget)
        draft_table_layout.addSpacerItem(QSpacerItem(0, 50))
        draft_table_layout.addWidget(go_live_button, alignment=Qt.AlignCenter)

        group_box.setLayout(draft_table_layout)

        # Set signals
        go_live_button.clicked.connect(self.go_live_cb)

        return group_box

    def create_player_characteristics(self):
        group_box = QGroupBox("Player Information")
        group_box.setStyleSheet("QGroupBox {  border: 4px solid gray;}")
        grid_layout = QGridLayout()

        search_box = QHBoxLayout()
        name_and_number_box = QHBoxLayout()
        career_avg_box = QHBoxLayout()
        info_box = QHBoxLayout()

        # Search bar
        player_search = PlayerEntry(self)
        player_search.setPlaceholderText("Search...")

        # Hold player names and IDs
        self.players = []
        for name in data.players:
            self.players.append(name)

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.HLine)
        divider_line.setFrameShadow(QFrame.Sunken)

        # Right side player information
        label_player_name = QLabel("Number and Name")
        label_pts = QLabel("PTS")
        label_reb = QLabel("REB")
        label_ast = QLabel("AST")
        label_pie = QLabel("PIE")

        label_ht = QLabel("HT")
        label_wt = QLabel("WT")
        label_age = QLabel("Age")
        label_born = QLabel("Born")

        # Add widgets into horizontal layouts
        search_box.addWidget(player_search, alignment=Qt.AlignCenter)

        name_and_number_box.addWidget(label_player_name, alignment=Qt.AlignCenter)

        career_avg_box.addWidget(label_pts, alignment=Qt.AlignTop)
        career_avg_box.addWidget(label_reb, alignment=Qt.AlignTop)
        career_avg_box.addWidget(label_ast, alignment=Qt.AlignTop)
        career_avg_box.addWidget(label_pie, alignment=Qt.AlignTop)

        info_box.addWidget(label_ht, alignment=Qt.AlignTop)
        info_box.addWidget(label_wt, alignment=Qt.AlignTop)
        info_box.addWidget(label_age, alignment=Qt.AlignTop)
        info_box.addWidget(label_born, alignment=Qt.AlignTop)

        # Add horizontal layouts into grid layout
        grid_layout.addItem(search_box)
        grid_layout.addWidget(divider_line)

        grid_layout.addItem(name_and_number_box)
        grid_layout.addItem(QSpacerItem(0, 100))

        grid_layout.addItem(career_avg_box)
        grid_layout.addItem(info_box)
        grid_layout.addItem(QSpacerItem(0, 100))

        group_box.setLayout(grid_layout)

        # Signals
        player_search.textChanged.connect(self.refresh_data_cb)

        return group_box

    # CALLBACKS----------
    def go_live_cb(self):
        """Handle updating the table with live data."""
        print('Go live!')

    def refresh_data_cb(self):
        """Handle updating the player information section."""
        sender = self.sender()

        for sublist in self.players:
            if sublist[3] == sender.text():
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=sublist[0])
                print(player_info)


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
        self.setColumnCount(10)
        self.setCornerButtonEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setDefaultAlignment(Qt.AlignCenter)
        self.horizontal_header.setSectionsMovable(True)
        # Fix this
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents & QHeaderView.Stretch)

        self.vertical_header = self.verticalHeader()
        self.vertical_header.setDefaultAlignment(Qt.AlignCenter)
        self.vertical_header.setSectionsMovable(True)
        self.vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        for index in range(self.columnCount()):
            header = QTableWidgetItem()
            header.setText("Category {}".format(index + 1))
            self.setHorizontalHeaderItem(index, header)

        for index in range(self.rowCount()):
            header = QTableWidgetItem()
            header.setText("Player {}".format(index + 1))
            self.setVerticalHeaderItem(index, header)

        # Signals
        self.horizontal_header.sectionDoubleClicked.connect(self.set_horizontal_headers)
        self.vertical_header.sectionDoubleClicked.connect(self.set_vertical_headers)
        self.completed[str].connect(self.display_data)


    def set_horizontal_headers(self):
        """Set the horizontal headers, user requested.

        :param list headers:
            List of categories user wishes to see.

        """
        header = QTableWidgetItem()
        accepted = CategoryDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.category_cache.category)
            header.setTextAlignment(Qt.TextWordWrap)
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
            header.setTextAlignment(Qt.TextWordWrap)
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
        # self.all_categories = Categories(self)
        # self.all_players = Players(self)

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
