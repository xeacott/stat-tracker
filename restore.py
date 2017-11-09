# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


"""
    restore file to be the entire model for which player and category data will be filed.

"""



class Categories(object):

    """Spawns a worker and thread to get a list of categories for a user."""

    def __init__(self, parent):
        super(Categories, self).__init__()
        self.parent = parent

        self.list = ['Offense',
                     'Defense']


class Players(object):

    """Spawns a worker and thread to get a list of players for a user."""

    def __init__(self, parent):
        super(Players, self).__init__()
        self.parent = parent

        self.list = ['DeAndre Jordan',
                     'Chris Paul']