# python
from typing import Type, cast
# project
from autofast.reflection.data import ClassMetaInfo
from autofast.reflection import get_class_meta_info


def __validate_ancestor_and_descendant_way(search_type : Type, current_class_meta : ClassMetaInfo):
    find_flag = False
    for parent_any in current_class_meta.parents:
        parent = cast(ClassMetaInfo, parent_any)

        if parent.type == search_type:
            return True

        find_parent_status = __validate_ancestor_and_descendant_way(search_type, parent)

        if find_parent_status:
            find_flag = True
            break

    return find_flag


def validate_ancestor_and_descendant(ancestor_type : Type, descendant_type : Type):
    '''
    Validates ancestor type and descendant for inheritance.

    Args:
        ancestor_type (Type): Ancestor type.
        descendant_type (Type): Descendant type.

    Raises:
        Exception: if `ancestor_type` is not ancestor of `descendant_type`.
    '''

    cls_meta = get_class_meta_info(descendant_type)

    find_status = __validate_ancestor_and_descendant_way(ancestor_type, cls_meta)

    if not find_status:
        raise Exception(f'\'{ancestor_type}\' is not ancestor of \'{descendant_type}\'.')