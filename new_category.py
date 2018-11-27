# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Relative Imports
# none


"""
    new_category file to hold model and data for dialog to enter new category information.

"""


class CategoryDialogSettings(object):

    """Tab dialog creation settings main class.

    TabSettings will act as the model in the model/view pair. This dialog will
    allow users to fully customize the new tab they want to embed into the tab widget.
    The settings that are applied here will control which new tab is created.

    """

    def __init__(self):
        self._category = None

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


class CategoryDialog(QDialog, object):

    """Build explorer UI and settings."""

    def __init__(self, parent):
        super(CategoryDialog, self).__init__(parent,
                                             flags=Qt.WindowTitleHint |
                                             Qt.WindowSystemMenuHint)
        self.parent = parent

        # Declare layouts
        layout = QVBoxLayout(self)

        # Label displaying information
        self.label = QLabel("Select which category to draw statistics for.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {font-size: 16px;}")

        # Custom tab as main view
        self.category = QComboBox()
        self.category.addItems(parent.all_categories.list)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.label)
        layout.addWidget(self.category, alignment=Qt.AlignCenter)
        layout.addWidget(self.buttons)

        self.setMinimumSize(350, 300)
        self.setWindowTitle("Set Category")

    @staticmethod
    def get_settings(parent):
        """
        Static method to get dialog setting.

        :param instance parent:
            Parent is CIP explorer.

        """
        dialog = CategoryDialog(parent)
        result = dialog.exec_()
        accepted = False
        if result == QDialog.Accepted:
            parent.category_cache.category = dialog.category.currentText()
            accepted = True
        return accepted

