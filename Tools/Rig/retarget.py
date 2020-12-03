# coding=ascii

"""
!@Brief Retarget library
"""

# ===========================================
#    Import Mosules
# ===========================================

from maya import mel, cmds, OpenMaya

from PySide2 import QtWidgets

from isartdigital.Tools.Core import apiUtils, nodeUtils, animUtils


# ===========================================
#    Func
# ===========================================

def _constraint(mo_driver, mo_driven):
    
    """
    !@Brief Constrain node.

    @type mo_driver: OpenMaya.MObject
    @param mo_driver: Driver node.
    @type mo_driven: OpenMaya.MObject
    @param mo_driven: Driven node.

    @rtype: OpenMaya.MObject
    @return: Constraint node.
    """

    if not mo_driver.hasFn(OpenMaya.MFn.kTransform) or not mo_driven.hasFn(OpenMaya.MFn.kTransform):
        raise RuntimeError('Node must be a transform not "{0}" | "{1}"'.format(mo_driver.apiTypeStr(), mo_driven.apiTypeStr()))

    mp_translate = OpenMaya.MFnDependencyNode(mo_driven).findPlug('translate')
    mp_rotate = OpenMaya.MFnDependencyNode(mo_driven).findPlug('rotate')
    set_translate = set() if not mp_translate.isLocked() else set(['x', 'y', 'z'])
    set_rotate = set() if not mp_rotate.isLocked() else set(['x', 'y', 'z'])
    for i, s_axis in enumerate('xyz'):
        if  mp_translate.child(i).isLocked():
            set_translate.add(s_axis)
        if  mp_rotate.child(i).isLocked():
            set_rotate.add(s_axis)

    s_node = cmds.parentConstraint(
        nodeUtils.name(mo_driver),
        nodeUtils.name(mo_driven),
        skipRotate=list(set_rotate),
        skipTranslate=list(set_translate)
    )

    return apiUtils.get_object(s_node[0])


def hierarchy(mo_driver, mo_driven):

    """
    !@Brief Retarget hierarchy.

    @type mo_driver: OpenMaya.MObject
    @param mo_driver: Root driver node.
    @type mo_driven: OpenMaya.MObject
    @param mo_driven: Root driven node.

    @rtype: OpenMaya.MObjectArray
    @return: Constraint nodes.
    """

    moa_driver = apiUtils.get_children(mo_driver, mfn_type=OpenMaya.MFn.kJoint, b_all_descendents=True, b_shape=False)
    a_src = [nodeUtils.name(moa_driver[i], b_full=False, b_namespace=False) for i in range(moa_driver.length())]
    moa_driven = apiUtils.get_children(mo_driven, mfn_type=OpenMaya.MFn.kJoint, b_all_descendents=True, b_shape=False)
    moa_constraints = OpenMaya.MObjectArray()

    for i in range(moa_driven.length()):
        s_short = nodeUtils.name(moa_driven[i], b_full=False, b_namespace=False)
        if s_short in a_src:
            moa_constraints.append(_constraint(moa_driver[a_src.index(s_short)], moa_driven[i]))
    
    animUtils.bake(moa_driven)
    cmds.delete([nodeUtils.name(moa_constraints[i]) for i in range(moa_constraints.length())])


def export_fbx(a_nodes=None, s_file_path=None):

    """
    !@Brief Export nodes to FBX.

    @type a_nodes: None / list
    @param a_nodes: List of node to exprot. Is is node get selected.
    @type s_file_path: None / list
    @param s_file_path: Output file path.
    """

    if not a_nodes:
        a_nodes = cmds.ls(selection=True, long=True)
    else:
        if not isinstance(a_nodes, (list, tuple)):
            raise RuntimeError('First argument must be a list not "{0}"'.format(type(a_nodes)))
    
    if not s_file_path:
        s_file_path, _ = QtWidgets.QFileDialog().getSaveFileName(
            parent=None,
            caption="Export As",
            filter="FBX (*.fbx)"
        )
        if not s_file_path:
            raise RuntimeError('No output file getted !')
    
    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya', quiet=True)
    
    try:
        cmds.select(a_nodes, hierarchy=True)
        mel.eval('FBXResetExport')
        mel.eval('FBXExportAnimationOnly -v true')
        mel.eval('FBXExportUpAxis y')
        mel.eval('FBXExportQuaternion -v quaternion')
        mel.eval('FBXExportUseSceneName -v true')
        mel.eval('FBXExportLights -v false')
        mel.eval('FBXExportCameras -v false')
        mel.eval('FBXExportBakeComplexAnimation -v true')
        mel.eval('FBXExport -f "{0}" -s 1'.format(s_file_path))
    except Exception as e:
        raise RuntimeError('Impossible to export node "{0}"'.format(a_nodes))

    print ('File exported to "{0}"'.format(s_file_path))
