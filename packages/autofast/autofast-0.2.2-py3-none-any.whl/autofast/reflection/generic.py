# python
from typing import Type, Generic, TypeVar, Any, List, Dict, cast, get_args


def is_generic_class(t : Type) -> bool:
    '''
    _summary_

    Parameters
    ----------
    t : Type
        _description_

    Returns
    -------
    bool
        _description_
    '''

    if not hasattr(t, '__dict__'):
        return False

    if '__origin__' in t.__dict__:
        return True

    if '__parameters__' in t.__dict__:
        return len(t.__dict__['__parameters__']) != 0

    return False


def is_instantiated_generic_class(t : Type) -> bool:
    '''
    Checks the type is generic class with instantiated parameters like List[float]

    Args:
        t (Type): type.

    Returns:
        bool: `True` if `t` is generic class with instantiated parameters, else `False`.
    '''

    if not is_generic_class(t):
        return False

    return '__args__' in t.__dict__


def is_type_equal_generic(t : Type) -> bool:
    '''
    Checks the type is typing.Generic

    Args:
        t (Type): type

    Returns:
        bool: `True` if `t` is `typing.Generic`, else `False`.
    '''

    if not '__origin__' in t.__dict__:
        return False
    
    return t.__dict__['__origin__'] == Generic


def is_generic_instance(ob : Any) -> bool:
    '''
    Checks the objects is generic instance.

    Args:
        ob (Any): object.

    Returns:
        bool: `True` if `ob` is instance of generic class, else `False`.
    '''

    return '__orig_class__' in ob.__dict__ 


def get_generic_instance_type(ob : Any) -> Type:
    '''
    Returns instantiated generic type.

    Args:
        ob (Any): object.

    Returns:
        Type: Instantiated generic type of this object.
    '''

    return ob.__dict__['__orig_class__']


def get_generic_origin(t : Type) -> Type:
    '''
    Returns origin type of instantiated generic type.

    Args:
        t (Type): instantiated generic type.

    Returns:
        Type: _description_
    '''

    return t.__dict__['__origin__']


def get_generic_origin_parameters(t : Type) -> List[TypeVar]:
    '''
    Returns `TypeVar` parameters of origin generic type.

    Args:
        t (Type): origin generic type.

    Returns:
        List[TypeVar]: parameters of origin generic type.
    '''

    return cast(List[TypeVar], list(t.__dict__['__parameters__']))


def get_nested_generic_instance(
    t : Type, 
    parameter_instances_dict : Dict[TypeVar, Type]
):
    '''
    Returns instantiated nested generic class with rules determined
    by `parameter_instances_dict` with generic parameter instantiating rules `TypeVar` -> `Type`.

    For example, generic class Foo[T, Bar[V], Z]
        with rules: T -> int, V -> float, Z -> Min[Max[T]]
        will be instantieted as fallows: Foo[int, Bar[float], Min[Max[int]]].

    Args:
        t (Type): 
            Given generic class.

        parameter_instances_dict (Dict[TypeVar, Type]): 
            Dictionary with rules `TypeVar` -> `Type`

    Returns:
        _type_: _description_
    '''
    args = get_args(t)

    new_args : List[Type] = []

    for arg in args:
        if type(arg) == TypeVar:
            arg = parameter_instances_dict[arg]

        if is_generic_class(arg):
            arg = get_nested_generic_instance(arg, parameter_instances_dict)
        
        new_args.append(arg)

    # ToDo
    # generic_origin = get_generic_origin(t)
    # generic_instance = get_generic_origin(t)[tuple(new_args)]
    
    # ToDo change on 3.8.13
    generic_instance = t[tuple(new_args)]

    return generic_instance