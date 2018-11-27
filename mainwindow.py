# Standard Library
# none

# Third Party Packages
import os
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from nba_api.stats.library import data
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playerprofilev2

# Relative Imports
from draft_table import *
from new_category import *
from new_player import *
from player_search import PlayerEntry
from acc_options_dialog import TrackerSettings
from load_settings import LoadSettings
from menu_status_bars import MenuBar, StatusBar
from restore import Categories, Players, Seasons
from worker import RefreshGames


class MainWindow(QWidget, object):

    """Main window of Stat Tracker.

    MainWindow is parent to menubar and statusbar. Instantiates the main
    objects to be used by Tracker. It is the main window of QApplication.

    """

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent

        self.latest_search = None

        # Menubar / Statusbar
        self.menubar = MenuBar(parent)
        self.statusbar = StatusBar(parent)

        # Create main layout
        hbox = QHBoxLayout()

        # Create game label instances
        self.game_list = [
            QLabel("Game 1"), QLabel("Game 2"), QLabel("Game 3"), QLabel("Game 4"),
            QLabel("Game 5"), QLabel("Game 6"), QLabel("Game 7"), QLabel("Game 8"),
            QLabel("Game 9"), QLabel("Game 10"), QLabel("Game 11"),  QLabel("Game 12"),
            QLabel("Game 13"), QLabel("Game 14")
        ]

        splitter = QSplitter(Qt.Horizontal)

        self.draft_table = self.create_draft_table()
        self.player_chars = self.create_player_characteristics()

        splitter.addWidget(self.draft_table)
        splitter.addWidget(self.player_chars)
        splitter.setStretchFactor(0, 1)
        splitter.setSizes([1000, 450])

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        self.setMinimumSize(1450, 750)

    def create_draft_table(self):
        """Initialize GUI with right side draft table and live games.

        :returns:
            Group box with all widgets placed accordingly.
        :rtype: QGroupBox

        """
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
        """Initialize right side global player search and game log.

        :returns:
            Group box with all widgets placed accordingly.
        :rtype: QGroupBox

        """

        # Create outer group box to store season stats and game log group box
        group_box = QGroupBox("Player Information")
        group_box.setStyleSheet("QGroupBox {font-size: 16px;}")

        # Layout for outer group box
        group_box_vbox = QVBoxLayout()

        # Create two inner group boxes and main vboxes
        self.player_chars_group_box = QGroupBox("Season Averages | {}".format(
            self.parent.restore.current_season
        ))
        vbox_season_stats = QVBoxLayout()

        player_game_log_group_box = QGroupBox("Game Log")
        vbox_game_log = QVBoxLayout()

        # Create season stats layouts for labels
        search_box = QHBoxLayout()
        name_and_number_box = QHBoxLayout()
        team_box = QHBoxLayout()
        career_avg_box = QHBoxLayout()
        info_box = QHBoxLayout()

        # Search bar
        player_search = PlayerEntry(self)
        player_search.setPlaceholderText("Search by last name...")

        # Divider Line
        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.HLine)
        divider_line.setFrameShadow(QFrame.Sunken)

        # Create labels to hold information
        name_style_sheet = ("QLabel {font-size: 16px;}")
        label_style_sheet = ("QLabel {font-size: 14px; font-weight: bold}")

        self.label_player_name = QLabel("Player Number\n Player Name")
        self.label_player_name.setWordWrap(True)
        self.label_player_name.setAlignment(Qt.AlignCenter)
        self.label_player_name.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.label_player_name.setStyleSheet(name_style_sheet)

        self.label_player_team = QLabel("Current Team")
        self.label_player_team.setWordWrap(True)
        self.label_player_team.setAlignment(Qt.AlignCenter)
        self.label_player_team.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.label_player_team.setStyleSheet(name_style_sheet)

        # Add widgets into corresponding horizontal layouts
        search_box.addWidget(player_search, alignment=Qt.AlignCenter)
        name_and_number_box.addWidget(self.label_player_name, alignment=Qt.AlignCenter)
        team_box.addWidget(self.label_player_team, alignment=Qt.AlignCenter)

        # Set the style sheets for each label
        self.player_char_labels = [
            QLabel("PTS"), QLabel("REB"), QLabel("AST"), QLabel("STL"), QLabel("BLK")]

        self.player_char_data = [
            QLabel(""), QLabel(""), QLabel(""), QLabel(""), QLabel("")]

        for item in self.player_char_labels:
            item.setStyleSheet(label_style_sheet)
            career_avg_box.addWidget(item, alignment=Qt.AlignTop | Qt.AlignCenter)

        for item in self.player_char_data:
            info_box.addWidget(item, alignment=Qt.AlignCenter)

        # Insert horizontal layouts into vertical layout
        vbox_season_stats.addItem(search_box)
        vbox_season_stats.addWidget(divider_line)

        vbox_season_stats.addItem(name_and_number_box)
        vbox_season_stats.addItem(QSpacerItem(0, 25))

        vbox_season_stats.addItem(team_box)
        vbox_season_stats.addItem(QSpacerItem(0, 25))

        vbox_season_stats.addItem(career_avg_box)
        vbox_season_stats.addItem(info_box)
        vbox_season_stats.addItem(QSpacerItem(0, 25))

        # Repeat for game log group box
        game_log_categories = QHBoxLayout()
        game_log_data_items = QHBoxLayout()

        # Create labels for game log headers
        self.game_log_list = [
            QLabel("Date"), QLabel("OPP"), QLabel("PTS"), QLabel("REB"),
            QLabel("AST"), QLabel("STL"), QLabel("BLK")]

        # Create labels for game log data
        self.game_log_header = [
            QLabel(""), QLabel(""), QLabel(""), QLabel(""),
            QLabel(""), QLabel(""), QLabel("")]

        # Insert labels into the horizontal box
        game_log_style_sheet = ("QLabel {font-size: 14px; font-weight: bold}")
        for item in self.game_log_list:
            item.setStyleSheet(game_log_style_sheet)
            game_log_categories.addWidget(item, alignment=Qt.AlignTop | Qt.AlignCenter)

        for item in self.game_log_header:
            game_log_data_items.addWidget(item, alignment=Qt.AlignCenter)

        # Insert horizontal box into vertical box
        vbox_game_log.addItem(game_log_categories)
        vbox_game_log.addItem(game_log_data_items)

        # Set vertical layouts in the sub group boxes
        self.player_chars_group_box.setLayout(vbox_season_stats)
        player_game_log_group_box.setLayout(vbox_game_log)

        # Add the group boxes to the main vertical layout
        group_box_vbox.addWidget(self.player_chars_group_box)
        group_box_vbox.addSpacerItem(QSpacerItem(0, 25))
        group_box_vbox.addWidget(player_game_log_group_box)

        # Add season stats main vertical layout into the group box
        group_box.setLayout(group_box_vbox)

        # Signals
        player_search.returnPressed.connect(self.global_player_save_cb)

        return group_box

    # CALLBACKS----------
    def global_player_save_cb(self):
        """Store the active record to be used for refreshing player info."""
        self.latest_search = self.sender().text()
        self.refresh_player_char_data_cb()

    def refresh_player_char_data_cb(self):
        """Handle updating the player information and game log data."""
        text = self.latest_search
        print(text)

        # Test that text is legal
        approved = PlayerEntry.test_text_cb(self, text)
        if approved:
            current_season = self.parent.restore.current_season
            element = self.parent.all_players.last_names.index(text)
            player_id = self.parent.all_players.player_id[element]

            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            season_stats = playerprofilev2.PlayerProfileV2(player_id=player_id)
            game_log = playergamelog.PlayerGameLog(player_id=player_id)

            self.blockSignals(True)

            # ---------------- Set common player info ----------------

            player_name = ("#{}\n{}, {}".format(
                player_info.common_player_info.data['data'][0][13],
                player_info.common_player_info.data['data'][0][3],
                player_info.data_sets[0].data['data'][0][14]
            ))

            player_team = ("{} {}\n{}".format(
                player_info.common_player_info.data['data'][0][20],
                player_info.common_player_info.data['data'][0][17],
                player_info.data_sets[1].data['data'][0][2]
            ))

            self.label_player_name.setText(player_name)
            self.label_player_team.setText(player_team)

            season_averages = []
            for sublist in season_stats.season_totals_regular_season.data['data']:
                if current_season in sublist[1]:
                    total_games = sublist[6]
                    points = round((sublist[26] / total_games), 1)
                    rebounds = round((sublist[20] / total_games), 1)
                    assists = round((sublist[21] / total_games), 1)
                    steals = round((sublist[22] / total_games), 1)
                    blocks = round((sublist[23] / total_games), 1)

                    season_averages.append(str(points))
                    season_averages.append(str(rebounds))
                    season_averages.append(str(assists))
                    season_averages.append(str(steals))
                    season_averages.append(str(blocks))

            for data, item in zip(season_averages, self.player_char_data):
                item.setAlignment(Qt.AlignCenter)
                item.setText(data)

            # ---------------- Set Game Log Info ----------------

            game_log_lists = [[] for x in range(7)]

            # Set game log info for the latest 5 games
            for game in range(0, 5):
                game_log_lists[0].append(str(game_log.data_sets[0].data['data'][game][3][0:6]))
                game_log_lists[1].append(str(game_log.data_sets[0].data['data'][game][4][-3:]))
                game_log_lists[2].append(str(game_log.data_sets[0].data['data'][game][24]))
                game_log_lists[3].append(str(game_log.data_sets[0].data['data'][game][18]))
                game_log_lists[4].append(str(game_log.data_sets[0].data['data'][game][19]))
                game_log_lists[5].append(str(game_log.data_sets[0].data['data'][game][20]))
                game_log_lists[6].append(str(game_log.data_sets[0].data['data'][game][21]))

            # Unpack lists and create strings to set the label text
            for section, label_data in zip(game_log_lists, self.game_log_header):
                text = ''
                for value in section:
                    text += ("{}\n\n\n".format(value))
                label_data.setAlignment(Qt.AlignCenter)
                label_data.setText(text)

            self.blockSignals(False)

            del player_info
            del season_stats
            del game_log

    def refresh_season_cb(self):
        """Refresh the GUI to reflect the change in season requested."""
        title = ("Season Averages | {}".format(self.parent.restore.current_season))
        self.player_chars_group_box.setTitle(title)

        legal_player = isinstance(self.latest_search, type(None))
        if not legal_player & self.parent.tracker_settings.year_changed:
            self.refresh_player_char_data_cb()


class Tracker(QMainWindow, object):

    """Display main window of CIP Object Explorer.

    This is the entry point for control of Explorer. This class handles
    reading the cached settings and properly restoring the state of GUI from
    last termination.

    """

    EXIT_CODE_RESTART = -1073740940

    def __init__(self, parent=None):
        super(Tracker, self).__init__(parent)
        favicon = QIcon()
        self.setWindowIcon(favicon)
        self.setWindowTitle("NBA Stat Tracker")

        self.restore = LoadSettings(self)

        self.category_cache = CategoryDialogSettings()
        self.player_cache = PlayerDialogSettings()
        self.all_seasons = Seasons()
        self.all_categories = Categories(self)
        self.all_players = Players(self)

        self.tracker_settings = TrackerSettings(self.restore)

        self.main_window = MainWindow(self)
        self.worker = RefreshGames(self)
        self.setCentralWidget(self.main_window)

    # CALLBACKS----------
    def on_start(self):
        """Closure for main application launch to check if application must be loaded with a theme."""
        if self.tracker_settings.night_mode:
            qApp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def quit_cb(self):
        """Exit the application and do not save state."""
        qApp.quit()

    @pyqtSlot()
    def restart_cb(self):
        """Terminate CipExplorer application.

        Cleanup activities related to termination of the application are
        located here.

        :param signal quit_signal:
            Quit signal.

        """
        qDebug("Performing application reboot...")
        qApp.exit(self.EXIT_CODE_RESTART)

