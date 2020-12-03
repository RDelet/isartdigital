# coding=ascii

"""
!@Brief Helpers for animation commands.
"""


# ======================================
#    Import modules
# ======================================

from maya import cmds, OpenMaya, OpenMayaAnim

import apiUtils
import nodeUtils


# ======================================
#    Bake
# ======================================

def bake(a_nodes, **kwargs):

    """
    !@Brief Bake nodes from given time range.

    @type a_nodes: list(str) / OpenMaya.MObjectArray
    @param a_nodes: List of nodes.
    """

    if isinstance(a_nodes, (list, tuple, OpenMaya.MObjectArray)) is False:
        raise TypeError("Arguments must be a list of string or MObjectArray not {0}".format(type(a_nodes)))

    #   Transform MObjectArray to list of names.
    if isinstance(a_nodes, OpenMaya.MObjectArray) is True:
        a_tmp = list()
        for i in range(a_nodes.length()):
            if a_nodes[i].hasFn(OpenMaya.MFn.kTransform) is False:
                raise TypeError("Node must be a transform not {0}".format(a_nodes[i].apiTypeStr()))
            a_tmp.append(OpenMaya.MFnDagNode(a_nodes[i]).fullPathName())
        a_nodes = a_tmp

    # ==================================
    #   Get timeline data

    mt_start = get_time(kwargs.get("f_start"), b_full=kwargs.get("b_full", True))
    mt_end = get_time(kwargs.get("f_end"), b_full=kwargs.get("b_full", True), b_end=True)

    # ==================================
    #   bake

    cmds.undoInfo(openChunk=True)
    cmds.refresh(suspend=True)

    cmds.bakeResults(
        a_nodes,
        time=(mt_start.value(),
        mt_end.value()),
        sampleBy=1,
        simulation=True
    )

    cmds.refresh(suspend=False)
    cmds.undoInfo(closeChunk=True)


def get_time(f_time=None, b_full=True, b_set=False, b_end=False):

    """
    !@Brief Get StartAnimationValue

    @type f_time: float
    @param f_time: Start frame value.
    @type b_full: bool
    @param b_full: If is True get animationStart else get minStart.
    @type b_set: bool
    @param b_set: If True set timeLine if float given is less than start frame.
    @type b_end: bool
    @param b_end: If True get end time else get start time.

    @rtype: OpenMaya.MTime
    @return: Start frame in MTime.
    """

    anim_control = OpenMayaAnim.MAnimControl()
    if b_end is True:
        mt_time = anim_control.animationEndTime() if b_full is True else anim_control.maxTime()
    else:
        mt_time = anim_control.animationStartTime() if b_full is True else anim_control.minTime()

    #   No float given
    if f_time is None:
        return mt_time

    #   Float given
    mt_gtime = OpenMaya.MTime()
    mt_gtime.setUnit(mt_time.unit())
    if isinstance(f_time, OpenMaya.MTime) is True:
        mt_gtime.setValue(f_time.value())
    else:
        mt_gtime.setValue(float(f_time))

    if mt_gtime > mt_time if b_end is True else mt_gtime < mt_time:
        if b_set is True:
            set_time(mt_gtime, b_full=b_full, b_end=b_end)
        else:
            raise Exception("Time given out of time range -- {0} | {1}".format(mt_gtime.value(), mt_time.value()))

    return mt_gtime


def set_time(mt_time, b_full=True, b_end=False):

    """
    !@Brief Set start time

    @type mt_time: OpenMaya.MTime
    @param mt_time: Time value.
    @type b_full: bool
    @param b_full: If is True get animationStart else get minStart.
    @type b_end: bool
    @param b_end: If True set end time else set start time.

    """

    anim_control = OpenMayaAnim.MAnimControl()

    if b_end is True:
        if b_full is True:
            anim_control.setAnimationEndTime(mt_time)
        else:
            anim_control.setMaxTime(mt_time)
    else:
        if b_full is True:
            anim_control.setAnimationStartTime(mt_time)
        else:
            anim_control.setMinTime(mt_time)


def current_time():

    """
    !@Brief Get current frame.

    @rtype: OpenMaya.MTime
    @return: Current frame in MTime.
    """

    return OpenMayaAnim.MAnimControl().currentTime()
