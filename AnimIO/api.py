import pyfbsdk


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
        if comp.Selected and comp.ClassName() not in type_filters:
            selected.append(comp)

    return selected
