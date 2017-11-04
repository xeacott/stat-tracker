# Standard Library
import argparse
import sys
from importlib import import_module

# Third Party Packages
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


MAIN_WINDOW = import_module('mainwindow')


def main():
    """Drive application upon startup and setup environment."""
    # Launch NBA Stat Tracker main window
    app = QApplication(sys.argv)
    mw = MAIN_WINDOW.CipExplorer()
    mw.show()

    # Closure to ensure information window opens after the
    # event loop is started
    def on_start_cb():
        mw.on_start()
    QTimer.singleShot(0, on_start_cb)

    app.exec_()
    app.deleteLater()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='stat-tracker', description='NBA Stat Tracker GUI.')

    args = parser.parse_args()
    main()
