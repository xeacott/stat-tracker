# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

"""
    new_category file to hold model and data for dialog to enter new category information.

"""


class PlayerDialogSettings(object):

    """Tab dialog creation settings main class.

    TabSettings will act as the model in the model/view pair. This dialog will
    allow users to fully customize the new tab they want to embed into the tab widget.
    The settings that are applied here will control which new tab is created.

    """

    def __init__(self):
        self._player = None
        self.success = False

    @property
    def player(self):
        """Return attribute settings.

        :returns: attr boolean value.
        :rtype: bool

        """
        return self._player

    @player.setter
    def player(self, value):
        """
        Set attr value based on value.

        :param bool value:
            Value to set if dump is set.

        """
        self._player = value


class PlayerDialog(QDialog, object):

    """Build explorer UI and settings."""

    def __init__(self, parent):
        super(PlayerDialog, self).__init__(parent,
                                             flags=Qt.WindowTitleHint |
                                             Qt.WindowSystemMenuHint)
        self.parent = parent

        # Declare layouts
        layout = QVBoxLayout(self)

        # Custom tab as main view
        self.player = PlayerEntry(parent)
        layout.addWidget(self.player, alignment=Qt.AlignCenter)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setMinimumSize(350, 250)
        self.setWindowTitle("Set Player")

    #CALLBACKS-------------------
    def test_text_cb(self):
        approved = True
        if not self.player.text() in self.parent.all_players.list:
            QMessageBox.about(self,
                              'Notice!',
                              'Player not loaded, please try again.')
            approved = False
        return approved

    @staticmethod
    def get_settings(parent):
        """
        Static method to get dialog setting.

        :param instance parent:
            Parent is CIP explorer.

        """
        dialog = PlayerDialog(parent)
        result = dialog.exec_()
        accepted = False
        if result == QDialog.Accepted:
            approved = dialog.test_text_cb()
            if approved:
                parent.player_cache.player = dialog.player.text()
                accepted = True
        return accepted


class PlayerEntry(QLineEdit, object):


    """Line edit to support auto-complete and other various methods needed for players."""

    def __init__(self, parent):
        super(PlayerEntry, self).__init__(parent)
        self.parent = parent

        self.completer = QCompleter()
        self.setCompleter(self.completer)

        self.t = self.parent.all_players.list
        my_completer = QCompleter(self.t, self)
        my_completer.setCaseSensitivity(1)
        self.setCompleter(my_completer)
