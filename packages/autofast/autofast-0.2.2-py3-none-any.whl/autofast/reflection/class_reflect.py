# python
from typing import Type, List, Any, cast


def get_parents(t : Type) -> List[Type]:
    '''
    Returns parent types of given type.

    Args:
        t (Type): Given type.

    Returns:
        List[Type]: parent types of given type. 
    '''

    parents : Any = None

    if '__orig_bases__' in t.__dict__:
        parents = t.__dict__['__orig_bases__']
    else:
        parents = t.__bases__

    return cast(List[Type], list(parents))