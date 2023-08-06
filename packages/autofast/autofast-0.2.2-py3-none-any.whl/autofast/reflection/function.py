# python
import inspect
from typing import Type, List, Any
# project
from .data    import FunctionMetaInfo, ArgumentMetaInfo
from .generic import *


def get_functions(data_type : Type) -> List[Any]:
    '''
    Returns functions of class.

    Args:
        data_type (Type): Given class.

    Returns:
        List[Any]: Functions of class.
    '''

    functions = []
    for name in dir(data_type):
        data = getattr(data_type, name)
        if inspect.isfunction(data):
            functions.append(data)

    return functions


def get_methods(data_type : Type) -> List[Any]:
    '''
    Returns methods of class.

    Args:
        data_type (Type): Given class.

    Returns:
        List[Any]: Methods of class.
    '''

    methods = []
    for name in dir(data_type):
        data = getattr(data_type, name)
        if inspect.ismethod(data):
            methods.append(data)

    return methods


def is_abstract_function(function_type : Any) -> bool:
    '''
    Checks the function is abstract.

    Args:
        function_type (Any): Given function.

    Returns:
        bool: Check status.
    '''

    if hasattr(function_type, '__isabstractmethod__'):
        return True

    return False


def get_function_short_name(function) -> str:
    '''
    Returns short name of function.

    Args:
        function (_type_): Given function.

    Returns:
        str: Short name of function.
    '''

    func_name : str = getattr(function, '__qualname__')
    
    return func_name.split('.')[1]


def get_class_that_defined_method(meth):
    '''
    Determines Class that defined a given method.

    See - https://stackoverflow.com/a/25959545

    Args:
        meth (Callable): Method to determine class from

    Returns:
        Callable: Class that defined method

    '''
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects 