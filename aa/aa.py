# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import json
from typing import Any


class AANode:
    def __init__(self,
                 key: int,
                 level: int,
                 left_child: "AANode" = None,
                 right_child: "AANode" = None,
                 ):
        self.key = key
        self.level = level
        self.left_child = left_child
        self.right_child = right_child


class AATree:
    def __init__(self, root: AANode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: AANode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    def insert(self, key: int):
        """ Key guaranteed not to be in the tree already """
        pass

    def delete(self, key: int):
        """ Key guaranteed to be in the tree """
        pass


def dump(tree: AATree) -> str:
    def _to_dict(node: AANode) -> dict[str, Any]:
        return {
            "key": node.key,
            "level": node.level,
            "left":  _to_dict(node.left_child) if node.left_child else None,
            "right":  _to_dict(node.right_child) if node.right_child else None,
        }
    if tree.root == None:
        dict_repr = None
    else:
        dict_repr = _to_dict(tree.root)
    return json.dumps(dict_repr)
