# python
from typing      import Any
from dataclasses import dataclass

@dataclass
class ArgumentMetaInfo:
    ''' Contains meta information of argument. '''

    name : str
    ''' Name identificator of argument. '''

    annotation : Any
    ''' Annotation of argument. '''