import json

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self, 
                  key        = None, 
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:    
        return {
            "k": node.key,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root, insert the given key and return the root node.
# The key is guaranteed to not be in the tree.
def insert(root: Node, key: int) -> Node:
    #Works!
    #A new node is added at the leaf
    if root is None:
        return Node(key)
    else :
        if root.key == key:
            return root
        elif root.key < key:
            root.rightchild = insert(root.rightchild, key)
        else:
            
            root.leftchild = insert(root.leftchild, key)
    return root

# For the tree rooted at root, delete the given key and return the root node.
# The key is guaranteed to be in the tree.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    if root is None:
        return root

    #Case 1: key is less than root.key

    if key < root.key:
        root.leftchild = delete(root.leftchild, key)
    elif key > root.key:
        root.rightchild = delete(root.rightchild, key)
    else:
        if root.leftchild is None and root.rightchild is None:
            return None
            
        if root.leftchild is None:
            temp = root.rightchild
            root = None
            return temp
            
        elif root.rightchild is None:
            temp = root.leftchild
            root = None
            return temp
            
        
        temp2 = min_node(root.rightchild)
        root.key = temp2.key
        
       
        root.rightchild = delete(root.rightchild, temp2.key)
    return root

def min_node(root: Node) -> Node:
    curr = root
    while curr.leftchild is not None:
        curr = curr.leftchild
    return curr

# For the tree rooted at root, calculate the list of keys on the path from the root to the search key.
# Return the json stringified list.
# The key is guaranteed to be in the tree.
def search(root: Node, search_key: int) -> str:
    # YOUR CODE GOES HERE.
    curr = root
    path_keys = []

    while (curr.key != search_key):
        path_keys.append(curr.key)

        if search_key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    path_keys.append(search_key)
    # Then tweak the next line so it uses your list rather than None.
    return(json.dumps(path_keys))

# For the tree rooted at root, dump the preorder traversal to a stringified JSON list and return.
def preorder(root: Node) -> str:
    preorder_path = []
    curr = root
    stack = []

    while curr or stack:
        if curr:
            preorder_path.append(curr.key)
            stack.append(curr)
            curr = curr.leftchild
        else:
            curr = stack.pop()
            curr = curr.rightchild

    return(json.dumps(preorder_path))


# For the tree rooted at root, dump the inorder traversal to a stringified JSON list and return.
def inorder(root: Node) -> str:
    stack = []
    result = []
    curr = root
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.leftchild
            
        curr = stack.pop()
        result.append(curr.key)
        curr = curr.rightchild
        
    return json.dumps(result)


# For the tree rooted at root, dump the postorder traversal to a stringified JSON list and return.
def postorder(root: Node) -> str:
    if not root:
        return "[]"

    stack = []
    result = []
    prev = None

    while root or stack:
        while root:
            stack.append(root)
            root = root.leftchild

        root = stack[-1]

        if not root.rightchild or root.rightchild == prev:
            result.append(root.key)
            prev = root
            root = None
            stack.pop()
        else:
            root = root.rightchild

    return json.dumps(result)

# For the tree rooted at root, dump the BFT traversal to a stringified JSON list and return.
# The DFT should traverse left-to-right.
def bft(root: Node) -> str:
    bft_path = []
    queue = []

    # YOUR CODE GOES HERE.
    queue.append(root)
    while queue:
        curr = queue.pop(0)
        bft_path.append(curr.key)

        if curr.leftchild:
            queue.append(curr.leftchild)
        if curr.rightchild:
            queue.append(curr.rightchild)
        


    # Then tweak the next line so it uses your list rather than None.
    return json.dumps(bft_path)

