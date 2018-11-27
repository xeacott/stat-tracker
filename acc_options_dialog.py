# Standard Library

# Third Party Packages
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Relative Imports
# none


class TrackerSettings(object):

    """Stat Tracker configuration settings.

    TrackerSettings is the model for the TrackerConfig view/controller.

    """

    def __init__(self, restore):

        self._restore = restore

        self._night_mode = False
        self._font_scaler = 1
        self._current_season = "2018-19"
        self._year_changed = False

        self._filename = r'C:\RAEngineering\cip-explorer.cache'
        self._description = "CIP Object Explorer channel settings."
        self.success = False
        self.load_cache()

    @property
    def night_mode(self):
        """Get the Night Mode selection.

        :returns: night_mode
        :rtype: bool

        """
        return self._night_mode

    @night_mode.setter
    def night_mode(self, value):
        """Set the Night Mode selection.

        :param bool value:
            Value is the currently active selection.

        """
        self._night_mode = value

    @property
    def font_scaler(self):
        """Get the Font Scaler Value.

        :returns: font scaler
        :rtype: int

        """
        return self._font_scaler

    @font_scaler.setter
    def font_scaler(self, value):
        """Set the font scaler.

        :param int value:
            Value is the currently active font scaler.

        """
        self._font_scaler = value

    @property
    def current_season(self):
        """Get the current season.

        :returns: current season
        :rtype: int

        """
        return self._current_season

    @current_season.setter
    def current_season(self, value):
        """Set the current season.

        :param int value:
            Value is the currently active season years.

        """
        self._current_season = value


    @property
    def year_changed(self):
        """Get the Night Mode selection.

        :returns: night_mode
        :rtype: bool

        """
        return self._year_changed

    @year_changed.setter
    def year_changed(self, value):
        """Set the Night Mode selection.

        :param bool value:
            Value is the currently active selection.

        """
        self._year_changed = value

    @property
    def error_msg(self):
        """Get the error message.

        :returns: error_msg
        :rtype: string

        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, value):
        """Set the error message.

        :param string value:
            Value is whatever the message is, check load/save cache
            to list current message strings.

        """
        self._error_msg = value

    def load_cache(self):
        """Load previously saved data from file."""
        if self._restore is not None:
            self._night_mode = self._restore.night_mode
            self._font_scaler = self._restore.font_scaler
            self._current_season = self._restore.current_season

    def save_cache(self):
        """Save settings back to restore object."""
        restart = False
        if self._restore.night_mode != self._night_mode:
            restart = True

        self._restore.night_mode = self._night_mode
        self._restore.font_scaler = self._font_scaler
        self._restore.current_season = self._current_season
        self._restore.save_cache(restart)


class TrackerConfigure(QDialog, object):

    """Display Tracker Configuration modal dialog.

    TrackerConfigure is the view/controller for the TrackerSettings model.

    """

    def __init__(self, parent):
        super(TrackerConfigure, self).__init__(parent,
                                               flags=Qt.WindowTitleHint |
                                               Qt.WindowSystemMenuHint)

        self.parent = parent

        # Gui options
        self.gui_options = self.create_options()

        # button button box
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # layouts and container creation
        hbox = QVBoxLayout()
        hbox.addWidget(self.gui_options)
        hbox.addWidget(self.buttons)

        self.init_mode_options()
        self.init_slider_options()
        self.init_season_options()

        self.setLayout(hbox)
        self.setMinimumSize(350, 300)
        self.setWindowTitle("GUI Configuration")

    @staticmethod
    def get_settings(parent):
        """Set the channel_settings based on dialog.

        :param instance parent:
            Parent is Tracker.

        """
        dialog = TrackerConfigure(parent)
        result = dialog.exec_()
        update = False
        if result == QDialog.Accepted:
            parent.tracker_settings.light_mode = dialog.light_mode_button.isChecked()
            parent.tracker_settings.night_mode = dialog.night_mode_button.isChecked()
            parent.tracker_settings.font_scaler = dialog.font_slider.value()
            if parent.tracker_settings.current_season != dialog.season_selection.currentText():
                update = True
            parent.tracker_settings.year_changed = update
            parent.tracker_settings.current_season = dialog.season_selection.currentText()

            parent.tracker_settings.save_cache()
            return True

    def create_options(self):
        """Populate widgets into the options dialog."""
        group_box = QGroupBox("GUI Configuration")

        self.change_theme_label = QLabel("Set Default Theme")
        self.change_font_size = QLabel("Set Font Size")
        self.change_season_years = QLabel("Set Current Season")

        self.light_mode_button = QRadioButton("Light Theme")
        self.night_mode_button = QRadioButton("Dark Theme")

        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setMinimum(8)
        self.font_slider.setMaximum(24)
        self.font_slider.setValue(16)

        self.font_slider.setTickPosition(QSlider.TicksBelow)
        self.font_slider.setTickInterval(1)
        self.font_slider.sizeHint()

        self.season_selection = QComboBox()
        self.season_selection.addItems(self.parent.all_seasons.seasons)
        self.season_selection.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding))

        vbox = QVBoxLayout()
        vbox.addWidget(self.change_theme_label)
        vbox.addWidget(self.light_mode_button)
        vbox.addWidget(self.night_mode_button)
        vbox.addSpacerItem(QSpacerItem(0, 20))

        vbox.addWidget(self.change_font_size)
        vbox.addWidget(self.font_slider)
        vbox.addSpacerItem(QSpacerItem(0, 20))

        vbox.addWidget(self.change_season_years)
        vbox.addWidget(self.season_selection, alignment=Qt.AlignCenter)
        group_box.setLayout(vbox)

        return group_box

    def init_mode_options(self):
        """Upon initialization of dialog set the current settings to reflect GUI state."""
        if self.parent.restore.night_mode:
            self.light_mode_button.setChecked(False)
            self.night_mode_button.setChecked(True)

        else:
            self.light_mode_button.setChecked(True)
            self.night_mode_button.setChecked(False)

    def init_slider_options(self):
        """Docstring"""

    def init_season_options(self):
        """Docstring"""
        element = self.parent.all_seasons.seasons.index(self.parent.restore.current_season)
        self.season_selection.setCurrentIndex(element)