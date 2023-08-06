# python
from dataclasses import dataclass
from typing import Set, Any, Dict, cast

from autofast.reflection.data import ClassMetaInfo

@dataclass
class InheritanceGraphNode:
    ''' Node of builded inheritance graph. '''

    meta : ClassMetaInfo
    ''' Original meta information of type. '''
    
    parents : Set[Any]
    ''' Parents of current node. '''

    children : Set[Any]
    ''' Children of current node. '''

    def __hash__(self):
        return hash(self.meta)


@dataclass
class InheritanceGraph:
    '''Inheritance graph. '''

    nodes : Dict[ClassMetaInfo, InheritanceGraphNode]
    '''Nodes of inheritance graph. '''


def __build_visit_node(meta : ClassMetaInfo, graph : InheritanceGraph):
    if not meta in graph.nodes:
        for parent_any in meta.parents:
            parent = cast(ClassMetaInfo, parent_any)
            __build_visit_node(parent, graph)

        node = InheritanceGraphNode(
            meta,
            set(),
            set()
        )

        for parent_any in meta.parents:
            parent = cast(ClassMetaInfo, parent_any)
            parent_node = graph.nodes[parent]

            node.parents.add(parent_node)

            parent_node.children.add(node)

        graph.nodes[meta] = node
        


def build_inheritance_graph(meta : ClassMetaInfo) -> InheritanceGraph:
    graph = InheritanceGraph(dict())

    __build_visit_node(meta, graph)

    return graph