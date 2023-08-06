from ..parse_graph.node import Node


class FieldParseError(Exception):
    def __init__(
        self, 
        node   : Node,
        reason : str
    ):
        message = f'Error during parse config on field {node.get_full_path_str()}, reason: {reason}.'
        
        super().__init__(message)
        
    
    