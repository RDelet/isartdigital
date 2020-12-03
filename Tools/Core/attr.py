# coding=ascii

"""
!@Brief
"""

# ===================================================
#   Import Module
# ===================================================

import logging
import qdMatrix

from maya import cmds, OpenMaya

from CoreScripts.qdHelpers.qdLog import QDLog
from CoreScripts.qdHelpers.qdAttributes import QDAttributeABC, QDAttributeEnum, QDAttribute

qd_logger = QDLog.create_log('QDAttribute')
qd_logger.setLevel(logging.ERROR)


# ===================================================
#   Data
# ===================================================

class _QDNumericAttr(QDAttributeEnum):

    """
    !@Brief Abstract class for Numeric attribute
    """

    def __init__(self, s_name, i_index):
        super(_QDNumericAttr, self).__init__(i_index, s_name)


class _QDTypedAttr(QDAttributeEnum):

    """
    !@Brief Abstract class for Typed attribute
    """

    def __init__(self, s_name, i_index):
        super(_QDTypedAttr, self).__init__(i_index, s_name)


class _QDUnitAttr(QDAttributeEnum):

    """
    !@Brief Abstract class for Unit attribute
    """

    def __init__(self, s_name, i_index):
        super(_QDUnitAttr, self).__init__(i_index, s_name)


class QDTypes(object):

    """
    !@Brief Enum for value type.
    """

    #   Numeric attribute
    kBool = _QDNumericAttr("bool", OpenMaya.MFnNumericData.kBoolean)
    kBool3 = _QDNumericAttr("bool3", OpenMaya.MFnNumericData.kBoolean)
    kChar = _QDNumericAttr("char", OpenMaya.MFnNumericData.kChar)
    kShort = _QDNumericAttr("short", OpenMaya.MFnNumericData.kShort)
    kShort2 = _QDNumericAttr("short2", OpenMaya.MFnNumericData.k2Short)
    kShort3 = _QDNumericAttr("short3", OpenMaya.MFnNumericData.k3Short)
    kLong = _QDNumericAttr("long", OpenMaya.MFnNumericData.kLong)
    kInt = _QDNumericAttr("int", OpenMaya.MFnNumericData.kInt)
    kLong2 = _QDNumericAttr("long2", OpenMaya.MFnNumericData.k2Long)
    kInt2 = _QDNumericAttr("int2", OpenMaya.MFnNumericData.k2Int)
    kLong3 = _QDNumericAttr("long3", OpenMaya.MFnNumericData.k3Long)
    kInt3 = _QDNumericAttr("int3", OpenMaya.MFnNumericData.k3Int)
    kFloat = _QDNumericAttr("float", OpenMaya.MFnNumericData.kFloat)
    kFloat2 = _QDNumericAttr("float2", OpenMaya.MFnNumericData.k2Float)
    kFloat3 = _QDNumericAttr("float3", OpenMaya.MFnNumericData.k3Float)
    kDouble = _QDNumericAttr("double", OpenMaya.MFnNumericData.kDouble)
    kDouble2 = _QDNumericAttr("double2", OpenMaya.MFnNumericData.k2Double)
    kDouble3 = _QDNumericAttr("double3", OpenMaya.MFnNumericData.k3Double)
    kDouble4 = _QDNumericAttr("double4", OpenMaya.MFnNumericData.k4Double)

    #   Typed attribute
    kNumeric = _QDTypedAttr("numeric", OpenMaya.MFnData.kNumeric)
    kString = _QDTypedAttr("string", OpenMaya.MFnData.kString)
    kStringArray = _QDTypedAttr("stringArray", OpenMaya.MFnData.kStringArray)
    kTypedMatrix = _QDTypedAttr("typedMatrix", OpenMaya.MFnData.kMatrix)
    kDoubleArray = _QDTypedAttr("doubleArray", OpenMaya.MFnData.kDoubleArray)
    kIntArray = _QDTypedAttr("intArray", OpenMaya.MFnData.kIntArray)
    kPointArray = _QDTypedAttr("pointArray", OpenMaya.MFnData.kPointArray)
    kVectorArray = _QDTypedAttr("vectorArray", OpenMaya.MFnData.kVectorArray)
    kComponentList = _QDTypedAttr("componentList", OpenMaya.MFnData.kComponentList)

    #   Unit Attribute
    kAngle = _QDUnitAttr("angle", OpenMaya.MFnUnitAttribute.kTime)
    kDistance = _QDUnitAttr("angle", OpenMaya.MFnUnitAttribute.kDistance)
    kTime = _QDUnitAttr("angle", OpenMaya.MFnUnitAttribute.kTime)

    #   Other
    kMessage = QDAttribute("message", OpenMaya.MFn.kMessageAttribute)
    kMatrix = QDAttribute("matrix", OpenMaya.MFn.kMatrixAttribute)
    kEnum = QDAttribute("enum", OpenMaya.MFn.kEnumAttribute)
    kCompound = QDAttribute("compound", OpenMaya.MFn.kCompoundAttribute)


# ===================================================
#   Misc
# ===================================================

def __msu_ptr(s_type):

    """
    !@Brief Create maya short pointer

    @type s_type: str / unicode
    @param s_type: Value type (float, double, in, short).

    @rtype: ptr
    @return: Maya script util pointer.
    """

    msu = OpenMaya.MScriptUtil()

    if s_type == "int" or s_type == "short":
        msu.createFromInt(0)
        if s_type == "int":
            return msu.asIntPtr()
        else:
            return msu.asShortPtr()
    elif s_type == "double":
        msu.createFromDouble(0.0)
        if s_type == "double":
            return msu.asDoublePtr()
        else:
            return msu.asFloatPtr()
    else:
        s_msg = "Invalid type given {0}.\n\tValid type are float, double, in or short".format(s_type)
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def edit_enum_name(mp_attr, value):

    """
    !@Brief Edit enum name

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Plug you want to change.
    @type value: list / tuple
    @param value: List of new enum.
    """

    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(value, (list, tuple)) is False:
        s_msg = "Argument must be a list not {0}".format(type(value))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   ToDo find solution in API
    #   Get node name
    mo_node = mp_attr.node()
    if mo_node.hasFn(OpenMaya.MFn.kDependencyNode) is True:
        s_node = mp_attr.info()
    elif mo_node.hasFn(OpenMaya.MFn.kDagNode) is True:
        s_attr_name = mp_attr.partialName(False, False, False, False, False, True)
        s_node = "{0}.{1}".format(OpenMaya.MFnDagNode(mo_node).fullPathName(), s_attr_name)
    else:
        s_msg = "Node must be a dependencyNode or dagNode not {0}".format(mo_node.apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get new enum names in string
    s_new_names = ""
    for v in value:
        if isinstance(v, (str, unicode)) is False:
            s_msg = "Argument must be a string not {0}".format(type(v))
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        s_new_names += "{0}:".format(v)

    #   Edit attribute
    cmds.addAttr(s_node, edit=True, enumName=s_new_names)


def add_to(
        mo_node, qd_type, s_long, s_short=None, default=None, value=None,
        b_lock=False, b_array=False, b_keyable=True, b_hidden=False, f_min=None, f_max=None, s_type=None):

    """
    !@Brief Create and add attribute to node.
    
    @type mo_node: OpenMaya.MObject
    @param mo_node: Node to add attribute .
    @type qd_type: int / OpenMaya.MFn
    @param qd_type: Maya api type.
    @type s_long: str / unicode
    @param s_long: Attribute longName.
    @type s_short: str / unicode
    @param s_short: Attribute shortName.Default is None and auto generate.
    @type default: unknow
    @param default: Default value.
    @type value: unknow
    @param value: Value to set.
    @type b_lock: bool
    @param b_lock: Lock attribute. Defautl is False.
    @type b_array: bool
    @param b_array: Array attribute. Default is False.
    @type b_keyable: bool
    @param b_keyable: Keyable attribute. Default is True.
    @type b_hidden: bool
    @param b_hidden: Hidden attribute. Default is False
    @type f_min: float
    @param f_min: Minimum value.
    @type f_max: float
    @param f_max: Maximum value.

    @rtype: OpenMaya.MPlug
    @return: New attribute
    """

    #   Check
    if s_type is None:
        if isinstance(mo_node, OpenMaya.MObject) is False:
            s_msg = "Object must be a MObject not {0}".format(type(mo_node))
            qd_logger.error(s_msg)
            raise TypeError(s_msg)

        if mo_node.isNull() is True:
            s_msg = "Object given is null."
            qd_logger.error(s_msg)
            raise Exception(s_msg)

    if isinstance(qd_type, QDAttributeABC) is False:
        s_msg = "TypeId value must be a QDAttributeABC not {0}".format(type(qd_type))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(s_long, (str, unicode)) is False:
        s_msg = "LongName must be a string not {0} | {1}".format(type(s_long), type(s_short))
        qd_logger.error(s_msg)
        raise AttributeError(s_msg)

    #   Build short name if is not given. Else check variable
    if s_short is None:
        s_short = s_long[0].lower()
        for s in s_long[1:]:
            if s.isupper() is True or s.isalnum() is True:
                s_short += s.lower()
    else:
        if isinstance(s_short, (str, unicode)) is False:
            s_msg = "ShortName must be a string not {0} | {1}".format(type(s_long), type(s_short))
            qd_logger.error(s_msg)
            raise AttributeError(s_msg)

    if isinstance(b_lock, bool) is False:
        s_msg = "Lock value must be a bool not {0}".format(type(b_lock))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_keyable, bool) is False:
        s_msg = "Keyable value must be a bool not {0}".format(type(b_keyable))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_array, bool) is False:
        s_msg = "Array value must be a bool not {0}".format(type(b_array))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_hidden, bool) is False:
        s_msg = "Hidden value must be a bool not {0}".format(type(b_hidden))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Check if attribute already exists
    if s_type is None:
        if mo_node.hasFn(OpenMaya.MFn.kDagNode) is True:
            s_node_name = OpenMaya.MFnDagNode(mo_node).fullPathName()
        else:
            s_node_name = OpenMaya.MFnDependencyNode(mo_node).name()

        s_node_long = "{0}.{1}".format(s_node_name, s_long)
        s_node_short = "{0}.{1}".format(s_node_name, s_short)
        if cmds.objExists(s_node_long) is True or cmds.objExists(s_node_short) is True:
            s_msg = "Attribute already exists on this node -- {0} or {1}".format(s_node_long, s_node_short)
            qd_logger.error(s_msg)
            raise Exception(s_msg)

    #   Create
    mfn_attr, mo_attr = create(
        s_long, s_short, qd_type, default=default,
        b_array=b_array, b_keyable=b_keyable, b_hidden=b_hidden, f_min=f_min, f_max=f_max
    )

    #   Add to node
    if s_type is None:
        mfn_dep_node = OpenMaya.MFnDependencyNode(mo_node)
        b_node_lock = mfn_dep_node.isLocked()
        mfn_dep_node.setLocked(False)
        mfn_dep_node.addAttribute(mo_attr, OpenMaya.MFnDependencyNode.kLocalDynamicAttr)
        mfn_dep_node.setLocked(b_node_lock)
        mp_attr = OpenMaya.MPlug(mo_node, mo_attr)
        mp_attr.setLocked(b_lock)
        if value is not None:
            set(mp_attr, value)
        return mp_attr
    else:
        try:
            m_node_class = OpenMaya.MNodeClass(s_type)
            m_node_class.addExtensionAttribute(mo_attr)
        except Exception as e:
            qd_logger.error(e)


def create(
        s_long, s_short, qd_type, default=None,
        b_keyable=True, b_array=False, b_hidden=False, b_writable=True, f_min=None, f_max=None):

    """
    !@Brief Create new attribute

    @type s_long: str / unicode
    @param s_long: Long name of attribute.
    @type s_short: str / unicode
    @param s_short: Short name of attribute.
    @type qd_type: AttrType
    @param qd_type: attribute type id.
    @type default: str / int / float / bool / OpenMaya.MObject
    @param default: Default value of attribute.
    @type b_keyable: bool
    @param b_keyable: set Attribute to keyable. Default is True.
    @type b_array: bool
    @param b_array: set Attribute as array. Default is False.
    @type b_hidden: bool
    @param b_hidden: set Attribute to hidden. Default is False.
    @type b_writable: bool
    @param b_writable: set Attribute to writable. Default is True.
    @type f_min: float
    @param f_min: Minimum value.
    @type f_max: float
    @param f_max: Maximum value.

    @rtype: OpenMaya.MPlug
    @return: New attribute in MPlug
    """

    #   Check
    if isinstance(s_long, (str, unicode)) is False:
        s_msg = "LongName value must be a string not {0}".format(type(s_long))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(s_short, (str, unicode)) is False:
        s_msg = "ShortName value must be a string not {0}".format(type(s_short))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(qd_type, QDAttributeABC) is False:
        s_msg = "TypeId value must be a QDAttributeABC not {0}".format(type(qd_type))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_keyable, bool) is False:
        s_msg = "Keyable value must be a bool not {0}".format(type(b_keyable))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_array, bool) is False:
        s_msg = "Array value must be a bool not {0}".format(type(b_array))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(b_hidden, bool) is False:
        s_msg = "Hidden value must be a bool not {0}".format(type(b_hidden))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Create attribute

    if qd_type == QDTypes.kMessage:

        mfn_attr = OpenMaya.MFnMessageAttribute()
        mo_attr = mfn_attr.create(s_long, s_short)

    elif isinstance(qd_type, _QDTypedAttr) is True:

        mfn_attr = OpenMaya.MFnTypedAttribute()
        if default is not None:
            if isinstance(default, OpenMaya.MObject) is False:
                s_msg = "Invalid default value given -- {0}".format(type(default))
                qd_logger.error(s_msg)
                raise TypeError(s_msg)
            mo_attr = mfn_attr.create(s_long, s_short, qd_type.index, default)
        else:
            mo_attr = mfn_attr.create(s_long, s_short, qd_type.index)

    elif isinstance(qd_type, _QDNumericAttr) is True:

        mfn_attr = OpenMaya.MFnNumericAttribute()
        if default is not None:
            if isinstance(default, (int, float, bool)) is False:
                s_msg = "Invalid default value given -- {0}".format(type(default))
                qd_logger.error(s_msg)
                raise TypeError(s_msg)
            if qd_type.name == "bool3":
                k_bool = OpenMaya.MFnNumericData.kBoolean
                mfn_num_attr_x = OpenMaya.MFnNumericAttribute()
                mo_attr_x = mfn_num_attr_x.create("{0}X".format(s_long), "{0}x".format(s_short), k_bool, default)
                mfn_num_attr_y = OpenMaya.MFnNumericAttribute()
                mo_attr_y = mfn_num_attr_y.create("{0}Y".format(s_long), "{0}x".format(s_short), k_bool, default)
                mfn_num_attr_z = OpenMaya.MFnNumericAttribute()
                mo_attr_z = mfn_num_attr_z.create("{0}Z".format(s_long), "{0}x".format(s_short), k_bool, default)
                mfn_num_attr = OpenMaya.MFnNumericAttribute()
                mo_attr = mfn_num_attr.create(s_long, s_short, mo_attr_x, mo_attr_y, mo_attr_z)
            else:
                mo_attr = mfn_attr.create(s_long, s_short, qd_type.index, default)
        else:
            if qd_type.name == "bool3":
                k_bool = OpenMaya.MFnNumericData.kBoolean
                mfn_num_attr_x = OpenMaya.MFnNumericAttribute()
                mo_attr_x = mfn_num_attr_x.create("{0}X".format(s_long), "{0}x".format(s_short), k_bool)
                mfn_num_attr_y = OpenMaya.MFnNumericAttribute()
                mo_attr_y = mfn_num_attr_y.create("{0}Y".format(s_long), "{0}x".format(s_short), k_bool)
                mfn_num_attr_z = OpenMaya.MFnNumericAttribute()
                mo_attr_z = mfn_num_attr_z.create("{0}Z".format(s_long), "{0}x".format(s_short), k_bool)
                mfn_num_attr = OpenMaya.MFnNumericAttribute()
                mo_attr = mfn_num_attr.create(s_long, s_short, mo_attr_x, mo_attr_y, mo_attr_z)
            else:
                mo_attr = mfn_attr.create(s_long, s_short, qd_type.index)

    elif isinstance(qd_type, _QDUnitAttr) is True:

        mfn_attr = OpenMaya.MFnUnitAttribute()
        if default is not None:
            if isinstance(default, (int, float)) is False:
                s_msg = "Invalid default value given -- {0}".format(type(default))
                qd_logger.error(s_msg)
                raise TypeError(s_msg)
            mo_attr = mfn_attr.create(s_long, s_short, qd_type.index, default)
        else:
            mo_attr = mfn_attr.create(s_long, s_short, qd_type.index)

    elif qd_type == QDTypes.kMatrix:

        mfn_attr = OpenMaya.MFnMatrixAttribute()
        mo_attr = mfn_attr.create(s_long, s_short, OpenMaya.MFnMatrixAttribute.kDouble)

    elif qd_type == QDTypes.kEnum:

        mfn_attr = OpenMaya.MFnEnumAttribute()
        if isinstance(default, int) is False:
            s_msg = "Invalid default value given -- {0}".format(type(default))
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        if default is not None:
            mo_attr = mfn_attr.create(s_long, s_short, default)
        else:
            mo_attr = mfn_attr.create(s_long, s_short)

    elif qd_type == QDTypes.kCompound:

        mfn_attr = OpenMaya.MFnCompoundAttribute()
        mo_attr = mfn_attr.create(s_long, s_short)

    else:
        s_msg = "Type given not implemented yet -- {0}".format(qd_type)
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Set attribute options
    mfn_attr.setKeyable(b_keyable)
    mfn_attr.setArray(b_array)
    mfn_attr.setHidden(b_hidden)
    mfn_attr.setWritable(b_writable)

    #   Set min max
    if isinstance(qd_type, (_QDNumericAttr, _QDUnitAttr)):
        if f_min is not None:
            mfn_attr.setMin(f_min)
        if f_max is not None:
            mfn_attr.setMax(f_max)

    return mfn_attr, mo_attr


def remove(mp_attr):

    """
    !@Brief Remove attribute of maya object.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Plug you want to delete.
    """

    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Node must be an MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    md_node = OpenMaya.MFnDependencyNode(mp_attr.node())
    mp_attr.setLocked(False)
    md_node.removeAttribute(mp_attr.attribute(), OpenMaya.MFnDependencyNode.kLocalDynamicAttr)


def exists(mo_node, s_attribute):

    """
    !@Brief Check if attribute exists.

    @type mo_node: OpenMaya.MObject
    @param mo_node: Maya node api object or dag object.
    @type s_attribute: str / unciode
    @param s_attribute: Attribute name.

    @rtype: bool
    @return: True if attribute exists else False.
    """

    #   Check arguments
    if isinstance(mo_node, OpenMaya.MObject) is False:
        s_msg = "Object given is invalid. Object must be an MObject not {0}".format(type(mo_node))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if mo_node.isNull() is True:
        s_msg = "Object given is null."
        qd_logger.error(s_msg)
        raise Exception(s_msg)

    if isinstance(s_attribute, (str, unicode)) is False:
        s_msg = "Attribute given is invalid. Attribute must be a string not {0}".format(type(mo_node))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Check attribute
    mfn_node = OpenMaya.MFnDependencyNode(mo_node)
    try:
        mfn_node.findPlug(s_attribute)
        return True
    except Exception as e:
        s_msg = "Attribute doesn't exists -- {0}.{1}\n\t{2}".format(mfn_node.name(), s_attribute, e)
        qd_logger.debug(s_msg)
        return False


def string_to_mplug(mo_node, s_attr):

    """
    !@Brief Retrieve MPlug from string attribute.

    @type mo_node: OpenMaya.MObject.
    @param mo_node: Node object.
    @type s_attr: str / unicode
    @param s_attr: String attribute

    @rtype: OpenMaya.MPlug
    @return: MPlug found
    """

    if isinstance(mo_node, OpenMaya.MObject) is False:
        s_msg = "Node must be a MObject not {0}".format(type(mo_node))
        raise TypeError(s_msg)

    if isinstance(s_attr, (str, unicode)) is False:
        s_msg = "Node must be a MObject not {0}".format(type(s_attr))
        raise TypeError(s_msg)

    return OpenMaya.MFnDependencyNode(mo_node).findPlug(s_attr)


def connect(*args, **kwargs):

    """
    !@Brief Connect two plugs
    """

    mdg_mod = OpenMaya.MDGModifier()

    #   Check argument
    if len(args) == 2:
        mp_source = args[0]
        mp_destination = args[1]
    elif len(args) == 4:
        mp_source = retrieve(args[0], args[1])
        mp_destination = retrieve(args[2], args[3])
    else:
        s_msg = "Invalid argument given. Valid declaration are:"
        s_msg += "\n\tmp_source, mp_destination"
        s_msg += "\n\tmp_source, s_source_attr, mp_destination, s_destination_attr"
        raise Exception(s_msg)

    #   Check object
    if isinstance(mp_source, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_source))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(mp_destination, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_destination))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Disconnect attribut if already connected
    if mp_destination.isConnected() is True:
        if kwargs.get("b_force_connection", True) is True:
            mpa_inputs = get_connected(mp_destination, b_outputs=False)
            if mpa_inputs.length() > 0:
                mdg_mod.disconnect(mpa_inputs[0], mp_destination)
        else:
            s_msg = "Attribute already connected {0}".format(mp_destination.info())
            qd_logger.error(s_msg)
            raise Exception(s_msg)

    #   Unlock attribute
    if kwargs.get("b_force", True) is True and mp_destination.isLocked() is True:
        mp_destination.setLocked(False)

    #   Connect attribute
    mdg_mod.connect(mp_source, mp_destination)

    mdg_mod.doIt()
    del mdg_mod


def disconnect(*args, **kwargs):

    """
    !@Brief Disconnect two plugs
    """

    #   Check argument
    if len(args) == 2:
        mp_source = args[0]
        mp_destination = args[1]
    elif len(args) == 4:
        mp_source = retrieve(args[0], args[1])
        mp_destination = retrieve(args[2], args[3])
    else:
        s_msg = "Invalid argument given. Valid declaration are:"
        s_msg += "\n\tmp_source, mp_destination"
        s_msg += "\n\tmp_source, s_source_attr, mp_destination, s_destination_attr"
        raise Exception(s_msg)

    #   Check object
    if isinstance(mp_source, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_source))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(mp_destination, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_destination))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Disconnect attribut if already connected
    if mp_destination.isConnected() is False:
        return

    mpa_inputs = get_connected(mp_destination, b_outputs=False)
    if mpa_inputs.length() == 0:
        return

    #   Unlock attribute
    if kwargs.get("b_force", True) is True and mp_destination.isLocked() is True:
        mp_destination.setLocked(False)

    #   Connect attribute
    mdg_mod = OpenMaya.MDGModifier()
    mdg_mod.disconnect(mp_source, mp_destination)
    mdg_mod.doIt()
    del mdg_mod


def transfert_connection(mo_source, mo_destination, b_disconnect_input=False):

    """
    !@Brief

    @type mo_source: OpenMaya.MObject
    @param mo_source: Source node for transfert attribute
    @type mo_destination: OpenMaya.MObject
    @param mo_destination: Destination node for connect attribute
    @type b_disconnect_input: bool
    @param b_disconnect_input: Disconnect attribute of source node after transfert.
    """

    for s_attr in ["translate", "rotate", "scale"]:

        #   ToDo: Works with parent plug

        for s_axis in "XYZ":

            s_full_attr = "{0}{1}".format(s_attr, s_axis)

            mpa_inputs = get_connected(mo_source, s_full_attr, b_outputs=False)
            if mpa_inputs.length() > 0:
                connect(mpa_inputs[0], retrieve(mo_destination, s_full_attr))

                #   Disconnect input after transfert.
                #   Disconnect only if input isn't an Expression.
                if b_disconnect_input is True:

                    mp = retrieve(mo_source, s_full_attr)
                    mit_dep_graph = OpenMaya.MItDependencyGraph(
                        mp,
                        OpenMaya.MFn.kExpression,
                        OpenMaya.MItDependencyGraph.kUpstream,
                        OpenMaya.MItDependencyGraph.kBreadthFirst,
                        OpenMaya.MItDependencyGraph.kPlugLevel
                    )

                    b_found = False
                    while mit_dep_graph.isDone() is False:
                        if mit_dep_graph.currentItem().hasFn(OpenMaya.MFn.kExpression) is True:
                            b_found = True
                        mit_dep_graph.next()

                    if b_found is False:
                        disconnect(mpa_inputs[0], mp)


def get_connected(*args, **kwargs):

    """
    !@Brief Get connected plug from given plug.

    @rtype: OpenMaya.MPlugArray
    @return: List of connected plugs
    """

    #   Check
    if len(args) == 1:
        if isinstance(args[0], OpenMaya.MPlug) is False:
            s_msg = "Argument must be a MPlug not {0}".format(type(args[0]))
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mplug = args[0]
    elif len(args) == 2:
        mplug = retrieve(args[0], args[1])
    else:
        s_msg = "Invalid number or argument given."
        qd_logger.error(s_msg)
        raise Exception(s_msg)

    #   Get
    mpa_output = OpenMaya.MPlugArray()
    mpa_connected = OpenMaya.MPlugArray()
    mpa_getter = OpenMaya.MPlugArray()

    if isinstance(mplug, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mplug))
        qd_logger.error(s_msg)
        raise RuntimeError(s_msg)

    if mplug.isConnected() is False and kwargs.get("b_recurse", True):
        #   Recurse on array attribute
        if mplug.isArray() is True:
            for i in range(mplug.numElements()):
                mpa_connected.append(mplug.elementByLogicalIndex(i))
        #   Recurse on compound attribute
        elif mplug.isCompound() is True:
            for i in range(mplug.numChildren()):
                mpa_connected.append(mplug.child(i))
        else:
            return mpa_output
    else:
        mpa_connected.append(mplug)

    for i in range(mpa_connected.length()):

        mpa_getter.clear()
        b_found = mpa_connected[i].connectedTo(mpa_getter, kwargs.get("b_inputs", True), kwargs.get("b_outputs", True))
        if b_found is False:
            continue

        for j in range(mpa_getter.length()):
            mpa_output.append(mpa_getter[j])

    return mpa_output


def connected_plugs(mo_node):

    """
    !@Brief Get all connected plugs.

    @type mo_node: OpenMaya.MObject
    @param mo_node: Node for get connected plugs.

    @rtype: list
    @return: List of (source, destination).
    """

    if isinstance(mo_node, OpenMaya.MObject) is False:
        s_msg = 'Argument must be a MObject not "{0}"'.format(type(mo_node))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    mpa_connected = OpenMaya.MPlugArray()
    try:
        OpenMaya.MFnDependencyNode(mo_node).getConnections(mpa_connected)
    except Exception as e:
        qd_logger.debug(e)
        qd_logger.debug('No connections was found on "{0}" !'.format(OpenMaya.MFnDependencyNode(mo_node).name()))

    a_connected = list()
    for i in range(mpa_connected.length()):
        mp = mpa_connected[i]
        if mp.isDestination():
            a_connected.append((mp.source(), mp))
        else:
            mpa_destination = OpenMaya.MPlugArray()
            mp.destinations(mpa_destination)
            for j in range(mpa_destination.length()):
                a_connected.append((mp, mpa_destination[j]))

    return a_connected


def get_first_free(mp):

    """
    !@Brief Get last index of MPlug array.

    @type mp: OpenMaya.MPlug
    @param mp: MPlug instance.

    @rtype: OpenMaya.MPlug
    @return: First plug free.
    """

    if isinstance(mp, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if mp.isArray() is False:
        s_msg = "Plug given is not array"
        qd_logger.error(s_msg)
        raise RuntimeError(s_msg)

    i = 0
    while True:

        mp_elem = mp.elementByLogicalIndex(i)
        if mp_elem.isNull() is True or mp_elem.isConnected() is False:
            return mp_elem

        if mp_elem.isCompound():
            b_pass = False
            for j in range(mp_elem.numChildren()):
                if mp_elem.child(j).isConnected() is True:
                    b_pass = True
                    break
            if b_pass is False:
                return mp_elem

        i += 1


def retrieve(mo_node, s_attr):

    """
    !@Brief Retrieve MPlug.

    @type mo_node: OpenMaya.MObject
    @param mo_node: Node contain attribute.
    @type s_attr: str / unicode
    @param s_attr: Attribute name.

    @rtype: OpenMaya.MPlug
    @return: MPlug getted.
    """

    #   Check arguments
    if isinstance(mo_node, OpenMaya.MObject) is False:
        s_msg = "Object must be an MObject not {0}".format(type(mo_node))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if mo_node.isNull() is True:
        s_msg = "Object given is null."
        qd_logger.error(s_msg)
        raise Exception(s_msg)

    if isinstance(s_attr, (str, unicode)) is False:
        s_msg = "Attribute must be a string not {0}".format(type(s_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Check attribute
    md_node = OpenMaya.MFnDependencyNode(mo_node)
    try:
        return md_node.findPlug(s_attr)
    except Exception as e:
        s_msg = "{0}\nAttribute doesn't exists {1}.{2}".format(e, md_node.name(), s_attr)
        qd_logger.error(s_msg)
        raise Exception(s_msg)


def hide(*args, **kwargs):

    """
    !@Brief Hide and lock attribute.
            Default attribute is locked to. Set b_lock at False for don't lock attribute.
    """

    #   Check
    if len(args) == 1:
        mp = args[0]
        if isinstance(mp, OpenMaya.MPlug) is False:
            s_msg = "Argument must be a MPlug not {0}".format(type(mp))
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
    elif len(args) == 2:
        mp = retrieve(args[0], args[1])
    else:
        s_msg = "Wrong number of argument. Give MPlug or MObject and attribute name"
        qd_logger.error(s_msg)
        raise Exception(s_msg)

    #   Lock
    mp.setLocked(kwargs.get("b_lock", True))

    #   Hide
    if mp.isCompound():
        for i in range(mp.numChildren()):
            mp.child(i).setKeyable(kwargs.get("b_hide", False))
            mp.child(i).setChannelBox(kwargs.get("b_hide", False))
    else:
        mp.setKeyable(kwargs.get("b_hide", False))
        mp.setChannelBox(kwargs.get("b_hide", False))


def unhide(*args, **kwargs):

    """
    !@Brief Unhide and unlock attribute.
            Default attribute is unlocked to. Set b_lock at True for keep locked attribute.
    """

    kwargs.update({"b_lock": True, "b_hide": True})
    return hide(*args, **kwargs)


# ===================================================
#   Getter
# ===================================================

def get(*args):

    """
    !@Brief Get attribute type.

    @rtype: python value
    @return: Attribute value
    """

    #   Parse argument
    if len(args) == 1:

        if isinstance(args[0], OpenMaya.MPlug) is False:
            s_msg = "First Argument must be a MPlug not {0}".format(args[0])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)

        mp_attr = args[0]

    elif len(args) == 2:

        if isinstance(args[0], OpenMaya.MObject) is False:
            s_msg = "First Argument must be a MObject not {0}".format(args[0])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)

        if isinstance(args[1], (str, unicode)) is False:
            s_msg = "Second Argument must be a string not {0}".format(args[0])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)

        mp_attr = OpenMaya.MFnDependencyNode(args[0]).findPlug(args[1])

    else:

        s_msg = "Invalid number of argument.\n\tMPlug, value\n\tMObject, string attr, value"
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   If value is an array
    if mp_attr.isArray() is True:
        a_value = list()
        for i in range(mp_attr.numElements()):
            a_value.append(get(mp_attr.elementByLogicalIndex(i)))
        return a_value

    if mp_attr.isCompound() is True:
        a_value = list()
        for i in range(mp_attr.numChildren()):
            a_value.append(get(mp_attr.child(i)))
        return a_value

    #   Else
    mo_attr = mp_attr.attribute()
    if mo_attr.hasFn(OpenMaya.MFn.kNumericAttribute) is True:
        return __get_numeric(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kTypedAttribute) is True:
        return __get_typed(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kUnitAttribute) is True:
        return __get_unit(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kMatrixAttribute) is True:
        return __get_matrix(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kFloatMatrixAttribute) is True:
        return __get_matrix(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kEnumAttribute) is True:
        return __get_enum(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kCompoundAttribute) is True:
        return __get_compound(mp_attr)
    elif mo_attr.hasFn(OpenMaya.MFn.kMessageAttribute) is True:
        s_msg = "Impossible to get message attribute"
        qd_logger.error(s_msg)
        raise TypeError(s_msg)
    else:
        s_msg = "Invalid plug type given -- {0}".format(mo_attr.apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __get_typed(mp_attr):

    """
    !@Brief Get typed attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mfn_attr = OpenMaya.MFnTypedAttribute(mp_attr.attribute())
    i_type = mfn_attr.attrType()

    if i_type == OpenMaya.MFnData.kNumeric:
        return __get_numeric(mp_attr)
    elif i_type == OpenMaya.MFnData.kString:
        return mp_attr.asString()
    elif i_type == OpenMaya.MFnData.kStringArray:
        raise OpenMaya.MFnArrayAttrsData(mp_attr.asMObject()).stringArray()
    elif i_type == OpenMaya.MFnData.kMatrix:
        return __get_matrix(mp_attr)
    elif i_type == OpenMaya.MFnData.kDoubleArray:
        return OpenMaya.MFnDoubleArrayData(mp_attr.asMObject()).array()
    elif i_type == OpenMaya.MFnData.kFloatArray:
        return OpenMaya.MFnFloatArrayData(mp_attr.asMObject()).array()
    elif i_type == OpenMaya.MFnData.kIntArray:
        return OpenMaya.MFnIntArrayData(mp_attr.asMObject()).array()
    elif i_type == OpenMaya.MFnData.kPointArray:
        return OpenMaya.MFnPointArrayData(mp_attr.asMObject()).array()
    elif i_type == OpenMaya.MFnData.kVectorArray:
        return OpenMaya.MFnVectorArrayData(mp_attr.asMObject()).array()
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __get_numeric(mp_attr):

    """
    !@Brief Get numeric attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mfn_attr = OpenMaya.MFnNumericAttribute(mp_attr.attribute())
    i_type = mfn_attr.unitType()

    if i_type == OpenMaya.MFnNumericData.kBoolean:
        return mp_attr.asBool()
    elif i_type == OpenMaya.MFnNumericData.kByte:
        return
    elif i_type == OpenMaya.MFnNumericData.kChar:
        return mp_attr.asChar()
    elif i_type == OpenMaya.MFnNumericData.kShort:
        return mp_attr.asShort()
    elif i_type == OpenMaya.MFnNumericData.k2Short:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("short")
        ptr_v2 = __msu_ptr("short")
        mfn_data.getData2Short(ptr_v1, ptr_v2)
        msu = OpenMaya.MScriptUtil()
        return msu.getShort(ptr_v1), msu.getShort(ptr_v2)
    elif i_type == OpenMaya.MFnNumericData.k3Short:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("short")
        ptr_v2 = __msu_ptr("short")
        ptr_v3 = __msu_ptr("short")
        mfn_data.getData3Short(ptr_v1, ptr_v2, ptr_v3)
        msu = OpenMaya.MScriptUtil()
        return msu.getShort(ptr_v1), msu.getShort(ptr_v2), msu.getShort(ptr_v3)
    elif i_type == OpenMaya.MFnNumericData.kAddr:
        return
    elif i_type == OpenMaya.MFnNumericData.kInt:
        return mp_attr.asInt()
    elif i_type == OpenMaya.MFnNumericData.k2Int:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("int")
        ptr_v2 = __msu_ptr("int")
        mfn_data.getData2Int(ptr_v1, ptr_v2)
        msu = OpenMaya.MScriptUtil()
        return msu.getInt(ptr_v1), msu.getInt(ptr_v2)
    elif i_type == OpenMaya.MFnNumericData.k3Int:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("int")
        ptr_v2 = __msu_ptr("int")
        ptr_v3 = __msu_ptr("int")
        mfn_data.getData3Int(ptr_v1, ptr_v2, ptr_v3)
        msu = OpenMaya.MScriptUtil()
        return msu.getInt(ptr_v1), msu.getInt(ptr_v2), msu.getInt(ptr_v3)
    elif i_type == OpenMaya.MFnNumericData.kFloat:
        return mp_attr.asFloat()
    elif i_type == OpenMaya.MFnNumericData.k2Float:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("float")
        ptr_v2 = __msu_ptr("float")
        mfn_data.getData2Float(ptr_v1, ptr_v2)
        msu = OpenMaya.MScriptUtil()
        return msu.getFloat(ptr_v1), msu.getFloat(ptr_v2)
    elif i_type == OpenMaya.MFnNumericData.k3Float:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("float")
        ptr_v2 = __msu_ptr("float")
        ptr_v3 = __msu_ptr("float")
        mfn_data.getData3Float(ptr_v1, ptr_v2, ptr_v3)
        msu = OpenMaya.MScriptUtil()
        return msu.getFloat(ptr_v1), msu.getFloat(ptr_v2), msu.getFloat(ptr_v3)
    elif i_type == OpenMaya.MFnNumericData.kDouble:
        return mp_attr.asDouble()
    elif i_type == OpenMaya.MFnNumericData.k2Double:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("double")
        ptr_v2 = __msu_ptr("double")
        mfn_data.getData2Double(ptr_v1, ptr_v2)
        msu = OpenMaya.MScriptUtil()
        return msu.getDouble(ptr_v1), msu.getDouble(ptr_v2)
    elif i_type == OpenMaya.MFnNumericData.k3Double:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("double")
        ptr_v2 = __msu_ptr("double")
        ptr_v3 = __msu_ptr("double")
        mfn_data.getData3Double(ptr_v1, ptr_v2, ptr_v3)
        msu = OpenMaya.MScriptUtil()
        return msu.getDouble(ptr_v1), msu.getDouble(ptr_v2), msu.getDouble(ptr_v3)
    elif i_type == OpenMaya.MFnNumericData.k4Double:
        mfn_data = OpenMaya.MFnNumericData(mp_attr.asMObject())
        ptr_v1 = __msu_ptr("double")
        ptr_v2 = __msu_ptr("double")
        ptr_v3 = __msu_ptr("double")
        ptr_v4 = __msu_ptr("double")
        mfn_data.getData4Double(ptr_v1, ptr_v2, ptr_v3, ptr_v4)
        msu = OpenMaya.MScriptUtil()
        return msu.getDouble(ptr_v1), msu.getDouble(ptr_v2), msu.getDouble(ptr_v3), msu.getDouble(ptr_v4)
    elif i_type == OpenMaya.MFnNumericData.kInvalid:
        s_msg = "kInvalid type not implemented yet -- {0}".format(mp_attr.info())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __get_unit(mp_attr):

    """
    !@Brief Get unit attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: float
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mfn_attr = OpenMaya.MFnUnitAttribute(mp_attr.attribute())
    i_type = mfn_attr.unitType()

    if i_type == OpenMaya.MFnUnitAttribute.kAngle:
        return mp_attr.asMAngle().value()
    elif i_type == OpenMaya.MFnUnitAttribute.kDistance:
        return mp_attr.asMDistance().value()
    elif i_type == OpenMaya.MFnUnitAttribute.kTime:
        return mp_attr.asMTime().value()
    elif i_type == OpenMaya.MFnUnitAttribute.kInvalid:
        s_msg = "kInvalid type not implemented yet -- {0}".format(mp_attr.info())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __get_matrix(mp_attr):

    """
    !@Brief Get matrix attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mfn_matrix_data = OpenMaya.MFnMatrixData(mp_attr.asMObject())
    return mfn_matrix_data.matrix()


def __get_enum(mp_attr):

    """
    !@Brief Get enum attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    return mp_attr.asInt()


def __get_compound(mp_attr):

    """
    !@Brief Get compound attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.

    @rtype: list
    @return: list of attributes values.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mfn_attr = OpenMaya.MFnCompoundAttribute(mp_attr.attribute())
    a_value = list()
    for i in range(mfn_attr.numChildren()):

        #   Get children plug.
        #   Get from MFnCompoundAttribute because MPlug.child() return networked plug
        mp_child = OpenMaya.MPlug(mp_attr.node(), mfn_attr.child(i))
        if mp_child.attribute().hasFn(OpenMaya.MFn.kMessageAttribute) is True:
            return None
        else:
            returned = get(mp_child)

        if isinstance(returned, (list, tuple)) is True:
            a_value.extend(returned)
        else:
            a_value.append(returned)

    return a_value


# ===================================================
#   Setter
# ===================================================

def set(*args, **kwargs):

    """
    !@Brief Set maya attribute
    """

    #   Parse argument
    if len(args) == 2:
        if isinstance(args[0], OpenMaya.MPlug) is False:
            s_msg = "First Argument must be a MPlug not {0}".format(args[0])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr = args[0]
        value = args[1]
    elif len(args) == 3:
        if isinstance(args[0], OpenMaya.MObject) is False:
            s_msg = "First Argument must be a MObject not {0}".format(args[0])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        if isinstance(args[1], (str, unicode)) is False:
            s_msg = "Second Argument must be a string not {0}".format(args[1])
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr = OpenMaya.MFnDependencyNode(args[0]).findPlug(args[1])
        value = args[2]
    else:
        s_msg = "Invalid number of argument.\n\tMPlug, value\n\tMObject, string attr, value"
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Mplug for unlock
    b_locked = mp_attr.isLocked()
    mp_attr.setLocked(False)

    #   If plug is an array
    if mp_attr.isArray() is True or mp_attr.isCompound() is True:
        if kwargs.get("i_index", None) is not None:
            if mp_attr.isArray() and mp_attr.isCompound() is False:
                set(mp_attr.elementByLogicalIndex(kwargs["i_index"]), value)
            else:
                set(mp_attr.child(kwargs["i_index"]), value)
        else:
            if mp_attr.isArray() is True:
                if isinstance(value, (list, tuple)) is False:
                    value = [value]
                for i in range(len(value)):
                    set(mp_attr.elementByLogicalIndex(i), value[i])
            else:
                for i in range(mp_attr.numChildren()):
                    set(mp_attr.child(i), value[i])
    else:
        try:
            mo_attr = mp_attr.attribute()
            if mo_attr.hasFn(OpenMaya.MFn.kNumericAttribute) is True:
                __set_numeric(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kTypedAttribute) is True:
                __set_typed(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kUnitAttribute) is True:
                __set_unit(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kMatrixAttribute) is True:
                __set_matrix(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kFloatMatrixAttribute) is True:
                __set_matrix(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kEnumAttribute) is True:
                __set_enum(mp_attr, value)
            elif mo_attr.hasFn(OpenMaya.MFn.kCompoundAttribute) is True:
                mp_attr.setLocked(b_locked)
                s_msg = "Impossible to set compound attribute -- {0}".format(mp_attr.info())
                qd_logger.error(s_msg)
                raise Exception(s_msg)
            elif mo_attr.hasFn(OpenMaya.MFn.kMessageAttribute) is True:
                mp_attr.setLocked(b_locked)
                s_msg = "Impossible to set message attribute"
                qd_logger.error(s_msg)
                raise TypeError(s_msg)
            else:
                mp_attr.setLocked(b_locked)
                s_msg = "Invalid plug type given -- {0}".format(mo_attr.apiTypeStr())
                qd_logger.error(s_msg)
                raise TypeError(s_msg)

        except Exception as e:
            qd_logger.error(e)
            raise Exception(e)

    #   restore locked value
    mp_attr.setLocked(b_locked)


def __set_typed(mp_attr, value):

    """
    !@Brief Get typed attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.
    @type value: unknow
    @param value: New attribute value.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Set
    mfn_attr = OpenMaya.MFnTypedAttribute(mp_attr.attribute())
    i_type = mfn_attr.attrType()

    if i_type == OpenMaya.MFnData.kNumeric:
        __set_numeric(mp_attr, value)
    elif i_type == OpenMaya.MFnData.kString:
        if isinstance(value, (str, unicode)) is False:
            s_msg = "Argument must be a string not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setString(str(value))
    elif i_type == OpenMaya.MFnData.kStringArray:
        s_msg = "Set stringArray not implemented yet. {0}".format(mp_attr.info())
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnData.kMatrix:
        if isinstance(value, OpenMaya.MMatrix) is False:
            s_msg = "Argument must be a MMatrix not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        __set_matrix(mp_attr, value)
    elif i_type == OpenMaya.MFnData.kDoubleArray:
        if isinstance(value, OpenMaya.MDoubleArray) is False:
            s_msg = "Argument must be a MDoubleArray not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mfn_data = OpenMaya.MFnDoubleArrayData()
        mfn_data.set(value)
        mp_attr.setMObject(mfn_data.create())
    elif i_type == OpenMaya.MFnData.kFloatArray:
        if isinstance(value, OpenMaya.MFloatArray) is False:
            s_msg = "Argument must be a MFloatArray not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mfn_data = OpenMaya.MFnFloatArrayData()
        mfn_data.set(value)
        mp_attr.setMObject(mfn_data.create())
    elif i_type == OpenMaya.MFnData.kIntArray:
        if isinstance(value, OpenMaya.MIntArray) is False:
            s_msg = "Argument must be a MIntArray not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mfn_data = OpenMaya.MFnIntArrayData()
        mfn_data.set(value)
        mp_attr.setMObject(mfn_data.create())
    elif i_type == OpenMaya.MFnData.kPointArray:
        if isinstance(value, OpenMaya.MPointArray) is False:
            s_msg = "Argument must be a MPointArray not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mfn_data = OpenMaya.MFnPointArrayData()
        mfn_data.set(value)
        mp_attr.setMObject(mfn_data.create())
    elif i_type == OpenMaya.MFnData.kVectorArray:
        if isinstance(value, OpenMaya.MVectorArray) is False:
            s_msg = "Argument must be a MVectorArray not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mfn_data = OpenMaya.MFnVectorArrayData()
        mfn_data.set(value)
        mp_attr.setMObject(mfn_data.create())
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __set_numeric(mp_attr, value):

    """
    !@Brief Get numeric attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.
    @type value: unknow
    @param value: New attribute value.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Set
    mfn_attr = OpenMaya.MFnNumericAttribute(mp_attr.attribute())
    i_type = mfn_attr.unitType()

    if i_type == OpenMaya.MFnNumericData.kBoolean:
        if isinstance(value, bool) is False:
            s_msg = "Argument must be a bool not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setBool(value)
    elif i_type == OpenMaya.MFnNumericData.kByte:
        if isinstance(value, int) is False:
            s_msg = "Argument must be a int not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setInt(value)
    elif i_type == OpenMaya.MFnNumericData.kChar:
        if isinstance(value, (str, unicode)) is False:
            s_msg = "Argument must be a string not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setChar(value)
    elif i_type == OpenMaya.MFnNumericData.kShort:
        if isinstance(value, int) is False:
            s_msg = "Argument must be a int not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setShort(value)
    elif i_type == OpenMaya.MFnNumericData.k2Short:
        s_msg = "Set k2Short not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.k3Short:
        s_msg = "Set k3Short not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.kAddr:
        return
    elif i_type == OpenMaya.MFnNumericData.kInt or i_type == OpenMaya.MFnNumericData.kLong:
        if isinstance(value, int) is False:
            s_msg = "Argument must be a int not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setInt(value)
    elif i_type == OpenMaya.MFnNumericData.k2Int or i_type == OpenMaya.MFnNumericData.k2Long:
        s_msg = "Set k2Int not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.k3Int or i_type == OpenMaya.MFnNumericData.k3Long:
        s_msg = "Set k3Int not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.kFloat:
        if isinstance(value, (int, float)) is False:
            s_msg = "Argument must be a float not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setFloat(value)
    elif i_type == OpenMaya.MFnNumericData.k2Float:
        s_msg = "Set k2Float not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.k3Float:
        s_msg = "Set k3Float not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.kDouble:
        if isinstance(value, (int, float)) is False:
            s_msg = "Argument must be a float not {0}".format(value)
            qd_logger.error(s_msg)
            raise TypeError(s_msg)
        mp_attr.setDouble(value)
    elif i_type == OpenMaya.MFnNumericData.k2Double:
        s_msg = "Set k2Double not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.k3Double:
        s_msg = "Set k3Double not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.k4Double:
        s_msg = "Set k4Double not implemented yet."
        qd_logger.error(s_msg)
        raise NotImplementedError(s_msg)
    elif i_type == OpenMaya.MFnNumericData.kInvalid:
        s_msg = "kInvalid type not implemented yet -- {0}".format(mp_attr.info())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __set_unit(mp_attr, value):

    """
    !@Brief Get unit attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.
    @type value: unknow
    @param value: New attribute value.

    @rtype: float
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(value, (int, float)) is False:
        s_msg = "Argument must be a float not {0}".format(value)
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Set
    mfn_attr = OpenMaya.MFnUnitAttribute(mp_attr.attribute())
    i_type = mfn_attr.unitType()

    if i_type == OpenMaya.MFnUnitAttribute.kAngle:
        mp_attr.setMAngle(OpenMaya.MAngle(value, OpenMaya.MAngle().uiUnit()))
    elif i_type == OpenMaya.MFnUnitAttribute.kDistance:
        mp_attr.setMDistance(OpenMaya.MDistance(value, OpenMaya.MDistance().uiUnit()))
    elif i_type == OpenMaya.MFnUnitAttribute.kTime:
        mp_attr.setMTime(OpenMaya.MTime(value, OpenMaya.MTime().uiUnit()))
    elif i_type == OpenMaya.MFnUnitAttribute.kInvalid:
        s_msg = "kInvalid type not implemented yet -- {0}".format(mp_attr.info())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)
    else:
        s_msg = "Invalid type -- {0}".format(mp_attr.attribute().apiTypeStr())
        qd_logger.error(s_msg)
        raise TypeError(s_msg)


def __set_matrix(mp_attr, value):

    """
    !@Brief Get matrix attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.
    @type value: unknow
    @param value: New attribute value.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(value, (OpenMaya.MMatrix, OpenMaya.MFloatMatrix, OpenMaya.MTransformationMatrix)) is False:
        s_msg = "Argument must be a MMatrix or MFloatMatrix not {0}".format(value)
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Set
    if isinstance(value, OpenMaya.MFloatMatrix) is True:
        a_matrix = qdMatrix.float_array_from_matrix(value)
        value = qdMatrix.float_array_to_mmatrix(a_matrix)

    mfn_matrix_data = OpenMaya.MFnMatrixData()
    mp_attr.setMObject(mfn_matrix_data.create(value))


def __set_enum(mp_attr, value):

    """
    !@Brief Get enum attribute.

    @type mp_attr: OpenMaya.MPlug
    @param mp_attr: Attribute plug object.
    @type value: unknow
    @param value: New attribute value.

    @rtype: unknow
    @return: Attribute value.
    """

    #   Check
    if isinstance(mp_attr, OpenMaya.MPlug) is False:
        s_msg = "Argument must be a MPlug not {0}".format(type(mp_attr))
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    if isinstance(value, int) is False:
        s_msg = "Argument must be a int not {0}".format(value)
        qd_logger.error(s_msg)
        raise TypeError(s_msg)

    #   Get
    mp_attr.setInt(value)
