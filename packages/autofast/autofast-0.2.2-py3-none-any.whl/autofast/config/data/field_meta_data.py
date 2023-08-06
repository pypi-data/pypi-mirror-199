from dataclasses import dataclass, MISSING
from dataclasses import field, Field
from typing import Any, Callable


FIELDMETA_KEYNAME = 'autofast_meta'

@dataclass
class FieldMeta:
    required   : bool                 = False
    parse_name : str                  = ''
    decoder    : Callable[[Any], Any] = None


    @staticmethod
    def to_dict(
        required   : bool                   = False,
        parse_name : str                    = '',
        decoder    : Callable[[Any], Any]   = None
    ):
        return {
            FIELDMETA_KEYNAME : FieldMeta(required, parse_name, decoder)
        }


def field_meta(
    required   : bool                 = False,
    parse_name : str                  = '',
    decoder    : Callable[[Any], Any] = None,
    default                           = MISSING, 
    default_factory                   = MISSING, 
    init                              = True, 
    repr                              = True,
    hash                              = None, 
    compare                           = True, 
    metadata                          = None
):
    meta_dict = FieldMeta.to_dict(required, parse_name, decoder)

    if not metadata is None:
        meta_dict.update(metadata)

    return field(
        default         = default, 
        default_factory = default_factory,
        init            = init,
        repr            = repr,
        hash            = hash,
        compare         = compare,
        metadata        = meta_dict
    )