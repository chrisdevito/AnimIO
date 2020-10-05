from __future__ import absolute_import

import json

import pyfbsdk
import pythonidelib

from AnimIO import LOG


def flush_output(func):
    """
    Quick decorator wrapper to flush output after code is run

    :param func: function to execute
    :type func: function

    :return: wrapped function
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            pythonidelib.FlushOutput()
            return result
        except BaseException as err:
            pythonidelib.FlushOutput()
            raise err
        finally:
            pythonidelib.FlushOutput()

    return wrapper


def write_file(file_path, anim_data):
    """
    Writes anim_data to file in json format

    :param file_path: path of file
    :type file_path: str

    :param anim_data: dict of data
    :type anim_data: dict
    """
    if not file_path.endswith(".json"):
        file_path += ".json"

    with open(file_path, "w") as write_file:
        json.dump(anim_data, write_file, sort_keys=True, indent=4)

    LOG.info("Successfully wrote animation data to {0}".format(file_path))


def read_file(file_path):
    """
    Reads anim_data from file

    :param file_path: path of file
    :type file_path: str

    :return: anim_data
    :rtype: diict
    """
    with open(file_path, "r") as read_file:
        anim_data = json.load(read_file)

    LOG.info("Successfully read animation data from {0}".format(file_path))
    return anim_data


def get_selected(type_filters=[]):
    """
    Gets selected components

    :param type_filters: list of class types to filter
    :type type_filters: list of str

    :return: list of components
    :rtype: list of objects
    """
    scene = pyfbsdk.FBSystem().Scene

    selected = []
    for comp in scene.Components:
        if comp.Selected and \
            hasattr(comp, "Animatable") and \
                comp.ClassName() not in type_filters:
            selected.append(comp)

    return selected


def get_curve_data(fcurve):
    """
    Gets data from fcurve

    :param fcurve: fcurve to get data
    :type fcurve: pyfbsdk.FBFCurve

    :return: list of curve data
    :rtype: list of dict
    """
    key_data_list = []

    for key in fcurve.Keys:

        key_data = {
            'time': key.Time.Get(),
            'value': key.Value,
            'interpolation': int(key.Interpolation),
            'tangent-mode': int(key.TangentMode),
            'constant-mode': int(key.TangentConstantMode),
            'left-derivative': key.LeftDerivative,
            'right-derivative': key.RightDerivative,
            'left-weight': key.LeftTangentWeight,
            'right-weight': key.RightTangentWeight
        }

        key_data_list.append(key_data)

    return key_data_list


def tangent_is_default_weight(tangent_weight):
    """
    Checks if tangent is equal to default value of 1/3

    :param tangent_is_default_weight: value to check
    :type tangent_is_default_weight: float

    :return: If default weight
    :rtype: bool
    """
    return tangent_weight > 0.3333 and tangent_weight < 0.3334


def set_curve_data(fcurve, key_data_list, frame_offset=0):
    """
    Sets curve data

    :param fcurve: fcurve to set data on
    :type fcurve: pyfbsdk.FBFCurve

    :param key_data_list: key data ordered in time as list
    :type key_data_list: list of dict

    :param frame_offset: frame offset value
    :type frame_offset: int
    """
    # clear curve first
    fcurve.EditClear()

    # grab offset in frames
    fb_offset = pyfbsdk.FBTime(0, 0, 0, frame_offset, 0)

    # set keys
    for key_data in key_data_list:

        # add key
        key_index = fcurve.KeyAdd(
            pyfbsdk.FBTime(key_data['time']) + fb_offset,
            key_data['value'])
        key = fcurve.Keys[key_index]

        # set interp
        key.Interpolation = pyfbsdk.FBInterpolation.values[
            key_data['interpolation']]

        # set tangent
        key.TangentMode = pyfbsdk.FBTangentMode.values[
            key_data['tangent-mode']]

        # not using TCB mode just set to break
        if key.TangentMode == pyfbsdk.FBTangentMode.kFBTangentModeTCB:
            key.TangentMode = pyfbsdk.FBTangentMode.kFBTangentModeBreak

        # set tangent constant
        key.TangentConstantMode = pyfbsdk.FBTangentConstantMode.values[
            key_data['constant-mode']]

    # set tangents
    for i, key_data in enumerate(key_data_list):
        key = fcurve.Keys[i]

        key.LeftDerivative = key_data['left-derivative']
        key.RightDerivative = key_data['right-derivative']

        # set tangent if needed to keep tangents from being unlocked
        if not tangent_is_default_weight(key_data['left-weight']):
            key.LeftTangentWeight = key_data['left-weight']

        if not tangent_is_default_weight(key_data['right-weight']):
            key.RightTangentWeight = key_data['right-weight']


@flush_output
def get_animdata(item):
    """
    Gets animation translation and rotation of item

    :param item: item to get data from
    :type item: pyfbsdk component

    :return: dict of data
    :rtype: dict
    """
    trans_anim_node = item.Translation.GetAnimationNode()
    rots_anim_node = item.Rotation.GetAnimationNode()

    if not trans_anim_node and not rots_anim_node:
        raise RuntimeError(
            "No animation found on Translation or Rotation of {0}".format(
                item.LongName))

    # store data
    anim_data = {"Translation": [],
                 "Rotation": []}

    if trans_anim_node:
        for i, anim_node in enumerate(trans_anim_node.Nodes):
            if anim_node.FCurve and len(anim_node.FCurve.Keys):
                anim_data["Translation"].append(
                    get_curve_data(anim_node.FCurve))
            else:
                anim_data["Translation"].append(
                    [{"value": item.Translation[i],
                     "static": True}])
    else:
        for i in xrange(3):
            anim_data["Translation"].append(
                [{"value": item.Translation[i],
                 "static": True}])

    if rots_anim_node:
        for i, anim_node in enumerate(rots_anim_node.Nodes):
            if anim_node.FCurve and len(anim_node.FCurve.Keys):
                anim_data["Rotation"].append(
                    get_curve_data(anim_node.FCurve))
            else:
                anim_data["Rotation"].append(
                    [{"value": item.Rotation[i],
                     "static": True}])
    else:
        for i in xrange(3):
            anim_data["Rotation"].append(
                [{"value": item.Rotation[i],
                 "static": True}])

    return anim_data


def get_startframe(anim_data):
    """
    Gets startframe from data

    :param anim_data: dict of data
    :type anim_data: dict

    :return: int or None
    :rtype: int or NoneType
    """
    # get start frame to offset from
    start_frames = []
    for t in anim_data["Translation"]:
        time_value = t[0].get("time")
        if time_value is not None:
            start_frames.append(time_value)

    if start_frames:
        return min(start_frames)
    else:
        return None


@flush_output
def set_animdata(item, anim_data, start_frame=None):
    """
    Sets animation on component's animation node

    :param item: item to get data from
    :type item: pyfbsdk component

    :param anim_data: dict of data
    :type anim_data: dict

    :param frame_offset: frame offset value
    :type frame_offset: int
    """
    # make sure anim data contains translation and rotation entries
    if not anim_data.get("Translation", None):
        raise RuntimeError("No translation in animation data!")

    if not anim_data.get("Rotation", None):
        raise RuntimeError("No rotation in animation data!")

    # get frame offset
    frame_offset = 0
    anim_start_frame = get_startframe(anim_data)
    if start_frame is not None and anim_start_frame is not None:
        frame_offset = start_frame - anim_start_frame

    # set translation static
    item.Translation = pyfbsdk.FBVector3d(
        [value[0].get("value", 0.0) for value in anim_data["Translation"]])

    for i, value in enumerate(anim_data["Translation"]):
        if not value[0].get("static", False):
            item.Translation.SetAnimated(True)
            trans_anim_node = item.Translation.GetAnimationNode()
            set_curve_data(
                trans_anim_node.Nodes[i].FCurve,
                value,
                frame_offset)

    # set rotation
    item.Rotation = pyfbsdk.FBVector3d(
        [value[0].get("value", 0.0) for value in anim_data["Rotation"]])

    for i, value in enumerate(anim_data["Rotation"]):
        if not value[0].get("static", False):
            item.Rotation.SetAnimated(True)
            rots_anim_node = item.Rotation.GetAnimationNode()
            set_curve_data(
                rots_anim_node.Nodes[i].FCurve,
                value,
                frame_offset)

    LOG.info("Animation set on {0}".format(item.LongName))
