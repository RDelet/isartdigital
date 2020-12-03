# coding=ascii

"""
!@Brief Simple node function / operation
"""


# ====================================
#   Import Modules
# ====================================

from maya import cmds, OpenMaya, OpenMayaAnim

import apiUtils


# ====================================
#   Func
# ====================================

def name(mo_node, b_full=True, b_namespace=True):
    
    """
    !@Brief Get node name.

    @type mo_node: OpenMaya.MObject
    @param mo_node: Maya object.
    @type b_full: bool
    @param b_full: If True get fullPath. Default is True.
    @type b_namespace: bool
    @param b_namespace: If True get with namespace. Default is True.

    @rtype: str
    @return: Node name.
    """

    if isinstance(mo_node, OpenMaya.MObject) is False:
        s_msg = "Argument must be a MObject not {0}".format(type(mo_node))
        raise TypeError(s_msg)

    if isinstance(b_full, bool) is False:
        s_msg = "Argument must be a bool not {0}".format(type(b_full))
        raise TypeError(s_msg)

    if mo_node.hasFn(OpenMaya.MFn.kDagNode) is False or b_full is False:
        s_node = OpenMaya.MFnDependencyNode(mo_node).name()
    else:
        s_node = OpenMaya.MFnDagNode(mo_node).fullPathName()

    return s_node if b_namespace is True else s_node.split(":")[-1]


def get_matrix(mo_node, b_exclusive=False, b_inverse=False):
    
    """
    !@Brief Get worldMatrix of object from dagPath.

    @type mo_node: OpenMaya.MObject
    @param mo_node: Transform api object.
    @type b_exclusive: bool
    @param b_exclusive: Get exlusive matrix. Default is False
    @type b_inverse: bool
    @param b_inverse: Get inverse matrix. Default is False

    @rtype: OpenMaya.MMatrix
    @return: Transform worldMatrix.
    """

    #   Check
    if isinstance(mo_node, OpenMaya.MObject) is False:
        raise TypeError("Transform given is invalid. Transform must be a MObject".format(type(mo_node)))

    if mo_node.hasFn(OpenMaya.MFn.kWorld) is True:
        return OpenMaya.MMatrix()

    if mo_node.hasFn(OpenMaya.MFn.kTransform) is False and mo_node.hasFn(OpenMaya.MFn.kJoint) is False:
        raise TypeError("Invalid type given. Driver must be a transform or joint node")

    #   Get dagPath
    mpa_node = OpenMaya.MDagPathArray()
    OpenMaya.MDagPath().getAllPathsTo(mo_node, mpa_node)
    if mpa_node.length() == 0:
        raise Exception("Problem on get dag path of driver node")

    if mpa_node.length() > 1:
        cmds.warning("Multi path found. This transform is instanced. First dag path found getted")

    if b_inverse is False:
        return mpa_node[0].inclusiveMatrix() if b_exclusive is False else mpa_node[0].exclusiveMatrix()
    return mpa_node[0].inclusiveMatrixInverse() if b_exclusive is False else mpa_node[0].exclusiveMatrixInverse()


def create(s_type, s_name, mo_parent=None, s_namespace=None, i_restriction=0):
    
    """
    !@Brief Create node.

    @type s_type: str / unicode
    @param s_type: Node type.
    @type s_name: str / unicode
    @param s_name: Node name.
    @type mo_parent: OpenMaya.MObject
    @param mo_parent: Parent object for dagNode.
    @type s_namespace: str / unicode
    @param s_namespace: With given namespace.
    @type i_restriction: int
    @param i_restriction: ObjectSet restriction.

    @rtype: OpenMaya.MObject
    @return:
    """

    if isinstance(s_name, (str, unicode)) is False:
        raise TypeError("Argument must be a string not {0}".format(type(s_name)))

    if mo_parent is not None:

        if isinstance(mo_parent, OpenMaya.MObject) is False:
            raise Exception("Parent given is invalid. Parent must be an MObject not {0}".format(type(mo_parent)))

        if mo_parent.isNull() is True:
            raise Exception("Parent given object is null.")

        if mo_parent.hasFn(OpenMaya.MFn.kWorld) is True:
            mo_parent = None

        if mo_parent is not None and mo_parent.hasFn(OpenMaya.MFn.kTransform) is False:
            raise Exception("Parent is invalid. Parent node must be a transform not {0}".format(mo_parent.apiTypeStr()))

    #   Set specific namespace
    if s_namespace is not None and s_namespace != "":
        s_namespace = apiUtils.set_namespace(s_namespace)

    #   Create Node
    mdg_mod = OpenMaya.MDGModifier()

    if s_type == 'transform':
        if mo_parent is None:
            mo_node = OpenMaya.MFnTransform().create()
        else:
            mo_node = OpenMaya.MFnTransform().create(mo_parent)
    elif s_type == 'joint':
        if mo_parent is None:
            mo_node = OpenMayaAnim.MFnIkJoint().create()
        else:
            mo_node = OpenMayaAnim.MFnIkJoint().create(mo_parent)
    elif s_type == 'objectSet':
        mo_node = OpenMaya.MFnSet().create(OpenMaya.MSelectionList(), i_restriction)
    else:
        mo_node = OpenMaya.MFnDependencyNode().create(s_type)
        if mo_parent is not None and mo_node.hasFn(OpenMaya.MFn.kTransform):
            mfn_parent = OpenMaya.MFnDagNode(mo_parent)
            mfn_parent.addChild(mo_node)

    mdg_mod.renameNode(mo_node, s_name)
    mdg_mod.doIt()
    del mdg_mod

    #   Restore current namespace
    if s_namespace is not None and s_namespace != "":
        apiUtils.set_namespace(s_namespace)

    return mo_node


def remove(mo_node, b_force=False):
    
    """
    !@Brief Remove given node

    @type mo_node: OpenMaya.MObject
    @param mo_node: Maya object node.
    @type b_force: bool
    @param b_force: Delete locked node.
    """

    if isinstance(mo_node, OpenMaya.MObject) is False:
        raise TypeError("Argument must be a MObject not {0}".format(type(mo_node)))

    if mo_node.hasFn(OpenMaya.MFn.kDagNode) is False and mo_node.hasFn(OpenMaya.MFn.kDependencyNode) is False:
        raise TypeError("Object must be a DagNode or DependencyNode not {0}".format(mo_node.apyTypeStr()))

    moh_node = OpenMaya.MObjectHandle(mo_node)
    if mo_node.isNull() or not moh_node.isValid() or not moh_node.isAlive():
        cmds.debug('Node given does not exists !')
        return

    mfn_node = OpenMaya.MFnDependencyNode(mo_node)
    if mfn_node.isLocked() and b_force is False:
        raise TypeError('Node "{0}" is locked. Set b_force to True for remove it'.format(name(mo_node)))

    if b_force:
        mfn_node.setLocked(False)

    mdg_mod = OpenMaya.MDagModifier() if mo_node.hasFn(OpenMaya.MFn.kDagNode) else OpenMaya.MDGModifier()
    mdg_mod.deleteNode(mo_node)
    mdg_mod.doIt()
    del mdg_mod


def snap(mo_driver, mo_driven):
    
    """
    !@Brief Snap transform node with matrix.

    @type mo_driver: OpenMaya.MObject
    @param mo_driver: Driver api object.
    @type mo_driven: OpenMaya.MObject
    @param mo_driven: Driver api object.
    """

    if isinstance(mo_driver, OpenMaya.MObject) is False:
        s_msg = "Argument must be a MObject not {0}".format(type(mo_driver))
        raise TypeError(s_msg)

    if isinstance(mo_driven, OpenMaya.MObject) is False:
        s_msg = "Argument must be a MObject not {0}".format(type(mo_driven))
        raise TypeError(s_msg)

    if mo_driver.hasFn(OpenMaya.MFn.kDagNode) is False or mo_driven.hasFn(OpenMaya.MFn.kDagNode) is False:
        s_msg = "Impossible to get matrix of DependencyNode -- {0} | {1}".format(mo_driver.apiTypeStr(), mo_driven.apiTypeStr())
        raise TypeError(s_msg)

    mm = get_matrix(mo_driver) * get_matrix(mo_driven, b_exclusive=True).inverse()
    OpenMaya.MFnTransform(mo_driven).set(OpenMaya.MTransformationMatrix(mm))

    mfn_driver = OpenMaya.MFnDependencyNode(mo_driver)
    mfn_driven = OpenMaya.MFnDependencyNode(mo_driver)
    for s_attr in ['rotatePivot', 'rotatePivotTranslate', 'scalePivot', 'scalePivotTranslate']:
        for i in range(3):
            f = mfn_driver.findPlug(s_attr).child(i).asFloat()
            mfn_driven.findPlug(s_attr).child(i).setFloat(f)


def add_shape():
    
    """
    !@Brief Add selected shape to selected transform
    """

    #   check
    a_selected = cmds.ls(selection=True, long=True)
    if a_selected is None and len(a_selected) == 0:
        raise Exception("Select shape node and transform node")

    s_node_type = cmds.nodeType(a_selected[0])
    if s_node_type not in ["mesh", "nurbsSurface", "nurbsCurve"]:
        raise TypeError("First node selected must be a shape not {0}".format(s_node_type))

    s_node_type = cmds.nodeType(a_selected[1])
    if s_node_type not in "transform":
        raise TypeError("First node selected must be a transform not {0}".format(s_node_type))

    #   Add
    cmds.parent(relative=True, shape=True)


def replace_shape():
    
    """
    !@Brief Replace selected shape to selected transform
    """

    #   check
    a_selected = cmds.ls(selection=True, long=True)
    if a_selected is None and len(a_selected) == 0:
        raise Exception("Select shape node and transform node")

    s_node_type = cmds.nodeType(a_selected[0])
    if s_node_type not in ["mesh", "nurbsSurface", "nurbsCurve"]:
        raise TypeError("First node selected must be a shape not {0}".format(s_node_type))

    s_node_type = cmds.nodeType(a_selected[1])
    if s_node_type not in "transform":
        raise TypeError("First node selected must be a transform not {0}".format(s_node_type))

    #   Replace
    a_shapes = cmds.listRelatives(a_selected[1], shapes=True, fullPath=True)
    if a_shapes is not None and len(a_shapes) > 0:
        for s_shape in a_shapes:
            if cmds.getAttr("{0}.intermediateObject".format(s_shape)) is True:
                continue
            cmds.delete(s_shape)

    cmds.parent(relative=True, shape=True)


def average_selection():

    a_selected = cmds.ls(selection=True, long=True, flatten=True)

    mv_pos = OpenMaya.MVector()
    i_num_point = 0

    for s_node in a_selected:
        
        if "." in s_node:
            
            dp_shape = apiUtils.get_path(s_node.split(".")[0])
            if dp_shape.hasFn(OpenMaya.MFn.kShape) is False:
                dp_shape.extendToShape()
            
            i_index = int(s_node.split("[")[-1].split("]")[0])
            mpa_pos = OpenMaya.MPointArray()
            
            if dp_shape.hasFn(OpenMaya.MFn.kMesh) is True:
                mfn_mesh = OpenMaya.MFnMesh(dp_shape)
                mfn_mesh.getPoints(mpa_pos, OpenMaya.MSpace.kWorld)
                mv_pos += OpenMaya.MVector(mpa_pos[i_index])
                i_num_point += 1
            elif dp_shape.hasFn(OpenMaya.MFn.kNurbsSurface) is True:
                mfn_nurbs_surface = OpenMaya.MFnNurbsSurface(dp_shape)
                mfn_nurbs_surface.getCVs(mpa_pos, OpenMaya.MSpace.kWorld)
                mv_pos += OpenMaya.MVector(mpa_pos[i_index])
                i_num_point += 1
            elif dp_shape.hasFn(OpenMaya.MFn.kNurbsCurve) is True:
                mfn_nurbs_curve = OpenMaya.MFnNurbsCurve(dp_shape)
                mfn_nurbs_curve.getCVs(mpa_pos, OpenMaya.MSpace.kWorld)
                mv_pos += OpenMaya.MVector(mpa_pos[i_index])
                i_num_point += 1
            else:
                raise TypeError("Invalid type selected -- {0}".format(dp_shape.node().apiTypeStr()))
        else:
            dp_shape = apiUtils.get_path(s_node)
            if dp_shape.hasFn(OpenMaya.MFn.kTransform) is False:
                dp_shape.pop()
            mm_matrix = dp_shape.inclusiveMatrix()
            mv_pos += OpenMaya.MVector(mm_matrix(3, 0), mm_matrix(3, 1), mm_matrix(3, 2))

    mv_pos /= float(i_num_point)


    s_transform = cmds.createNode("transform", name="AVERAGE_SELECTION", skipSelect=True)
    cmds.setAttr("%s.translateX" % s_transform, mv_pos.x)
    cmds.setAttr("%s.translateY" % s_transform, mv_pos.y)
    cmds.setAttr("%s.translateZ" % s_transform, mv_pos.z)
    cmds.setAttr("%s.displayHandle" % s_transform, True)
