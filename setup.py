import os
import shutil
from functools import partial

import pyfbsdk

this_package = os.path.abspath(os.path.dirname(__file__))
this_path = partial(os.path.join, this_package)


def setup():
    """
    adds package to python folder in motionbuilder
    """
    package_path = this_path("AnimIO")
    python_path = pyfbsdk.FBSystem().GetPythonStartupPath()[0]
    dest_path = os.path.join(python_path, "AnimIO")

    # remove dir if exists to reinstall
    if os.path.exists(dest_path):

        result = pyfbsdk.FBMessageBox(
            "Reinstall", "Reinstall AnimIO?", "Ok", "Cancel")

        if result == 1:
            shutil.rmtree(dest_path)
        else:
            raise RuntimeError("AnimIO not reinstalled!")

    shutil.copytree(
        package_path, dest_path)

    pyfbsdk.FBMessageBox(
        "Installed", "AnimIO has been installed", "Ok")


if __name__ == '__builtin__':
    setup()
