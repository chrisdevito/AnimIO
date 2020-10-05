from __future__ import absolute_import

from AnimIO.packages.Qt import QtWidgets


def get_motion_builder_window():
    """
    Get MotionBuilder MainWindow as a QWidget.

    :raises: ``RuntimeError`` if no MotionBuilder window not found

    :return: MotionBuilder's main window
    :rtype: QtGui.QWidget
    """
    widget = QtWidgets.QApplication.activeWindow()

    if not widget:
        for widget in QtWidgets.QApplication.instance().topLevelWidgets():
            if "MotionBuilder" in widget.windowTitle():
                return widget
    else:
        return widget

    raise RuntimeError('Could not locate MotionBuilderWindow...')
