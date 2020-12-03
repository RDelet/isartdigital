# coding=ascii

"""
!@Brief Maya Matrix utils
"""

# ==================================
#   Import Modules
# ==================================

from maya import cmds, OpenMaya


# ==================================
# 
# ==================================

def float_array_to_mmatrix(a_matrix):

    """
    !@Brief Transform list / tuple to MMatrix.

    @type a_matrix: list(float)
    @param a_matrix: List of array datas.

    @rtype: OpenMaya.MMatrix
    @return: Matrix transformed.
    """

    if not isinstance(a_matrix, (list, tuple)):
        raise BaseException("Invalid argument given !!!")

    out_matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(a_matrix, out_matrix)

    return out_matrix
