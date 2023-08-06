# python
from typing      import Any, List, cast
from dataclasses import dataclass
# project
from .argument_meta_info import ArgumentMetaInfo


@dataclass
class FunctionMetaInfo:
    ''' Contains meta-information of function. '''

    origin_handler : Any
    ''' Origin handler of function. '''

    name : str
    ''' Name identificator of function. '''

    return_annotation : Any
    '''Annotation of return type. '''

    abstract : bool
    ''' Flag indicating that function is abstract. '''
    
    static : bool
    ''' Flag indicating that function is static. '''

    arguments : List[ArgumentMetaInfo]
    ''' Collection of meta-information of arguments. '''


    def __eq__(self, other) -> bool:
        other_t = cast(FunctionMetaInfo, other)

        return self.origin_handler == other_t.origin_handler


    def __hash__(self) -> int:
        '''
        Returns hash.

        Returns:
            int: hash (hash of original function handler.)
        '''
        return hash(self.origin_handler)


    def __str__(self):
        '''
        Returns default str-present of meta-information of function.

        Args:
            func_info (FunctionMetaInfo): Meta-information of function.

        Returns:
            str: Default str-present of meta-infromation of function.
        '''
        string_list = []
        if(self.abstract):
            string_list.append('abstract ')

        string_list.append(f'{self.name}(')

        arguments = self.arguments
        for arg_idx in range(len(arguments)):
            arg = arguments[arg_idx]

            str_anno : str  = ''
            if arg.annotation == Any:
                str_anno = 'Any'
            else:
                str_anno = f'{arg.annotation}'

            string_list.append(f'{arg.name} : {str_anno}')
                
            if arg_idx != len(arguments) - 1:
                string_list.append(', ')
        
        string_list.append(')')

        string_list.append(f' -> {self.return_annotation}')

        return ''.join([s for s in string_list])


    def is_signature_equal(self, other : Any):
        other_meta = cast(FunctionMetaInfo, other)

        if self.name != other_meta.name:
            return False

        if self.return_annotation != other_meta.return_annotation:
            return False

        for self_arg, other_arg in zip(self.arguments, other_meta.arguments):
            if self_arg.annotation != other_arg.annotation:
                return False

        return True