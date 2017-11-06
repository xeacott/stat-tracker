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


class TabDialogSettings(object):

    """Tab dialog creation settings main class.

    TabSettings will act as the model in the model/view pair. This dialog will
    allow users to fully customize the new tab they want to embed into the tab widget.
    The settings that are applied here will control which new tab is created.

    """

    def __init__(self):
        self._attr = False
        self._category = None
        self.success = False

    @property
    def attr(self):
        """Return attribute settings.

        :returns: attr boolean value.
        :rtype: bool

        """
        return self._attr

    @attr.setter
    def attr(self, value):
        """
        Set attr value based on value.

        :param bool value:
            Value to set if dump is set.

        """
        self._attr = value

    @property
    def category(self):
        """Return attribute settings.

        :returns: attr boolean value.
        :rtype: bool

        """
        return self._category

    @category.setter
    def category(self, value):
        """
        Set attr value based on value.

        :param bool value:
            Value to set if dump is set.

        """
        self._category= value


class TabDialog(QDialog, object):

    """Build explorer UI and settings."""

    def __init__(self, parent):
        super(TabDialog, self).__init__(parent,
                                        flags=Qt.WindowTitleHint |
                                           Qt.WindowSystemMenuHint)
        self.parent = parent

        # Declare layouts
        layout = QVBoxLayout(self)

        # Custom tab as main view
        self.category = LineEdit(parent)
        layout.addWidget(self.category, alignment=Qt.AlignCenter)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setMinimumSize(350, 250)
        self.setWindowTitle("Set Category")

    #CALLBACKS-------------------
    def test_text_cb(self):
        approved = True
        if not self.category.text() in self.parent.all_categories.list:
            QMessageBox.about(self,
                              'Notice!',
                              'Category not loaded, please try again.')
            approved = False
        return approved

    @staticmethod
    def get_settings(parent):
        """
        Static method to get dialog setting.

        :param instance parent:
            Parent is CIP explorer.

        """
        dialog = TabDialog(parent)
        result = dialog.exec_()
        accepted = False
        if result == QDialog.Accepted:
            approved = dialog.test_text_cb()
            if approved:
                parent.cached_settings.category = dialog.category.text()
                accepted = True
        return accepted


class LineEdit(QLineEdit, object):


    """Line edit to support auto-complete and other
    various methods needed for categories.

    """

    def __init__(self, parent):
        super(LineEdit, self).__init__(parent)
        self.parent = parent

        self.completer = QCompleter()
        self.setCompleter(self.completer)

        self.t = self.parent.all_categories.list
        my_completer = QCompleter(self.t, self)
        my_completer.setCaseSensitivity(1)
        self.setCompleter(my_completer)


class GetList(object):

    """Spawns a worker and thread to get a list of categories for a user."""

    def __init__(self, parent):
        super(GetList, self).__init__()
        self.parent = parent

        self.list = ['Offense',
                     'Defense']