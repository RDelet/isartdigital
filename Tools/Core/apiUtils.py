# coding=ascii

"""
!@Brief Simple api mapping
"""

# ====================================
#   Import Modules
# ====================================

from maya import cmds, OpenMaya


# ====================================
#   Misc functions
# ====================================

def get_object(s_node):

    """
    !@Brief Get MObject from node name.

    @type s_node: string
    @param s_node: Node name.

    @rtype: OpenMaya.MObject
    @return: Maya MObject object.
    """

    if not isinstance(s_node, basestring):
        raise RuntimeError('Node name must be a string not "{0}"'.format(type(s_node)))

    #   Get PyNode in MSelectionList
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(s_node)

    #   Get MDagPath
    m_object = OpenMaya.MObject()
    selection_list.getDependNode(0, m_object)

    return m_object


def get_path(s_node):

    """
    !@Brief Get MDagPath from node name.

    @type s_node: string
    @param s_node: Node name.

    @rtype: OpenMaya.MDagPath
    @return: Maya MDagPath object.
    """

    if not isinstance(s_node, basestring):
        raise RuntimeError('Node name must be a string not "{0}"'.format(type(s_node)))

    #   Get PyNode in MSelectionList
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(s_node)

    #   Get MDagPath
    m_dag_path = OpenMaya.MDagPath()
    selection_list.getDagPath(0, m_dag_path)

    return m_dag_path


def get_plug(s_node):

    """
    !@Brief Get MPlug from node name.

    @type s_node: string
    @param s_node: Node name.

    @rtype: OpenMaya.MPlug
    @return: Maya MPlug object.
    """

    if not isinstance(s_node, basestring):
        raise RuntimeError('Node name must be a string not "{0}"'.format(type(s_node)))

    #   Get PyNode in MSelectionList
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(s_node)

    #   Get MDagPath
    m_plug = OpenMaya.MDagPath()
    selection_list.getPlug(0, m_plug)

    return m_plug


def get_children(mo_node, traversal_type=True, mfn_type=OpenMaya.MFn.kTransform, b_all_descendents=False, b_shape=True):
    
    """
    !@Brief list all descendents children of an object

    @type mo_node: OpenMaya.MObject
    @param mo_node: Root node name.
    @type traversal_type: bool
    @param traversal_type: Type of parsing descendents. Default is True (OpenMaya.MItDag.kBreadthFirst)
    @type mfn_type: OpenMaya.MFn
    @param mfn_type: If you want to surch type of node. Default is all node.
    @type b_all_descendents: bool
    @param b_all_descendents: Get all descendents.
    @type b_shape: bool
    @param b_shape: Get shape.

    @rtype: OpenMaya.MDagPathArray
    @return: list of children.
    """

    moa_childrens = OpenMaya.MObjectArray()

    #   Check
    if isinstance(mo_node, OpenMaya.MObject) is False:
        raise TypeError("Invalid object given. Node must be a MObject not {0}".format(type(mo_node)))

    #   Get node directly below
    if not b_all_descendents:
        mfn_node = OpenMaya.MFnDagNode(mo_node)
        for i in range(mfn_node.childCount()):
            mo_child = mfn_node.child(i)
            if not b_shape and mo_child.hasFn(OpenMaya.MFn.kShape):
                continue
            if not mo_child.hasFn(mfn_type):
                continue
            moa_childrens.append(mo_child)
    #   Get all Descendents
    else:
        #   Get parsing type
        mit_dag_parsing = OpenMaya.MItDag.kBreadthFirst
        if not traversal_type:
            mit_dag_parsing = OpenMaya.MItDag.kDepthFirst
        #   Create Iterator
        it_dag = OpenMaya.MItDag(mit_dag_parsing, mfn_type)
        it_dag.reset(mo_node, mit_dag_parsing, mfn_type)
        #   Parse iterator
        moa_childrens = OpenMaya.MObjectArray()
        while not it_dag.isDone():
            dp_current_item = OpenMaya.MDagPath()
            it_dag.getPath(dp_current_item)
            if dp_current_item.hasFn(mfn_type):
                moa_childrens.append(dp_current_item.node())
            it_dag.next()

    return moa_childrens


def set_namespace(s_namespace, s_parent_namespace=":"):
    
    """
    !@Brief Set maya namespace. If namespace doesn't exists create it.

    @type s_namespace: str / unicode
    @param s_namespace: New namespace
    @type s_parent_namespace: str / unicode
    @param s_parent_namespace: Parent namespace name. Default is ":".

    @rtype: str
    @return: Last namespace.
    """

    if s_namespace is None or s_namespace == "":
        s_namespace = ":"

    m_namespace = OpenMaya.MNamespace()
    s_current_namespace = m_namespace.currentNamespace()
    m_namespace.setCurrentNamespace(s_parent_namespace)

    if m_namespace.namespaceExists(s_namespace) is False:
        m_namespace.addNamespace(s_namespace)
    m_namespace.setCurrentNamespace(s_namespace)

    return s_current_namespace
