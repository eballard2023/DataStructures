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
    if root is None:
        return -1
    else:
        left = height(root.leftchild)
        right = height(root.rightchild)
        return max(left, right) + 1



# Insert.
def insert(root: Node, key: int, value: str) -> Node:
    if root is None:
        return Node(key, value)
    elif key < root.key:
        root.leftchild = insert(root.leftchild, key, value)
      
        if height(root.leftchild) - height(root.rightchild) > 1:

            if key < root.leftchild.key:
               
                root = leftrotate(root)
            else:
         
                root.leftchild = rightrotate(root.leftchild)
                root = leftrotate(root)
    else:
        #right tree
        root.rightchild = insert(root.rightchild, key, value)
       
        if height(root.rightchild) - height(root.leftchild) > 1:
           
            if key >= root.rightchild.key:
                
                root = rightrotate(root)
            else:
              
                root.rightchild = leftrotate(root.rightchild)
                root = rightrotate(root)
    return root

def leftrotate(root: Node) -> Node:
   new_root = root.leftchild
   root.leftchild = new_root.rightchild
   new_root.rightchild = root
   return new_root

def rightrotate(root: Node) -> Node:
    new_root = root.rightchild
    root.rightchild = new_root.leftchild
    new_root.leftchild = root
    return new_root


# Bulk Delete.
def delete(root: Node, keys: List[int]) -> Node:
    # Flag all nodes whose keys are in the list for deletion
    def tag(node: Node) -> bool:
        if node is None:
            return False
        delete = False
        if tag(node.leftchild) and tag == node:
            node.leftchild = None
        if tag(node.rightchild) and tag == node:
            node.rightchild = None
        if node.key in keys:
            node.value = None
            delete = True
        return delete
    tag(root)

    # Perform an in-order traversal to get an ordered list of key-value pairs
    def inorder(node: Node) -> List[List[int]]:
        if node is None:
            return []
        result = []
        result.extend(inorder(node.leftchild))
        if node.value is not None:
            result.append([node.key, node.value])
        result.extend(inorder(node.rightchild))
        return result
    key_value_pairs = inorder(root)

    # Completely rebuild the tree using the ordered list
    def build_tree(pairs: List[List[int]]) -> Node:
        if not pairs:
            return None
        mid = len(pairs) // 2
        root = Node(pairs[mid][0], pairs[mid][1])
        root.leftchild = build_tree(pairs[:mid])
        root.rightchild = build_tree(pairs[mid+1:])
        return root
    return build_tree(key_value_pairs)

# Search.
def search(root: Node, search_key: int) -> str:
    depth = 0
    search_val = None

    curr = root
    while curr is not None:
        depth += 1
        if search_key == curr.key:
            search_val = curr.value 
            break
        elif search_key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    return json.dumps([depth,search_val])
# Range Query.
def rangequery(root: Node, x0: int, x1: int) -> List[str]:
    rangeQ = []
    
    def travel(node: Node):
        if node is None:
            return
        if node.key >= x0 and node.key <= x1:
            if node.value is not None:
                rangeQ.append(node.value)
            travel(node.leftchild)
            travel(node.rightchild)
        elif node.key < x0:
            travel(node.rightchild)
        else:
            travel(node.leftchild)

    travel(root)

    return rangeQ