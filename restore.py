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
        self.player_stats = {
            'MIN': None,
            'FGM': None,
            'FGA': None,
            'FG_PCT': None,
            'FG3M': None,
            'FG3A': None,
            'FG3_PCT': None,
            'FTM': None,
            'FTA': None,
            'FT_PCT': None,
            'OREB': None,
            'DREB': None,
            'REB': None,
            'AST': None,
            'STL': None,
            'BLK': None,
            'TOV': None,
            'PF': None,
            'PTS': None
        }
        self.team_ids = []
        self.player_list = []
        self.player_id = []
        self.player_and_id_dict = []
        self.stat_category = range(5, 24)
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


    def get_player_stats(self, player_id):
        player_stat_dict = {}
        full_list_of_data = []
        player_stat_name = None
        player_stat_data = None
        stats = player.PlayerCareer(player_id)
        for i in self.stat_category:
            try:
                player_stat_name = stats.json['resultSets'][1]['headers'][i]
                player_stat_data = stats.json['resultSets'][1]['rowSet'][0][i]
            except IndexError:
                print(i)
            player_stat_dict[player_stat_name] = player_stat_data
            full_list_of_data.append(player_stat_dict)
        return player_stat_dict



