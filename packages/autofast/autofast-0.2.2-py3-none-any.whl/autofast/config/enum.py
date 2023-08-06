# python
from typing import TypeVar, Generic, Type
from enum import Enum


EnumT = TypeVar('EnumT', bound=Enum)

def parse_enum_str(
    enum_type   : Type[EnumT], 
    val         : str, 
    strong_enum : bool = False
) -> EnumT:
    '''
    Parses string value value to `enum_type`.

    Args:
        enum_type (Type[EnumT]): Type of enum (Must inherit from `Enum`).
        val (str): string value.
        strong_enum (bool, optional): 
            Enable/disable strong register string matching. 
            For example if disable, Enum value RED_COLOR and string 'Red_cOlor' can be parsed,
            otherwise must be strong register matching.
            Defaults to False.

    Raises:
        ValueError: If string value can not be parsed.

    Returns:
        _type_: Parsed enum value.
    '''

    # parse str
    if isinstance(val, str):
        elements_data = dict()
        for el in enum_type:
            if not strong_enum:
                elements_data[el.name.lower()] = el
            else:
                elements_data[el.name] = el

        key_item = val.lower() if not strong_enum else val
        
        if not key_item in elements_data:
            raise ValueError(
                f'string \'{val}\' is can not parse to enum \'{enum_type}\''
            )
            
        return elements_data[key_item]


def parse_enum_int(
    enum_type : Type[EnumT],
    val       : int
) -> EnumT:
    '''
    Parses integer value to `enum_type`.

    Args:
        enum_type (Type[EnumT]): Type of enum (Must inherit from `Enum`).
        val (int): Integer value.

    Raises:
        ValueError: If integer value is not present in enumeration.

    Returns:
        EnumT: Parsed enum value.
    '''
    int_values = set(item.value for item in enum_type)
        
    if not val in int_values:
        raise ValueError(f'can not convert int value \'{val}\' to enum\'{enum_type}\'')
    
    return enum_type(val)