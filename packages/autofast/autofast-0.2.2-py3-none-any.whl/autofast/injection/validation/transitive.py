# project
from .graph import *


def __validate_node_transitive_inheritance_way(node : InheritanceGraphNode, ancestor : InheritanceGraphNode):
    for parent in node.parents:
        if parent == ancestor:
            raise Exception(
                f'Error. Transitive inheritance from ancestor.'
                f'{node.meta.type} <- {ancestor.meta.type}'
            )

        for ancestor_parent in ancestor.parents:
            __validate_node_transitive_inheritance_way(node, ancestor_parent)


def __validate_node_transitive_inheritance(node : InheritanceGraphNode):
    for parent_any in node.parents:
        parent = cast(InheritanceGraphNode, parent_any)
        for ancestor_any in parent.parents:
            ancestor = cast(InheritanceGraphNode, ancestor_any)

            __validate_node_transitive_inheritance_way(node, ancestor)

        __validate_node_transitive_inheritance(parent)


def validate_transitive_inheritance(cls : ClassMetaInfo):
    '''
    Validates inheritance for transitive inheritance like
    A -> C, A -> B ; B -> D; D -> C

    Args:
        cls (ClassMetaInfo): Meta information of class.

    Raises:
        Exception: if class has a transitive inheritance.
    '''

    graph = build_inheritance_graph(cls)

    for meta, node in graph.nodes.items():
        __validate_node_transitive_inheritance(node)