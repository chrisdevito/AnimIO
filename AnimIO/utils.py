from __future__ import absolute_import

from AnimIO.ui.ui import UI
from AnimIO.ui import utils


def show():
    """
    Shows ui
    """
    win = UI(parent=utils.get_motion_builder_window())
    win.show()
