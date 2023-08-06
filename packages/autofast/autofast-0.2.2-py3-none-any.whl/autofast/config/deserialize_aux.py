# python
import numbers
from typing import Type, List


def is_generic(t : Type) -> bool:
    return hasattr(t, '__origin__')


def is_list_alias(t : Type) -> bool:
    return t.__origin__ == list if is_generic(t) else False


def is_tuple_alias(t : Type) -> bool:
    return t.__origin__ == tuple if is_generic(t) else False


def is_true_number_type(type) -> bool:
    return issubclass(type, numbers.Number) and not issubclass(type, bool)


def get_list_alias_arg(t : Type) -> Type:
    return t.__args__[0]


def get_tuple_alias_args(t : Type) -> List[Type]:
    return t.__args__

