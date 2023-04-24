# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import json
from typing import Any


class SplayNode:
    def __init__(self,
                 key: int,
                 left_child: "SplayNode" = None,
                 right_child: "SplayNode" = None,
                 ):
        self.key = key
        self.left_child = left_child
        self.right_child = right_child


class SplayTree:
    def __init__(self, root: SplayNode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: SplayNode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    def splay(self, key: int, root: SplayNode = None):
        """ Key may or may not be in tree. May be called at any time during a test, as if a search was performed. """
        pass

    def insert(self, key: int):
        """ Key guaranteed not to be in the tree already. Use algorithm 1 in the notes. """
        pass

    def delete(self, key: int):
        """ Key guaranteed to be in the tree. Use algorithm 1 in the notes. """
        pass


def dump(tree: SplayTree) -> str:
    def _to_dict(node: SplayNode) -> dict[str, Any]:
        return {
            "key": node.key,
            "left":  _to_dict(node.left_child) if node.left_child else None,
            "right":  _to_dict(node.right_child) if node.right_child else None,
        }
    if tree.root == None:
        dict_repr = None
    else:
        dict_repr = _to_dict(tree.root)
    return json.dumps(dict_repr)
