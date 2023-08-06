# python
from __future__ import annotations
from typing import Any, Type
from abc    import ABC, abstractmethod
# project


class Node(ABC):
    def __init__(
        self,
        parent   : Node,
        key_name : str
    ):
        self.parent   = parent
        self.key_name = key_name
        
    @abstractmethod
    def get_original_type(self) -> Type:
        raise NotImplementedError()
        
        
    def get_full_path(self) -> list:
        current_path = []
        if not self.key_name is None:
            current_path = [self.key_name]

        parent_path = []
        if not self.parent is None:
            parent_path = self.parent.get_full_path()
            
        return parent_path + current_path
    
    
    def get_full_path_str(self):
        full_path = self.get_full_path()
        
        strings = []
        for idx in range(len(full_path)):
            key_name = full_path[idx]
            
            if isinstance(key_name, str):
                if idx != 0:
                    strings.append('.')
                strings.append(key_name)
            else:
                strings.append(f'[{key_name}]')
                
        return ''.join(strings)
        
            

class DictNode(Node):
    def __init__(
        self,
        data     : dict,
        parent   : Any,
        key_name : str
    ):
        super().__init__(parent, key_name)
        
        self.dict_data : dict[str, Node] = {}
        
        for key, item in data.items():
            self.dict_data[key] = _provide_node(item, self, key)
            
    
    def get_original_type(self) -> Type:
        return dict


            
class ListNode(Node):
    def __init__(
        self,
        list_data : list,
        parent    : Any,
        key_name  : str
    ):
        super().__init__(parent, key_name)
        
        self.list_data : list[Node] = []
        
        for idx in range(len(list_data)):
            item = list_data[idx]
            self.list_data.append(_provide_node(item, self, idx))
    
    
    def get_original_type(self) -> Type:
        return list
        
        
        
class ValueNode(Node):
    def __init__(
        self,
        value    : Any,
        parent   : Any,
        key_name : str
    ):
        super().__init__(parent, key_name)
        
        self.value    = value
        self.parent   = parent
        self.key_name = key_name
        
    
    def get_original_type(self) -> Type:
        return type(self.value)
    
        

def _provide_node(item, parent, key_name):
    if isinstance(item, dict):
        return DictNode(item, parent, key_name)
    elif isinstance(item, list):
        return ListNode(item, parent, key_name)
    else:
        return ValueNode(item, parent, key_name)