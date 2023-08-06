# python
from typing import List
# project
from autofast.reflection.data import ClassMetaInfo, FunctionMetaInfo
from .graph import *


@dataclass
class __FunctionValidationData:
    class_info  : ClassMetaInfo
    function    : FunctionMetaInfo
    overrided   : bool


def __validate_ancestor_to_descendants_functions_way(
    node                      : InheritanceGraphNode, 
    functions_validation_data : List[__FunctionValidationData]
):
    meta = node.meta

    node_functions = meta.functions

    functions_validation_data_copy = functions_validation_data.copy()

    for node_function in node_functions:
        is_original_function = True
        for function_data in functions_validation_data:
            ancestor_func = function_data.function

            if node_function.name == ancestor_func.name:
                is_original_function = False
        
                if not node_function.is_signature_equal(ancestor_func):
                    raise Exception(
                        f'Error. function \'{node_function.name}\' from type \'{meta.type} ' 
                        f'wrong override same function from ancestor class \'{function_data.class_info.type}, '
                        f'\'{node_function}\' != \'{ancestor_func}\'.'
                    )

                if node_function.abstract and ancestor_func.abstract and not function_data.overrided:
                    raise Exception(
                        f'Cannot re-declare abstract function in child class. '
                        f'First declare in \'{function_data.class_info.type}\', second declare in \'{meta.type}\'.'
                    )

                function_data.overrided = True

        if is_original_function:
            functions_validation_data_copy.append(__FunctionValidationData(meta, node_function, False))

    for child_any in node.children:
        child = cast(InheritanceGraphNode, child_any)
        __validate_ancestor_to_descendants_functions_way(
            child,
            functions_validation_data_copy
        )

    # Check if abstract method not overrided
    for func_data in functions_validation_data_copy:
        if func_data.class_info == meta:
            func_meta = func_data.function

            if func_meta.abstract:
                if not func_data.overrided:
                    raise Exception(
                        f'Error. abstract function \'{func_meta}\' from type \'{func_data.class_info.type} '
                        f'not overrided.'
                    )


def validate_functions(cls : ClassMetaInfo):
    '''
    Validates inhertiance class and his parents and ancestors according
    to the fallowing rules:
        --In inheritance cannot have re-declared abstract methods.

        --If class have a abstract function, one of his descendant must
        implement this function.

        --Descendants cannot redeclare signature ancestor methods.

    Args:
        cls (ClassMetaInfo): Meta information of class.

    Raises:
        Exception: if functions in inheritance not match for strong inheritance rules.
    '''

    graph = build_inheritance_graph(cls)

    # ancestors with no parents
    adam_ancestors : List[InheritanceGraphNode] = list()

    for meta, node in graph.nodes.items():
        if len(node.parents) == 0:
            adam_ancestors.append(node)

    empty_list : List[__FunctionValidationData] = list()

    for adam_ancestor in adam_ancestors:
        __validate_ancestor_to_descendants_functions_way(adam_ancestor, empty_list)