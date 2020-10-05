from __future__ import absolute_import

import os
from functools import partial
from AnimIO import (api, LOG)
try:
    from AnimIO.packages.Qt import (QtWidgets, QtCore)
except ImportError:
    pass

this_package = os.path.abspath(os.path.dirname(__file__))
this_path = partial(os.path.join, this_package)


class UI(QtWidgets.QDialog):
    """
    AnimIO User Interface Dialog
    """
    def __init__(self, parent=None):

        super(UI, self).__init__(parent)

        # stores our animation item
        self.item = None
        self.default_string = "Add selected item..."

        self.setWindowTitle("Anim IO")
        self.resize(350, 100)

        # Grab stylesheet
        with open(this_path("style.css")) as f:
            self.setStyleSheet(f.read())

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        # menu bar
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.help = self.menu_bar.addMenu("Help")

        self.documentation = QtWidgets.QAction("Documentation", self)
        self.help.addAction(self.documentation)

        self.layout.setMenuBar(self.menu_bar)

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
        self.obj_line = QtWidgets.QLineEdit(self.default_string)
        self.obj_line.setReadOnly(True)
        self.add_obj_btn = QtWidgets.QPushButton("<<")

        self.obj_layout = QtWidgets.QHBoxLayout()
        self.obj_layout.addWidget(self.obj_lbl, 0)
        self.obj_layout.addWidget(self.obj_line, 1)
        self.obj_layout.addWidget(self.add_obj_btn, 0)

        self.import_btn = QtWidgets.QPushButton("Import Anim")
        self.export_btn = QtWidgets.QPushButton("Export Anim")

        self.startframe_chkbox = QtWidgets.QCheckBox()
        self.startframe_chkbox.setChecked(False)
        self.startframe_lbl = QtWidgets.QLabel("Start Frame :")
        self.startframe_lbl.setEnabled(False)
        self.startframe_spnbox = QtWidgets.QSpinBox()
        self.startframe_spnbox.setMinimum(-999999)
        self.startframe_spnbox.setMaximum(999999)
        self.startframe_spnbox.setAlignment(QtCore.Qt.AlignRight)
        self.startframe_spnbox.setMinimumWidth(75)
        self.startframe_spnbox.setEnabled(False)

        self.start_spacer = QtWidgets.QSpacerItem(
            100, 25,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)

        self.startframe_layout = QtWidgets.QHBoxLayout()
        self.startframe_layout.addItem(self.start_spacer)
        self.startframe_layout.addWidget(self.startframe_lbl, 0)
        self.startframe_layout.addWidget(self.startframe_spnbox, 0)
        self.startframe_layout.addWidget(self.startframe_chkbox, 0)

        self.layout.addLayout(self.obj_layout)
        self.layout.addWidget(self.import_btn)
        self.layout.addWidget(self.export_btn)
        self.layout.addLayout(self.startframe_layout)

    def add_callbacks(self):
        """
        Adds callbacks to widgets
        """
        self.add_obj_btn.clicked.connect(self.add_selection)
        self.import_btn.clicked.connect(self.import_anim)
        self.export_btn.clicked.connect(self.export_anim)
        self.startframe_chkbox.stateChanged.connect(self.toggle_startframe)
        self.documentation.triggered.connect(self.open_documentation)

    def add_tooltips(self):
        """
        Adds tooltips to widgets
        """
        self.add_obj_btn.setToolTip(
            "Press this button to add the "
            "currently selected animatable object.")
        self.obj_line.setToolTip(
            "Name of object to export or import animation")

        self.import_btn.setToolTip(
            "Press this button to import an "
            "exported anim json file.")
        self.export_btn.setToolTip(
            "Press this button to export a "
            "an anim json file.")

        self.startframe_spnbox.setToolTip(
            "Optional value to set start frame of animation.")
        self.startframe_chkbox.setToolTip(
            "Check this to apply start frame value.")

    def toggle_startframe(self, state):
        """
        Toggles startframe option
        """
        if QtCore.Qt.CheckState.Checked == state:
            self.startframe_spnbox.setEnabled(True)
            self.startframe_lbl.setEnabled(True)

        else:
            self.startframe_spnbox.setEnabled(False)
            self.startframe_lbl.setEnabled(False)

    def open_documentation(self):
        """
        Shows the documentation in webbrowser
        """
        import webbrowser
        webbrowser.get().open_new_tab(
            "https://animio.readthedocs.io/en/latest/")

    @api.flush_output
    def add_selection(self):
        """
        Adds selected object to ui
        """
        current_sel = api.get_selected()

        if current_sel:
            selected = current_sel[0].LongName
            self.obj_line.setText(selected)
            self.item = current_sel[0]
            LOG.debug("Added {0} to ui".format(selected))

    @api.flush_output
    def import_anim(self):
        """
        Import animation onto selected item
        """
        self.check_selected()

        file_browser = FileDialog(
            parent=self, view_mode=QtWidgets.QFileDialog.ExistingFile)

        if file_browser.exec_():
            file_names = file_browser.selectedFiles()

            if file_names:

                # read data
                anim_data = api.read_file(file_names[0])

                # check start frame
                start_frame = None
                if self.startframe_chkbox.isChecked():
                    start_frame = self.startframe_spnbox.value()

                # set data
                api.set_animdata(self.item, anim_data, start_frame)

    @api.flush_output
    def export_anim(self):
        """
        Export animation onto selected item in ui
        """
        self.check_selected()

        file_browser = FileDialog(parent=self)
        if file_browser.exec_():

            file_names = file_browser.selectedFiles()

            if file_names:
                anim_data = api.get_animdata(self.item)
                api.write_file(file_names[0], anim_data)

    @api.flush_output
    def check_selected(self):
        """
        Check that name is added to obj_line
        """
        if self.obj_line.text() == self.default_string:
            raise RuntimeError(
                "No object added to ui! "
                "Please select and add object to import or export.")


class FileDialog(QtWidgets.QFileDialog):
    """
    Subclass of QFileDialog with preferred attributes
    """
    def __init__(
        self, parent=None,
            view_mode=QtWidgets.QFileDialog.AnyFile):

        super(FileDialog, self).__init__(parent)

        self.setNameFilter("JSON (*.json)")
        self.setFileMode(view_mode)
        self.setViewMode(QtWidgets.QFileDialog.Detail)
