from __future__ import annotations
import json
import math
from typing import List

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  spread_splitindex : int,
                  spread_splitvalue : float,
                  leftchild,
                  rightchild):
        self.spread_splitindex = spread_splitindex
        self.spread_splitvalue = spread_splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "spread_splitindex": node.spread_splitindex,
                    "spread_splitvalue": node.spread_splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        datum = Datum(coords=point, code=code)

        if (self.root is None):
            self.root = NodeLeaf([datum])
        else:
            self.insert_aux(datum, self.root, 0)
                


        
        

       

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self, point:tuple[int]):
        datum = Datum(coords=point, code=None)
        node, parent, depth = self.delete_aux(datum, self.root, None, 0)
        if node is not None:
            if parent is None:
                self.root = None
            elif isinstance(parent.leftchild, NodeLeaf) and isinstance(parent.rightchild, NodeLeaf):
                self.spread_merge(parent)
            else:
                if parent.leftchild is node:
                    grandchild = parent.rightchild
                else:
                    grandchild = parent.leftchild
                if parent is self.root:
                    self.root = grandchild
                else:
                    grandparent = self.parent_search(self.root, parent, 0)
                    if grandparent.leftchild is parent:
                        grandparent.leftchild = grandchild
                    else:
                        grandparent.rightchild = grandchild

    def delete_aux(self, datum: Datum, node, parent, depth: int):
        if isinstance(node, NodeLeaf):
            if datum in node.data:
                node.data.remove(datum)
                if not node.data:
                    return node, parent, depth
                else:
                    return None, parent, depth
            else:
                return None, parent, depth
        else:
            axis = depth % self.k
            if datum.coords[axis] <= node.spread_splitvalue:
                return self.delete_aux(datum, node.leftchild, node, depth + 1)
            else:
                return self.delete_aux(datum, node.rightchild, node, depth + 1)

    def spread_merge(self, node):
        merged_data = node.leftchild.data + node.rightchild.data
        merged_leaf = NodeLeaf(merged_data)
        if node is self.root:
            self.root = merged_leaf
        else:
            grandparent = self.parent_search(self.root, node, 0)
            
    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        leaveschecked = 0
        knnlist = []
        # The following return line can probably be left alone unless you make changes in variable names.
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]}))

    def insert_aux(self, datum: Datum, node, depth: int) -> None:
        if isinstance(node, NodeLeaf):
            if len(node.data) < self.m:
                node.data.append(datum)
            elif len(node.data) == self.m:
                self.spread_split(datum, node, depth)
        else:
            axis = depth % self.k
            if datum.coords[axis] <= node.spread_splitvalue:
                self.insert_aux(datum, node.leftchild, depth + 1)
            else:
                self.insert_aux(datum, node.rightchild, depth + 1)

    def spread_split(self, datum: Datum, node, depth: int) -> None:
        def tie_break_key(d: Datum, axis: int, k: int) -> tuple:
            return tuple(d.coords[(axis + i) % k] for i in range(1, k))

        data = node.data + [datum]

        if depth == 0:
            axis = max(range(self.k), key=lambda axis: max(d.coords[axis] for d in data) - min(d.coords[axis] for d in data))
        else:
            axis = (depth - 1) % self.k

        # Sort the points in the leaf according to the chosen coordinate with ties broken by the remaining coordinates in cycling order
        data.sort(key=lambda d: (d.coords[axis],) + tie_break_key(d, axis, self.k))

        # spread_split index
        median_indx = len(data) // 2

        # spread_split value
        if len(data) % 2 == 0:
            median_val = (data[median_indx - 1].coords[axis] + data[median_indx].coords[axis]) / 2
        else:
            median_val = float(data[median_indx].coords[axis])

        # Everything to the left of the median
        left = data[:median_indx]

        # Everything to the right of the median
        right = data[median_indx:]

        left_leaf = NodeLeaf(left)
        right_leaf = NodeLeaf(right)

        new_node = NodeInternal(spread_splitindex=axis, spread_splitvalue=median_val, leftchild=left_leaf, rightchild=right_leaf)

        if node is self.root:
            self.root = new_node
        else:
            parent = self.parent_search(self.root, node, depth=0)

            if parent.leftchild is node:
                parent.leftchild = new_node
            else:
                parent.rightchild = new_node

            



    def parent_search(self, current_node, target_node, depth: int):
        #Returns none if no parent, otherwise returns the parent!
        if current_node is None:
            return None

        if (isinstance(current_node, NodeInternal) and
            (current_node.leftchild is target_node or current_node.rightchild is target_node)):
            return current_node

        axis = depth % self.k

        if target_node.coords[axis] <= current_node.spread_splitvalue:
            return self.parent_search(current_node.leftchild, target_node, depth + 1)
        else:
            return self.parent_search(current_node.rightchild, target_node, depth + 1)

    


def main():
    k = 2
    m = 4
    tree = KDtree(k, m)

    points_and_codes = [
       ((9, 13), "MFT"),
       ((14, 6), "QCJ"),
       ((12, 0), "GCY"),
       ((19, 14), "NQH"),
       ((15, 10), "JYP"),
       ((1, 3), "DLY"),
       ((10, 7), "UXJ"),
       ((8, 15), "UJB"),
       ((17, 1), "UVV"),
       ((18, 16), "JFX"),
   ]

   

    for point, code in points_and_codes:
        tree.insert(point, code)

    print(tree.dump())
if __name__ == "__main__":
    main()




'''{
  "spread_splitindex": 1,
  "spread_splitvalue": 10.0,
  "l": {
    "spread_splitindex": 0,
    "spread_splitvalue": 12.0,
    "l": {
      "p": "[{'coords': (1, 3), 'code': 'DLY'}, {'coords': (10, 7), 'code': 'UXJ'}]"
    },
    "r": {
      "p": "[{'coords': (12, 0), 'code': 'GCY'}, {'coords': (14, 6), 'code': 'QCJ'}, {'coords': (17, 1), 'code': 'UVV'}]"
    }
  },
  "r": {
    "spread_splitindex": 0,
    "spread_splitvalue": 15.0,
    "l": {
      "p": "[{'coords': (8, 15), 'code': 'UJB'}, {'coords': (9, 13), 'code': 'MFT'}]"
    },
    "r": {
      "p": "[{'coords': (15, 10), 'code': 'JYP'}, {'coords': (18, 16), 'code': 'JFX'}, {'coords': (19, 14), 'code': 'NQH'}]"
    }
  }
}'''