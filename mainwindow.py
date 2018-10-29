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
from draft_table import *
from new_category import *
from new_player import *
from menu_status_bars import MenuBar, StatusBar
from restore import Categories, Players
from worker import RefreshGames


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

        self.draft_table = self.create_draft_table()
        self.player_chars = self.create_player_characteristics()
        splitter.addWidget(self.draft_table)
        splitter.addWidget(self.player_chars)
        splitter.setStretchFactor(0, 1)
        splitter.setSizes([1200, 250])

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        self.setMinimumSize(1450, 750)

    def create_draft_table(self):
        group_box = QGroupBox("Draft Table")
        group_box.setStyleSheet("QGroupBox {font-size: 16px;}")

        # Left side Table Widget and Button
        self.table_widget = DataTable(self.parent)
        table_size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.table_widget.setSizePolicy(table_size_policy)

        draft_table_layout = QVBoxLayout()
        game_set_one = QHBoxLayout()
        game_set_two = QHBoxLayout()

        game1 = QLabel("Game 1")
        game2 = QLabel("Game 2")
        game3 = QLabel("Game 3")
        game4 = QLabel("Game 4")
        game5 = QLabel("Game 5")
        game6 = QLabel("Game 6")

        game7 = QLabel("Game 7")
        game8 = QLabel("Game 8")
        game9 = QLabel("Game 9")
        game10 = QLabel("Game 10")
        game11 = QLabel("Game 11")
        game12 = QLabel("Game 12")

        game_set_one.addWidget(game1, alignment=Qt.AlignCenter)
        game_set_one.addWidget(game2, alignment=Qt.AlignCenter)
        game_set_one.addWidget(game3, alignment=Qt.AlignCenter)
        game_set_one.addWidget(game4, alignment=Qt.AlignCenter)
        game_set_one.addWidget(game5, alignment=Qt.AlignCenter)
        game_set_one.addWidget(game6, alignment=Qt.AlignCenter)

        game_set_two.addWidget(game7, alignment=Qt.AlignCenter)
        game_set_two.addWidget(game8, alignment=Qt.AlignCenter)
        game_set_two.addWidget(game9, alignment=Qt.AlignCenter)
        game_set_two.addWidget(game10, alignment=Qt.AlignCenter)
        game_set_two.addWidget(game11, alignment=Qt.AlignCenter)
        game_set_two.addWidget(game12, alignment=Qt.AlignCenter)

        draft_table_layout.addWidget(self.table_widget)
        draft_table_layout.addSpacerItem(QSpacerItem(0, 20))
        draft_table_layout.addLayout(game_set_one)
        draft_table_layout.addSpacerItem(QSpacerItem(0, 35))
        draft_table_layout.addLayout(game_set_two)
        draft_table_layout.addSpacerItem(QSpacerItem(0, 35))

        group_box.setLayout(draft_table_layout)

        return group_box

    def create_player_characteristics(self):
        group_box = QGroupBox("Player Information")
        group_box.setStyleSheet("QGroupBox {font-size: 16px;}")
        grid_layout = QGridLayout()

        search_box = QHBoxLayout()
        name_and_number_box = QHBoxLayout()
        career_avg_box = QHBoxLayout()
        info_box = QHBoxLayout()

        # Search bar
        player_search = PlayerEntry(self)
        player_search.setPlaceholderText("Search...")

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
    def refresh_data_cb(self):
        """Handle updating the player information section."""
        sender = self.sender()

        for sublist in self.players:
            if sublist[3] == sender.text():
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=sublist[0])
                print(player_info)


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
        self.worker = RefreshGames(self)
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
