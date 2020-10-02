import os
from functools import partial
from AnimIO.packages.Qt import (QtWidgets, QtCore)

this_package = os.path.abspath(os.path.dirname(__file__))
this_path = partial(os.path.join, this_package)


class UI(QtWidgets.QDialog):
    """
    AnimIO User Interface Dialog
    """
    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        # Set window
        self.setWindowTitle("Anim IO")
        self.resize(450, 275)

        # Grab stylesheet
        with open(this_path("style.css")) as f:
            self.setStyleSheet(f.read())

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
