# Standard Library
import os, os.path
import pickle
from enum import IntEnum

# Third Party Packages
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


"""
    restore file to be the entire model for which player and category data will be filed.
"""

FILENAME = r'C:\STAT-tracker\settings.cache'
DIRECTORY = r'C:\STAT-tracker'


class Cache(IntEnum):

    """Set cache enums."""

    NIGHT_MODE = 0
    FONT_SCALER = 1
    CURRENT_SEASON = 2


class LoadSettings(QObject, object):

    """Load and save data to use for session.

    Restore class creates an object to be used as a container to hold
    all the necessary settings and object structure between sessions.

    """

    restart_signal = pyqtSignal()

    def __init__(self, parent):
        super(LoadSettings, self).__init__(parent)
        # Explorer settings
        self.parent = parent

        # Global settings
        self.night_mode = False
        self.font_scaler = 1
        self.current_season = "2018-19"

        # Flags
        self.error_msg = None

        # Setup restart signal if theme or font has changed
        self.restart_signal.connect(self.parent.restart_cb)

        self.load_cache()

    def load_cache(self):
        """Load previously saved settings.

        :raises:
            'IOError' when a cache file is not found.

            'RuntimeError' when revision of cache file has changed.

        """
        # pylint: disable=unused-variable
        try:
            # Read data from an existing file
            with open(FILENAME, 'rb') as handle:
                read_object = pickle.load(handle)

                self.night_mode = read_object.get(Cache.NIGHT_MODE)
                self.font_scaler = read_object.get(Cache.FONT_SCALER)
                self.current_season = read_object.get(Cache.CURRENT_SEASON)

        except IOError:
            self.error_msg = ('No previous configuration found. '
                              'Please restore your players.')

        except RuntimeError:
            try:
                os.remove(FILENAME)
            except OSError:
                pass
            self.error_msg = (
                'Cip-explorer revision is incompatible with previously'
                ' saved channel configuration. Please configure your channel.')

    def save_cache(self, restart):
        """Save settings from dialog."""
        self.cached_settings = {}
        self.cached_settings[Cache.NIGHT_MODE] = self.night_mode
        self.cached_settings[Cache.FONT_SCALER] = self.font_scaler
        self.cached_settings[Cache.CURRENT_SEASON] = self.current_season

        if not os.path.exists(DIRECTORY):
            os.mkdir(DIRECTORY)

        with open(FILENAME, 'wb') as handle:
            pickle.dump(self.cached_settings, handle, protocol=pickle.HIGHEST_PROTOCOL)

        if restart:
            self.restart_signal.emit()
