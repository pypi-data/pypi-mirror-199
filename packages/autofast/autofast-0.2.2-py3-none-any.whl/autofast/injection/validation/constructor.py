# python
from typing import Type, Any
# project
from autofast.reflection      import get_class_meta_info
from autofast.reflection.data import ClassMetaInfo


def validate_constructor(cls_meta: ClassMetaInfo):
    has_constructor = False
    for func in cls_meta.functions:
        if func.name == '__init__':
            has_constructor = True

            if len(func.arguments) < 1:
                raise ValueError(
                    f'Error. Data type \'{cls_meta.type}\' has constructor function \'__init__\' with empty arguments.'
                )

            if  len(func.arguments) <= 1:
                return
            
            for arg in func.arguments[1:]:
                if arg.annotation == Any:
                    raise ValueError(
                        f'Error. argument \'{arg.name}\' has not annotation in constructor function \'__init__\' '
                        f'of type \'{cls_meta.type}\'.'
                    )