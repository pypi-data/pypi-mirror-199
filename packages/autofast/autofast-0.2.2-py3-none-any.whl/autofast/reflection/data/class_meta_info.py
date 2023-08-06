# python
from typing      import Type, Any, List, cast
from dataclasses import dataclass
# project
from .function_meta_info import FunctionMetaInfo

@dataclass()
class ClassMetaInfo:
    ''' Contains meta-information of class. '''

    type    : Type
    ''' Type. '''

    is_generic : bool
    ''' Flag indicating that class is generic. '''

    parents : List[Any]
    ''' Collection of meta-information of class parents. '''

    functions : List[FunctionMetaInfo]
    ''' Collection of meta-information of functions, defined in given class. '''

    def __eq__(self, other) -> bool:
        '''
        Compares meta information with other meta information

        Args:
            other (ClassMetaInfo): other meta information. 

        Returns:
            int: Compare result.
        '''
        other_t = cast(ClassMetaInfo, other)

        return self.type == other_t.type


    def __hash__(self) -> int:
        '''
        Returns hash.

        Returns:
            _type_: Hash (hash of origin type).
        '''
        return hash(self.type)