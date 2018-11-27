# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Relative Imports
from acc_options_dialog import TrackerConfigure


class MenuBar(object):

    """Defines and controls all menubar actions."""

    def __init__(self, parent):
        menubar = parent.menuBar()
        self.parent = parent

        # FILE MENU
        file_mb = menubar.addMenu("File")

        settings = QAction("Options...", parent)
        file_mb.addAction(settings)
        settings.triggered.connect(self.open_settings_cb)

        clear = QAction("Reset Draft Table", parent)
        clear.setShortcut("Ctrl+R")
        file_mb.addAction(clear)
        clear.triggered.connect(self.clear_table_cb)

        export = QAction("Export Console", parent)
        export.setShortcut("Ctrl+E")
        file_mb.addAction(export)

        file_mb.addSeparator()

        quit_mb = QAction("Quit", parent)
        quit_mb.setShortcut("Ctrl+Q")
        file_mb.addAction(quit_mb)
        quit_mb.triggered.connect(self.quit_application_cb)


        # HELP MENU
        help_mb = menubar.addMenu("Help")

        cip_object_help = QAction("Stat Tracker Help", parent)
        cip_object_help.setShortcut("Ctrl+H")
        help_mb.addAction(cip_object_help)
        cip_object_help.triggered.connect(self.show_help_cb)

        help_mb.addSeparator()

        about = QAction("About", parent)
        help_mb.addAction(about)
        about.triggered.connect(self.show_about_cb)


    #CALLBACKS------------------
    def open_settings_cb(self):
        """Display options for configuration."""
        accepted = TrackerConfigure.get_settings(self.parent)
        if accepted:
            self.parent.main_window.refresh_season_cb()

    def clear_table_cb(self):
        """Docstring"""
        self.parent.main_window.table_widget.clear()
        self.parent.main_window.table_widget.set_default_categories()
        self.parent.main_window.table_widget.set_default_players()

    def quit_application_cb(self):
        """Docstring"""
        self.parent.quit_cb()

    def show_help_cb(self):
        """Display message on how to use."""
        msg = ("NBA Stat Tracker is a GUI that allows users to enter their draft information,"
               "search globally for players to receive basic or advanced statistics, and to track"
               "statistics on live inputted players to help during the NBA fantasy season.\n\n"
               "This application is currently in development mode and all comments/concerns should"
               "be sent to jokersaidit@gmail.com or the github link can be followed directly at:\n"
               "www.github.com")
        QMessageBox.about(self.parent, "Help", msg)

    def show_about_cb(self):
        """Display message on how to use."""
        msg = "NBA Stat Tracker can be used to search for player information."
        QMessageBox.about(self.parent, "About", msg)


class StatusBar(object):

    """Defines and controls all statusbar actions."""

    def __init__(self, parent):
        self.statusbar = parent.statusBar()
        self.parent = parent     # parent is CipExplorer
        self.statusbar.setSizeGripEnabled(True)
        font = QFont()
        font.setFamily("Helvetica [Cronyx]")
        font.setPointSize(10)
        font.setWeight(60)
        self.statusbar.setFont(font)
        self.statusbar.setStyleSheet("background-color:rgb(193, 193, 193)")
        parent.setStatusBar(self.statusbar)