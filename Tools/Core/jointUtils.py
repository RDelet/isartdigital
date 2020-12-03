# coding=ascii

"""
!@Brief Simple function for joints
"""

# ===========================================
#    Import Mosules
# ===========================================

from maya import cmds, OpenMaya

import apiUtils
import nodeUtils


# ===========================================
#    Func
# ===========================================


def duplicate_hierarchy(mo_root, mo_parent=None, s_namespace=':'):
    
    """
    !@Brief Duplicate hierarchy from given root node.
    
    @type mo_root: OpenMaya.MObject
    @param mo_root: Root node name.
    @type s_root: OpenMaya.MObject
    @param s_root: parent node.
    @type s_namespace: str / unicode
    @param s_namespace: Duplication namespace.
    
    @rtype: OpenMaya.MObject
    @return: New root node object.
    """
    
    #    Check    
    if not isinstance(mo_root, OpenMaya.MObject):
        raise RuntimeError('Root argument must be a string or MObject not "{0}"'.format(type(mo_root)))
    
    if not mo_root.hasFn(OpenMaya.MFn.kJoint):
        raise RuntimeError('Node given must be a joint not "{0}"'.format(mo_root.apiTypeStr()))
    
    #    Duplicate
    s_short = nodeUtils.name(mo_root, b_full=False, b_namespace=False)
    mo_new_joint = nodeUtils.create('joint', s_short, s_namespace=s_namespace)
    
    if mo_parent:
        mfn_parent = OpenMaya.MFnDagNode(mo_parent)
        mfn_parent.addChild(mo_new_joint)
    
    nodeUtils.snap(mo_root, mo_new_joint)
    
    #    Duplicate Children
    mfn_root = OpenMaya.MFnDagNode(mo_root)
    for i in range(mfn_root.childCount()):
        mo_child = mfn_root.child(i)
        if not mo_child.hasFn(OpenMaya.MFn.kJoint):
            continue
        duplicate_hierarchy(mo_child, mo_parent=mo_new_joint)
    
    return mo_new_joint


def remove_joint_orient(b_lock=False):

    """
    !@Brief Set final rotation on rotation attribute and remove to jointOrient.

    @type b_lock: bool
    @param b_lock: Lock jointOrient
    """

    a_selected = cmds.ls(selection=True, long=True)

    for s_node in a_selected:
        
        a_matrix = cmds.xform(s_node, query=True, matrix=True, worldSpace=True)
        
        cmds.setAttr("{0}.jointOrient".format(s_node), lock=False)
        for s_axis in "XYZ":
            cmds.setAttr("{0}.jointOrient{1}".format(s_node, s_axis), lock=False)
            cmds.setAttr("{0}.jointOrient{1}".format(s_node, s_axis), 0.0, lock=b_lock)
        
        cmds.xform(s_node, matrix=a_matrix, worldSpace=True)
