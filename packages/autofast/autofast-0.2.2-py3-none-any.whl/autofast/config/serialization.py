# python
from enum   import Enum
from typing import Type, TypeVar, Any, List, Collection, Tuple, Dict, Optional
from dataclasses import fields
# project
from .data import ConfigurationOptions
from .deserialization import provide_fields_meta

EnumT = TypeVar('EnumT', bound=Enum)


VALUE_TYPES = [type(None), bool, int, float, str]

def __is_value(t : Type) -> bool:
    for value_type in VALUE_TYPES:
        if t is value_type:
            return True
        
    return False
    

def __serialize_enum(enum_value : EnumT, options : ConfigurationOptions) -> str:
    strong_enum_flag = options.strong_enum_str

    enum_type = type(enum_value)

    enum_strings : Dict[Any, str] = dict()

    for el in enum_type:
        if not strong_enum_flag:
            enum_strings[el] = el.name.lower()
        else:
            enum_strings[el] = el.name

    return enum_strings[enum_value]


def __serialize_collection(
    data_collection : Collection[Any], 
    options : ConfigurationOptions
) -> List[Any]:
    serialized_list = list()

    for item in data_collection:
        serialized_list.append(__serialize_item(item, options))

    return serialized_list


def __serialize_item(item : Any, options : ConfigurationOptions) -> Any:
    if item is None:
        return None
    
    item_type = type(item)

    if __is_value(item_type):
        return item
    elif issubclass(item_type, Enum):
        return __serialize_enum(item, options)
    elif issubclass(item_type, (list, tuple)):
        return __serialize_collection(item, options)
    else:
        return __serialize_dataclass(item, options)


def __serialize_dataclass(object : Any, options : ConfigurationOptions) -> Optional[Dict]:
    if object is None:
        return None
    
    object_type = type(object)

    meta_info = provide_fields_meta(object_type, options.meta_info)

    data_dict = dict()

    object_dict = object.__dict__
    for field in fields(type(object)):
        field_value = object_dict[field.name]
        store_name  = field.name

        if not meta_info is None:
            if field.name in meta_info:
                parse_name = meta_info[field.name].parse_name
                if parse_name != '':
                    store_name = parse_name

        serialized_data = __serialize_item(field_value, options)
        data_dict[store_name] = serialized_data

    return data_dict


def serialize_config(
    data    : Any,
    options : Optional[ConfigurationOptions] = None
) -> Dict:

    if options is None:
        options = ConfigurationOptions()

    return __serialize_dataclass(data, options)