# Standard Library
# none

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Relative Imports
from new_category import *


class MainWindow(QWidget, object):

    """Main window of Stat Tracker.

    MainWindow is parent to menubar and statusbar. Instantiates the main
    objects to be used by CipExplorer. It is the main window of QApplication.

    """

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent  # parent is CipExplorer

        # Menubar / Statusbar
        self.menubar = MenuBar(parent)
        self.statusbar = StatusBar(parent)

        # Declare layouts
        layout = QHBoxLayout()
        middle_table = QVBoxLayout()

        # Center Table Widget and Buttons
        self.table_widget = PresentData(self.parent)

        go_live_button = QPushButton("Go Live!")
        go_live_button.setToolTip("Allow for live stats to update.")
        go_live_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        go_live_button.setSizePolicy(go_live_policy)

        middle_table.addWidget(go_live_button, alignment=Qt.AlignCenter)
        middle_table.addSpacerItem(QSpacerItem(0, 25))
        middle_table.addWidget(self.table_widget)

        # Set layouts
        layout.addLayout(middle_table)

        # Set signals
        go_live_button.clicked.connect(self.go_live_cb)

        self.setLayout(layout)
        self.setMinimumSize(950, 450)

    # CALLBACKS----------
    def go_live_cb(self):
        """Handle updating the table with live data."""


class MenuBar(object):

    """Defines and controls all menubar actions."""

    def __init__(self, parent):
        menubar = parent.menuBar()
        self.parent = parent

        # FILE MENU
        file_mb = menubar.addMenu("File")

        new_tab = QAction("New Tab", parent)
        new_tab.setShortcut("Ctrl+T")
        file_mb.addAction(new_tab)

        compare = QAction("Compare", parent)
        compare.setShortcut("Ctrl+C")
        file_mb.addAction(compare)

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

        cip_object_help = QAction("Explorer Help", parent)
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


class PresentData(QTableWidget, object):

    """Give user a nice way to view the information requested."""

    def __init__(self, parent):
        super(PresentData, self).__init__(parent)
        self.parent = parent

        self.wordWrap()
        self.setRowCount(10)
        self.setColumnCount(10)
        self.setCornerButtonEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

        self.vertical_header = self.verticalHeader()
        self.vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        # Signals
        self.horizontal_header.sectionDoubleClicked.connect(self.set_horizontal_headers)
        self.vertical_header.sectionDoubleClicked.connect(self.set_vertical_headers)


    def set_horizontal_headers(self, i):
        """Set the horizontal headers, user requested.

        :param list headers:
            List of categories user wishes to see.

        """
        i = (self.currentColumn())
        header = QTableWidgetItem()
        accepted = TabDialog.get_settings(self.parent)
        if accepted:
            header.setText(self.parent.cached_settings.category)
            self.setHorizontalHeaderItem(i, header)


    def set_vertical_headers(self, i):
        """Set the vertical headers, user requested.

        :param list headers:
            List of players user wishes to see.

        """
        # self.setVerticalHeaderLabels(headers)



class CipExplorer(QMainWindow, object):

    """Display main window of CIP Object Explorer.

    This is the entry point for control of Explorer. This class handles
    reading the cached settings and properly restoring the state of GUI from
    last termination.

    """

    def __init__(self, parent=None):
        super(CipExplorer, self).__init__(parent)
        favicon = QIcon()
        self.setWindowIcon(favicon)
        self.setWindowTitle("NBA Stat Tracker")

        self.cached_settings = TabDialogSettings()
        self.all_categories = GetList(self)

        self.main_window = MainWindow(self)
        self.setCentralWidget(self.main_window)

    # CALLBACKS----------
    def on_start(self):
        print('on start')

    def quit_cb(self, quit_signal):
        """Terminate CipExplorer application.

        Cleanup activities related to termination of the application are
        located here.

        :param signal quit_signal:
            Quit signal.

        """
        self.close()
