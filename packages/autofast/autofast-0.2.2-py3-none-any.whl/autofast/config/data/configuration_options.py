# python
from dataclasses import dataclass, field
from typing      import Dict, Type
# project
from .field_meta_data import FieldMeta


MetaInfoType = Dict[Type, Dict[str, FieldMeta]]

@dataclass
class ConfigurationOptions:
    meta_info              : MetaInfoType = field(default_factory=dict)
    strong_enum_str        : bool         = False
    strong_number_matching : bool         = False 