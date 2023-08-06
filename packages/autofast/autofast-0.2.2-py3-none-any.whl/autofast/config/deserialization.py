# python
from numbers        import Number
from dataclasses    import MISSING, dataclass, fields, field
from types          import MappingProxyType
from typing         import Optional, Type, List, Any, TypeVar, cast
from typing         import Dict
from enum           import Enum
# 3rd party
from nameof import nameof

from .error.config_parse_error import ConfigParseError
# project
from .deserialize_aux import is_list_alias, is_tuple_alias, is_true_number_type
from .deserialize_aux import get_list_alias_arg, get_tuple_alias_args
from .data.field_meta_data import FieldMeta, FIELDMETA_KEYNAME
from .parse_graph     import Node, DictNode, ListNode, ValueNode
from .error           import FieldParseError
from .enum            import parse_enum_str, parse_enum_int

from .data import ConfigurationOptions, MetaInfoType


__GenType = TypeVar('__GenType')



def __deserialize_item(
    item_type : Type, 
    node      : Node, 
    options   : ConfigurationOptions
):
    if isinstance(node, ValueNode):
        val_node : ValueNode = node
        if val_node.value is None:
            return None

    
    deserialized_item = None
    
    # deserialize list part
    if is_list_alias(item_type):
        deserialized_item = __deserialize_list(item_type, node, options)

    # deserialize list part that a present tuple
    elif is_tuple_alias(item_type):
        deserialized_item = __deserialize_tuple(item_type, node, options)
    
    # deserialize str
    elif issubclass(item_type, str):
        deserialized_item = __deserialize_str(node)

    # deserialize Enum
    elif issubclass(item_type, Enum):
        deserialized_item = __deserialize_enum(item_type, node, options)

    # deserialize number
    elif is_true_number_type(item_type):
        deserialized_item = __deserialize_number(item_type, node, options)
        
    # deserialize bool
    elif issubclass(item_type, bool):
        deserialized_item = __deserialize_bool(node)

    # deserialize dict
    elif isinstance(node, DictNode):
        deserialized_item = __deserialize_dict(item_type, node, options)
    
    else:
        raise ConfigParseError(
            node,
            f'invalid type of serialization in config:{node.get_original_type()}'
        )
    
    return deserialized_item


def _validate_list_node(node : Node):
    if not isinstance(node, ListNode):
        raise FieldParseError(
            node, 
            f'expected type {nameof(list)}, gotted:{node.get_original_type()}'
        )


def __deserialize_list(
    list_t  : Any, 
    node    : Node, 
    options : ConfigurationOptions
):
    _validate_list_node(node)

    list_node = cast(ListNode, node)
    
    item_type = get_list_alias_arg(list_t)
    
    deserialized_list = []
    for item in list_node.list_data:
        deserialized_list.append(__deserialize_item(item_type, item, options))
        
    return deserialized_list


def __deserialize_tuple(
    tuple_type  : Any, 
    node        : Node, 
    options     : ConfigurationOptions
):
    _validate_list_node(node)
    
    list_node = cast(ListNode, node)
    
    tuple_types = get_tuple_alias_args(tuple_type)
    
    
    if len(tuple_types) != len(list_node.list_data):
        raise FieldParseError(node, 'len of args in tuple alias != len of list in config')
    
    deserialized_list = []
    for tuple_type, item in zip(tuple_types, list_node.list_data):
        deserialized_list.append(__deserialize_item(tuple_type, item, options))
        
    return tuple(deserialized_list)


def __validate_value_node(node : Node):
    if not isinstance(node, ValueNode):
        raise FieldParseError(
            node,
            f'expected value, gotted:{node.get_original_type()}'
        )
        

def __deserialize_str(
    node
):
    __validate_value_node(node)
    
    val_node : ValueNode = node
    val                  = val_node.value
    
    if not isinstance(val, str):
        raise FieldParseError(
            node,
            f'expected type \'{nameof(str)}\', gotted:{type(val)}'
        )
        
    return str(val)


def __deserialize_enum(
    enum_type : Type,
    node      : Node,
    options   : ConfigurationOptions
):
    __validate_value_node(node)
    
    val_node = cast(ValueNode, node)

    val = val_node.value
    
    if not isinstance(val, (str, int)):
        raise FieldParseError(
            node,
            f'type of value in enum must be {nameof(int)} or {nameof(str)}'
        )
    
    # parse str
    if isinstance(val, str):
        try:
            enum_data = parse_enum_str(enum_type, val, options.strong_enum_str)
            return enum_data
        except Exception as exc:
            raise FieldParseError(
                node,
                str(exc)
            )
    # parse int
    else:
        try:
            enum_data = parse_enum_int(enum_type, val)
            return enum_data
        except Exception as exc:
            raise FieldParseError(
                node,
                str(exc)
            )
    
    
def __deserialize_number(
    number_type : Type,
    node        : Node,
    options     : ConfigurationOptions
):
    __validate_value_node(node)
    
    val_node = cast(ValueNode, node)
    
    val      = val_node.value
    val_type = type(val)
    
    if not is_true_number_type(val_type):
        raise FieldParseError(
            node,
            f'expected {nameof(Number)} (except bool) type, gotted:{val_type}'
        )
        
    if options.strong_number_matching:
        if not number_type is val_type:
            raise FieldParseError(
                node,
                f'not strong number type matching, expected:{number_type}, gotted:{val_type}'
            )
            
    return number_type(val)


def __deserialize_bool(
    node : Node
):
    __validate_value_node(node)
    
    val_node = cast(ValueNode, node)
    val      = val_node.value
    
    if not isinstance(val, bool):
        raise FieldParseError(
            node,
            f'expected {nameof(bool)}, gotted:{type(val)}'
        )
        
    return bool(val)


def validate_fields_meta(
    meta_data : Dict[str, FieldMeta],
    data_type : Type
):
    for field_name, field_meta in meta_data.items():
        if not type(field_meta) is FieldMeta:
            raise ConfigParseError(
                f'Wrong type of fields_meta in field \'{field_name}\' in dataclass \'{data_type}\', '
                f'expected \'{nameof(FieldMeta)}\', gotted \'{type(field_meta)}\''
            )
        

def provide_fields_meta(
    data_type : Type, 
    meta_info : MetaInfoType
) -> Dict[str, FieldMeta]:
    type_meta = {}

    # write local fields params
    for field in fields(data_type):
        if isinstance(field.metadata, MappingProxyType):
            if FIELDMETA_KEYNAME in field.metadata:
                type_meta[field.name] = field.metadata[FIELDMETA_KEYNAME]

    # rewrite meta from static field FIELDS_META
    if hasattr(data_type, "FIELDS_META"):
        type_fields_meta = data_type.FIELDS_META

        for field_name, field_meta in type_fields_meta.items():
            type_meta[field_name] = field_meta

    # rewrite global params
    if data_type in meta_info:
        type_fields_meta = meta_info[data_type]

        for field_name, field_meta in type_fields_meta.items():
            type_meta[field_name] = field_meta

    validate_fields_meta(type_meta, data_type)
        
    return type_meta


def __deserialize_dict(
    data_type : Type[__GenType], 
    dict_node : DictNode,
    options   : ConfigurationOptions
) -> __GenType:
    t_params = {}
    
    fields_meta = provide_fields_meta(data_type, options.meta_info)
    
    for field in fields(data_type):
        # default parsing
        parse_field_name = field.name
        decoder      = lambda node : __deserialize_item(field.type, node, options)
        
        # validation field meta
        if not fields_meta is None:
            if field.name in fields_meta:
                field_meta = fields_meta[field.name]
                parse_name = field_meta.parse_name
                if parse_name != '':
                    parse_field_name = parse_name

                # validation required
                if field_meta.required and not parse_field_name in dict_node.dict_data:
                    raise ConfigParseError(
                        f'Error during config parsing. Missing field \'{parse_field_name}\' in config '
                        f'that present field \'{field.name}\' in dataclass \'{data_type}\'.'
                    )
                    
                # if available decoder
                if not field_meta.decoder is None:
                    decoder = lambda dict_val : field_meta.decoder(dict_val)

        dict_value = dict_node.dict_data[parse_field_name] if parse_field_name in dict_node.dict_data else None
        
        deserialize_value = None
        if not dict_value is None:
            deserialize_value = decoder(dict_value)

        # set default value if field not available in configuration
        if deserialize_value is None:
            if not field.default is MISSING:
                deserialize_value = field.default
            elif not field.default_factory is MISSING:
                deserialize_value = field.default_factory()

    
        t_params[field.name] = deserialize_value
        
    return data_type(**t_params)


def deserialize_config(
    data_type              : Type[__GenType],
    dict_data              : dict,
    options                : Optional[ConfigurationOptions] = None
) -> __GenType:

    if options is None:
        options = ConfigurationOptions()

    node = DictNode(dict_data, None, '<root>')

    return __deserialize_dict(data_type, node, options)