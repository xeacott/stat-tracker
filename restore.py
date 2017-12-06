# Standard Library

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# NBA Package
from nba_py import constants, team, player

"""
    restore file to be the entire model for which player and category data will be filed.

"""

class Categories(object):

    """Spawns a worker and thread to get a list of categories for a user."""

    def __init__(self, parent):
        super(Categories, self).__init__()
        self.parent = parent

        self.list = ['MIN',
                     'FGM',
                     'FGA',
                     'FG_PCT',
                     'FG3M',
                     'FG3A',
                     'FG3_PCT',
                     'FTM',
                     'FTA',
                     'FT_PCT',
                     'OREB',
                     'DREB',
                     'REB',
                     'AST',
                     'STL',
                     'BLK',
                     'TOV',
                     'PF',
                     'PTS']


class Players(object):

    """Spawns a worker and thread to get a list of players for a user."""

    def __init__(self, parent):
        super(Players, self).__init__()
        self.parent = parent

        self.current_season = constants.CURRENT_SEASON

        self.team_ids = []
        self.player_list = []
        self.player_id = []
        self.player_and_id_dict = []
        self.stat_category = range(8, 27)
        self.get_all_team_ids(team.TEAMS)
        self.full_player_list()

    def get_all_team_ids(self, nested):
        """Get a complete list of all available team IDs for the current season.

        :param dict nested:
            Contains a dict of teams' data

        """
        for teams, ids in nested.items():
            if isinstance(ids, dict):
                id = ids.get('id')
                self.team_ids.append(id)

    def full_player_list(self):
        """Get a complete list of all players and their associated player ID."""
        for specific_team_id in self.team_ids:
            team_roster = team.TeamCommonRoster(specific_team_id, self.current_season)
            team_size = len(team_roster.json['resultSets'][0]['rowSet']) - 1
            for i in range(team_size):
                player = team_roster.json['resultSets'][0]['rowSet'][i][3]
                player_id = team_roster.json['resultSets'][0]['rowSet'][i][12]
                self.player_list.append(player)
                self.player_id.append(player_id)
                self.player_and_id_dict = dict(zip(self.player_list, self.player_id))


class RetrievePlayer(QObject, object):

    """Spawn a thread and worker to retrieve player information."""

    def __init__(self, parent):
        super(RetrievePlayer, self).__init__()

        self.parent = parent
        self.thread = QThread()
        self.worker = WorkerObject(self.parent)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.get_player_stats)
        self.worker.finished.connect(self.clean_up)
        self.thread.start()


    # NOT GETTING HIT
    def clean_up(self):
        print('Quitting thread')

        self.thread.quit()


class WorkerObject(QObject, object):

    """Worker to get player data.

    This object is pushed onto a thread. When finished, a signal is emitted back to the
    thread letting it know to close gracefully. If the channel creation errors out the
    exception is caught and printed to the python console.

    """

    finished = pyqtSignal()

    def __init__(self, explorer):
        super(WorkerObject, self).__init__()

        self.explorer = explorer
        self.player_stat_dict = {}
        self.full_list_of_data = []
        self.error_msg = None

    def get_player_stats(self):
        player_stat_name = None
        player_stat_data = None
        player_id = self.explorer.main_window.table_widget.player_id
        stats = player.PlayerCareer(player_id)
        for i in self.explorer.all_players.stat_category:
            try:
                player_stat_name = stats.json['resultSets'][0]['headers'][i]
                player_stat_data = stats.json['resultSets'][0]['rowSet'][-1][i]
            except IndexError:
                print(i)
            self.player_stat_dict[player_stat_name] = player_stat_data
            self.full_list_of_data.append(self.player_stat_dict)

        self.finished.emit()
