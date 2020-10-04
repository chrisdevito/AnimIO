from __future__ import absolute_import
import os
from functools import partial
from AnimIO.packages.Qt import (QtWidgets, QtCore)
from AnimIO import api

this_package = os.path.abspath(os.path.dirname(__file__))
this_path = partial(os.path.join, this_package)


class UI(QtWidgets.QDialog):
    """
    AnimIO User Interface Dialog
    """
    def __init__(self, parent=None):

        super(UI, self).__init__(parent)

        self.setWindowTitle("Anim IO")
        self.resize(350, 100)

        # Grab stylesheet
        with open(this_path("style.css")) as f:
            self.setStyleSheet(f.read())

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.add_widgets()
        self.add_callbacks()
        self.add_tooltips()

    def add_widgets(self):
        """
        Adds widgets to layout
        """
        self.obj_lbl = QtWidgets.QLabel("Object :")
        self.obj_line = QtWidgets.QLineEdit("Add selected item...")
        self.obj_line.setReadOnly(True)
        self.add_obj_btn = QtWidgets.QPushButton("<<")

        self.obj_layout = QtWidgets.QHBoxLayout()
        self.obj_layout.addWidget(self.obj_lbl, 0)
        self.obj_layout.addWidget(self.obj_line, 1)
        self.obj_layout.addWidget(self.add_obj_btn, 0)

        self.import_btn = QtWidgets.QPushButton("Import Anim")
        self.export_btn = QtWidgets.QPushButton("Export Anim")

        self.startframe_lbl = QtWidgets.QLabel("Start Frame :")
        self.startframe_spnbox = QtWidgets.QDoubleSpinBox()
        self.startframe_spnbox.setMinimum(-999999)
        self.startframe_spnbox.setMaximum(999999)
        self.startframe_spnbox.setAlignment(QtCore.Qt.AlignRight)
        self.startframe_spnbox.setMinimumWidth(75)

        self.start_spacer = QtWidgets.QSpacerItem(
            100, 25,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)

        self.startframe_layout = QtWidgets.QHBoxLayout()
        self.startframe_layout.addItem(self.start_spacer)
        self.startframe_layout.addWidget(self.startframe_lbl, 0)
        self.startframe_layout.addWidget(self.startframe_spnbox, 0)

        self.layout.addLayout(self.obj_layout)
        self.layout.addWidget(self.import_btn)
        self.layout.addWidget(self.export_btn)
        self.layout.addLayout(self.startframe_layout)

    def add_callbacks(self):
        """
        Adds callbacks to widgets
        """
        self.add_obj_btn.clicked.connect(self.add_selection)
        self.export_btn.clicked.connect(self.export_anim)
        self.import_btn.clicked.connect(self.import_anim)

    def add_tooltips(self):
        """
        Adds tooltips to widgets
        """
        pass

    def add_selection(self):
        """
        Adds selected object to ui
        """
        current_sel = api.get_selected()

        if current_sel:
            self.obj_line.setText(current_sel[0].name())

    def import_anim(self):
        """
        Import animation onto selected item
        """
        pass

    def export_anim(self):
        """
        Import animation onto selected item
        """
        pass
