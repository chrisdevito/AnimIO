from AnimIO.ui.ui import UI
from AnimIO.ui import utils


def show():
    """
    Shows ui

    :raises: None
    :return: None
    :rtype: NoneType
    """
    win = UI(parent=utils.get_motion_builder_window())
    win.show()
