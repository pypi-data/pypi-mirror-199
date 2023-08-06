# python
import nameof
from typing import Any

def is_none(argument : Any, argument_name : str):
    if argument is None:
        raise ValueError(f'\'{argument_name} was {nameof(None)}')