# ==================================
#   Import Modules
# ==================================

from maya import cmds, OpenMaya

from isartdigital.Tools.Core import apiUtils, matrix


# ==================================
#   Skin Utils
# ==================================

def reset_bind_matrix(a_joints=None):

    """
    !@Brief Reset joint bindPreMatrix.

    @type a_joints: list / tuple
    @param a_joints: List of joint names.
    """

    # Check args
    if not a_joints:
        a_joints = cmds.ls(type='joint', long=True)
    else:
        a_joints = cmds.ls(a_joints, type='joint', long=True)
        if not a_joints:
            raise RuntimeError('Invalid nodes given !')
    # Reset
    for s_joint in a_joints:
        # Retrieve SkinCluster connections
        a_outputs = cmds.listConnections('{0}.worldMatrix[0]'.format(s_joint), type='skinCluster',
                                         source=False, destination=True, plugs=True, connections=True)
        if not a_outputs:
            continue
        # Get BindMatrix
        dp = apiUtils.get_path(s_joint)
        mm = dp.inclusiveMatrixInverse()
        a_matrix = [mm(i, j) for i in range(4) for j in range(4)]
        # Set skinCluster
        for i in range(0, len(a_outputs), 2):
            s_skin, s_attr = a_outputs[i + 1].split('.')
            i_id = int(s_attr.split('[')[-1].split(']')[0])
            cmds.setAttr('{0}.bindPreMatrix[{1}]'.format(s_skin, i_id), a_matrix, type='matrix')
        # Set new BindPose
        mm = dp.inclusiveMatrix()
        a_matrix = [mm(i, j) for i in range(4) for j in range(4)]
        cmds.setAttr('{0}.bindPose'.format(s_joint), a_matrix, type='matrix')


def go_to_bindpose(a_joints=None):

    """
    !@Brief Reset joint bindPreMatrix.

    @type a_joints: list / tuple
    @param a_joints: List of joint names.
    """

    # Check args
    if not a_joints:
        a_joints = cmds.ls(type='joint', long=True)
    else:
        a_joints = cmds.ls(a_joints, type='joint', long=True)
        if not a_joints:
            raise RuntimeError('Invalid nodes given !')
    # Set bindPose
    for s_joint in a_joints:
        dp_joint = apiUtils.get_path(s_joint)
        if not cmds.objExists('{0}.bindPose'.format(s_joint)):
            continue
        a_bindPose = cmds.getAttr('{0}.bindPose'.format(s_joint))
        if not a_bindPose:
            continue
        mm_bindpose = matrix.float_array_to_mmatrix(a_bindPose)
        mm_local = mm_bindpose
        a_parents = cmds.listRelatives(s_joint, parent=True, fullPath=True)
        if a_parents:
            if not cmds.objExists('{0}.bindPose'.format(a_parents[0])):
                continue
            a_bindPose_parent = cmds.getAttr('{0}.bindPose'.format(a_parents[0]))
            if not a_bindPose:
                continue
            mm_bindpose_parent = matrix.float_array_to_mmatrix(a_bindPose_parent)
            mm_local = mm_bindpose * mm_bindpose_parent.inverse()
        OpenMaya.MFnTransform(dp_joint).set(OpenMaya.MTransformationMatrix(mm_local))
