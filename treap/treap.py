# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import json
from typing import Any


class TreapNode:
    def __init__(self,
                 key: int,
                 priority: int,
                 left_child: "TreapNode" = None,
                 right_child: "TreapNode" = None,
                 ):
        self.key = key
        self.priority = priority
        self.left_child = left_child
        self.right_child = right_child


class Treap:
    def __init__(self, root: TreapNode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: TreapNode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    def insert(self, key: int, priority: int):
        """ Key and priority individually guaranteed not to be in the tree already """
        pass

    def delete(self, key: int):
        """ Key guaranteed to be in the tree.

        Use algorithm presented in notes where a priority of -math.inf is assigned before rotating to leaf. """
        pass


def dump(tree: Treap) -> str:
    def _to_dict(node: TreapNode) -> dict[str, Any]:
        return {
            "key": node.key,
            "priority": node.priority,
            "left":  _to_dict(node.left_child) if node.left_child else None,
            "right":  _to_dict(node.right_child) if node.right_child else None,
        }
    if tree.root == None:
        dict_repr = None
    else:
        dict_repr = _to_dict(tree.root)
    return json.dumps(dict_repr)
