# python
from typing import Type, List
from abc    import ABC
# project
from .generic       import *
from .function      import *
from .class_reflect import *
from .data import ClassMetaInfo


def get_functions_meta_info(t : Type) -> List[FunctionMetaInfo]:
    '''
    Returns meta-information of functions defined in class.

    Args:
        t (Type): Given class.

    Returns:
        List[FunctionMetaInfo]: meta-information of functions defined in type.
    '''

    functions = get_functions(t)

    meta_info_list : List[FunctionMetaInfo] = []
    for func in functions:
        if get_class_that_defined_method(func) != t:
            continue

        short_name    = get_function_short_name(func)
        abstract_flag = is_abstract_function(func)

        args_spec = inspect.getfullargspec(func)

        arguments : List[ArgumentMetaInfo] = []
        for arg in args_spec.args:
            arg_annotation = Any
            if arg in args_spec.annotations:
                arg_annotation = args_spec.annotations[arg]
            arguments.append(ArgumentMetaInfo(arg, arg_annotation))

        return_annotation = None
        if 'return' in args_spec.annotations:
            return_annotation = args_spec.annotations['return']

        # ToDo add static method inspect
        meta_info_list.append(
            FunctionMetaInfo(
                func,
                short_name, 
                return_annotation, 
                abstract_flag, 
                False, 
                arguments
            )
        )

    return meta_info_list


def get_functions_meta_info_generic_instance(t : Type) -> List[FunctionMetaInfo]:
    '''
    Returns meta-information of functions defined in given generic class.

    Args:
        t (Type): Given generic class.

    Returns:
        List[FunctionMetaInfo]: Meta-information of functions defined in given generic type.
    '''

    origin_t = get_generic_origin(t)
    args = get_args(t)
    gen_parameters = get_generic_origin_parameters(origin_t)

    parameter_instances_dict : Dict[TypeVar, Type] = {}
    for arg, gen_param in zip(args, gen_parameters):
        parameter_instances_dict[gen_param] = arg

    functions = get_functions_meta_info(get_generic_origin(t))

    for function in functions:
        return_anno = function.return_annotation
        if not return_anno is None:
            if type(return_anno) == TypeVar:
                return_anno = parameter_instances_dict[return_anno]

            if is_generic_class(return_anno):
                return_anno = get_nested_generic_instance(
                    return_anno,
                    parameter_instances_dict
                )
        function.return_annotation = return_anno

        # Replace parameters in generic and nested generic classes with instances
        for arg in function.arguments:
            arg_anno = arg.annotation
            if not arg_anno is None:
                if type(arg_anno) == TypeVar:
                    arg_anno = parameter_instances_dict[arg_anno]
                if is_generic_class(arg_anno):
                    arg_anno = get_nested_generic_instance(
                        arg_anno,
                        parameter_instances_dict
                    )
            arg.annotation = arg_anno

    return functions


def get_generic_class_meta_info(t : Type) -> ClassMetaInfo:
    '''
    Returns meta-information for given generic class.

    Args:
        t (Type): Given generic class.

    Raises:
        RuntimeError: If len of args in instantiated generic type != len of parameters in origin generic type.

    Returns:
        ClassMetaInfo: Meta
    '''

    args = get_args(t)

    t_origin = cast(Type, get_generic_origin(t))
    
    t_origin_parameters = get_generic_origin_parameters(t_origin)

    if len(args) != len(t_origin_parameters):
        raise RuntimeError(
            f'Failed to inspect generic instance \'{t_origin}\', '
            f'len of args != len of parameters:',
            f'{args} != {t_origin_parameters}.')

    parameter_instances_dict : Dict[TypeVar, Type] = {}
    for parameter, arg in zip(t_origin_parameters, args):
        parameter_instances_dict[parameter] = arg

    parents = get_parents(t_origin)

    parents_list : List[ClassMetaInfo] = []
    for parent_type in parents:
        if is_type_equal_generic(parent_type):
            continue
        if parent_type == ABC:
            continue

        instance_type = None
        if is_generic_class(parent_type):
            instance_type = get_nested_generic_instance(parent_type, parameter_instances_dict)
        else:
            instance_type = parent_type

        parents_list.append(get_class_meta_info(instance_type))

    functions = get_functions_meta_info_generic_instance(t)

    return ClassMetaInfo(t, True, parents_list, functions)


def get_class_meta_info(t : Type) -> ClassMetaInfo:
    '''
    Returns meta-information of given class.

    Args:
        t (Type): Given class.

    Raises:
        ValueError: if given class is non-instantiated generic class.

    Returns:
        ClassMetaInfo: Meta-information of given class.
    '''
    if is_generic_class(t):
        if not is_instantiated_generic_class(t):
            raise ValueError(
                f'Cannot get info from class \'{t}\' because ' 
                f'is not have instance args of generic parameters.'
            )
        return get_generic_class_meta_info(t)

    funcs_meta_info = get_functions_meta_info(t)

    parents = get_parents(t)

    parents_info_list = []
    for parent in parents:
        if parent == object:
            continue
        parents_info_list.append(get_class_meta_info(parent))

    return ClassMetaInfo(t, False, parents_info_list, funcs_meta_info)