# python
from typing import Type
# project
from autofast.reflection import get_class_meta_info

from .constructor import validate_constructor
from .function import validate_functions
from .inheritance import validate_ancestor_and_descendant
from .transitive  import validate_transitive_inheritance

def validate_registration_strong_inheritance(provide_type : Type, register_type : Type):
    '''
    Validates provide and register types for strong inheritance rules. 

    Args:
        provide_type (Type): Type to be resolved. 
        register_type (Type): Type to be registered.
    '''

    if provide_type == register_type:
        return

    validate_ancestor_and_descendant(provide_type, register_type)

    register_meta = get_class_meta_info(register_type)

    validate_transitive_inheritance(register_meta)
    validate_functions(register_meta)
    validate_constructor(register_meta)


def validate_registration(provide_type : Type, register_type : Type):
    '''
    Validates provide and register types.

    Args:
        provide_type (Type): Type to be resolved.
        register_type (Type): Type to be registered.
    '''

    if provide_type == register_type:
        return

    validate_ancestor_and_descendant(provide_type, register_type)

    register_meta = get_class_meta_info(register_type)
    validate_constructor(register_meta)