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
        self.full_player_list()

    def full_player_list(self):
        """Get a complete list of all players and their associated player ID."""

        for player in players.get_players():
            self.player_list.append(player)
            self.player_id.append(player['id'])
            if player['first_name']:
                self.abv_player_list.append(player['first_name'][0] + ". " + player['last_name'])
            else:
                self.abv_player_list.append(player['last_name'])

