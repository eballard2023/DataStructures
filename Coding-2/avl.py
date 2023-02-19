import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "k": node.key,
            "v": node.value,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)

# Height of (sub)tree rooted at root.
def height(root: Node) -> int:
    # Fill in and tweak the return.
    return(None)

# Insert.
def insert(root: Node, key: int, value: str) -> Node:
    # Fill in.
    return root

# Bulk Delete.
def delete(root: Node, keys: List[int]) -> Node:
    # Fill in.
    return root

# Search.
def search(root: Node, search_key: int) -> str:
    # Fill in and tweak the return.
    return json.dumps(None)

# Range Query.
def rangequery(root: Node, x0: int, x1: int) -> List[str]:
    # Fill in and tweak the return.
    return None
