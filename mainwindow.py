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

        # Create game label instances
        self.game_list = [
            QLabel("Game 1"),
            QLabel("Game 2"),
            QLabel("Game 3"),
            QLabel("Game 4"),
            QLabel("Game 5"),
            QLabel("Game 6"),
            QLabel("Game 7"),
            QLabel("Game 8"),
            QLabel("Game 9"),
            QLabel("Game 10"),
            QLabel("Game 11"),
            QLabel("Game 12"),
            QLabel("Game 13"),
            QLabel("Game 14")
        ]

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

        label_style_sheet = ("QLabel {font-size: 14px;}")

        for game in range(0, len(self.game_list)):
            self.game_list[game].setStyleSheet(label_style_sheet)
            self.game_list[game].setWordWrap(True)
            if game < 7:
                game_set_one.addWidget(self.game_list[game], alignment=Qt.AlignLeft)
            else:
                game_set_two.addWidget(self.game_list[game], alignment=Qt.AlignLeft)

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
        team_box = QHBoxLayout()
        career_avg_box = QHBoxLayout()
        info_box = QHBoxLayout()

        # Search bar
        player_search = PlayerSearch(self)
        player_search.setPlaceholderText("Search...")

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.HLine)
        divider_line.setFrameShadow(QFrame.Sunken)

        # Right side player information
        label_style_sheet = ("QLabel {font-size: 14px;}")
        name_style_sheet = ("QLabel {font-size: 16px;}")

        self.label_player_name = QLabel("Player number and name")
        self.label_player_name.setWordWrap(True)
        self.label_player_name.setAlignment(Qt.AlignCenter)
        self.label_player_name.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.label_player_name.setStyleSheet(name_style_sheet)

        self.label_player_team = QLabel("Team")
        self.label_player_team.setWordWrap(True)
        self.label_player_team.setAlignment(Qt.AlignCenter)
        self.label_player_team.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.label_player_team.setStyleSheet(name_style_sheet)

        self.label_pts = QLabel("PTS")
        self.label_pts.setStyleSheet(label_style_sheet)

        self.label_reb = QLabel("REB")
        self.label_reb.setStyleSheet(label_style_sheet)

        self.label_ast = QLabel("AST")
        self.label_ast.setStyleSheet(label_style_sheet)

        self.label_pie = QLabel("PIE")
        self.label_pie.setStyleSheet(label_style_sheet)

        self.label_ht = QLabel("HT")
        self.label_ht.setStyleSheet(label_style_sheet)

        self.label_wt = QLabel("WT")
        self.label_wt.setStyleSheet(label_style_sheet)

        self.label_born = QLabel("Born")
        self.label_born.setStyleSheet(label_style_sheet)


        # Add widgets into horizontal layouts
        search_box.addWidget(player_search, alignment=Qt.AlignCenter)

        name_and_number_box.addWidget(self.label_player_name, alignment=Qt.AlignCenter)

        team_box.addWidget(self.label_player_team, alignment=Qt.AlignCenter)

        career_avg_box.addWidget(self.label_pts, alignment=Qt.AlignTop)
        career_avg_box.addWidget(self.label_reb, alignment=Qt.AlignTop)
        career_avg_box.addWidget(self.label_ast, alignment=Qt.AlignTop)
        career_avg_box.addWidget(self.label_pie, alignment=Qt.AlignTop)

        info_box.addWidget(self.label_ht, alignment=Qt.AlignTop)
        info_box.addWidget(self.label_wt, alignment=Qt.AlignTop)
        info_box.addWidget(self.label_born, alignment=Qt.AlignTop)

        # Add horizontal layouts into grid layout
        grid_layout.addItem(search_box)
        grid_layout.addWidget(divider_line)

        grid_layout.addItem(name_and_number_box)
        grid_layout.addItem(QSpacerItem(0, 50))

        grid_layout.addItem(team_box)
        grid_layout.addItem(QSpacerItem(0, 100))

        grid_layout.addItem(career_avg_box)
        grid_layout.addItem(info_box)
        grid_layout.addItem(QSpacerItem(0, 100))

        group_box.setLayout(grid_layout)

        # Signals
        player_search.editingFinished.connect(self.refresh_data_cb)

        return group_box

    # CALLBACKS----------
    def refresh_data_cb(self):
        """Handle updating the player information section."""

        player_id = None
        text = self.sender().text()

        if text in self.parent.all_players.abv_player_list:
            element = self.parent.all_players.abv_player_list.index(text)
            player_id = self.parent.all_players.player_id[element]

        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

        self.blockSignals(True)
        self.label_player_name.setText("# " + player_info.common_player_info.data['data'][0][13] +
                                       "\n" + player_info.common_player_info.data['data'][0][3])
        self.label_player_team.setText(player_info.common_player_info.data['data'][0][20] + " " +
                                       player_info.common_player_info.data['data'][0][17] + "\n"+
                                       player_info.data_sets[1].data['data'][0][2])
        self.label_pts.setText("PTS \n" + str(player_info.data_sets[1].data['data'][0][3]))
        self.label_reb.setText("REB \n" + str(player_info.data_sets[1].data['data'][0][5]))
        self.label_ast.setText("AST \n" + str(player_info.data_sets[1].data['data'][0][4]))
        self.label_pie.setText("PIE \n" + str(player_info.data_sets[1].data['data'][0][6]))

        self.label_ht.setText("HT \n" + str(player_info.common_player_info.data['data'][0][10]))
        self.label_wt.setText("WT \n" + str(player_info.common_player_info.data['data'][0][11]))
        self.label_born.setText("Born \n" +  str(player_info.common_player_info.data['data'][0][6][0:10]))
        self.blockSignals(False)


class PlayerSearch(QLineEdit, object):

    """Line edit to support auto-complete and other various methods needed for players."""

    def __init__(self, parent):
        super(PlayerSearch, self).__init__(parent)
        self.parent = parent

        list = []
        self.completer = QCompleter()
        self.setCompleter(self.completer)

        try:
            list = self.parent.parent.all_players.abv_player_list
        except AttributeError:
            pass

        my_completer = QCompleter(list)
        my_completer.setCaseSensitivity(1)
        self.setCompleter(my_completer)


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
