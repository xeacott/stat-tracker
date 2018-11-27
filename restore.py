# Standard Library

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# NBA Package
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerfantasyprofile


"""
    restore file to be the entire model for which player and category data will be filed.
"""

class Seasons(object):

    """Holds all available seasons."""

    def __init__(self):

        self.seasons = [
            "2010-11",
            "2011-12",
            "2012-13",
            "2013-14",
            "2014-15",
            "2015-16",
            "2016-17",
            "2017-18",
            "2018-19"
        ]


class Categories(object):

    """Spawns a worker and thread to get a list of categories for a user."""

    def __init__(self, parent):
        super(Categories, self).__init__()
        self.parent = parent

        self.list = []
        self.full_category_list()

    def full_category_list(self):
        """Get a complete list of all categories."""

        for category in playerfantasyprofile.PlayerFantasyProfile.expected_data['Overall']:
            self.list.append(category)


class Players(object):

    """Spawns a worker and thread to get a list of players for a user."""

    def __init__(self, parent):
        super(Players, self).__init__()
        self.parent = parent

        self.player_list = []
        self.player_id = []
        self.abv_player_list = []
        self.last_names = []
        self.full_player_list()

    def full_player_list(self):
        """Get a complete list of all players and their associated player ID."""

        for player in players.get_players():
            if player['first_name']:
                abv_name = ("{}. {}".format(player['first_name'][0], player['last_name']))
                last_name_first_name = ("{}, {}".format(player['last_name'], player['first_name']))
                player_id = ("{}".format(player['id']))
                self.abv_player_list.append(abv_name)
                self.last_names.append(last_name_first_name)
                self.player_id.append(player_id)
