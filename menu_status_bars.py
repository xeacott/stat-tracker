# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MenuBar(object):

    """Defines and controls all menubar actions."""

    def __init__(self, parent):
        menubar = parent.menuBar()
        self.parent = parent

        # FILE MENU
        file_mb = menubar.addMenu("File")

        settings = QAction("Options...", parent)
        file_mb.addAction(settings)

        export = QAction("Export Console", parent)
        export.setShortcut("Ctrl+E")
        file_mb.addAction(export)

        quit_mb = QAction("Quit", parent)
        quit_mb.setShortcut("Ctrl+Q")
        file_mb.addAction(quit_mb)


        # HELP MENU
        help_mb = menubar.addMenu("Help")

        cip_object_help = QAction("Stat Tracker Help", parent)
        cip_object_help.setShortcut("Ctrl+H")
        help_mb.addAction(cip_object_help)

        help_mb.addSeparator()

        about = QAction("About", parent)
        help_mb.addAction(about)
        about.triggered.connect(self.show_help)


    #CALLBACKS------------------
    def show_help(self):
        """Display message on how to use."""
        msg = ("NBA Stat Tracker can be used to search for player information.")
        QMessageBox.about(self.parent,
                          "About",
                          msg)


class StatusBar(object):

    """Defines and controls all statusbar actions."""

    def __init__(self, parent):
        statusbar = parent.statusBar()
        self.parent = parent     # parent is CipExplorer
        statusbar.setSizeGripEnabled(True)
        font = QFont()
        font.setFamily("")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(55)
        statusbar.setFont(font)
        statusbar.setStyleSheet("background-color:rgb(192, 192, 192)")
        parent.setStatusBar(statusbar)