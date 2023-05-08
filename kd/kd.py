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
                    "splitindex": node.spread_splitindex,
                    "splitvalue": node.spread_splitvalue,
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
    def insert(self, point: tuple[int], code: str):
        datum = Datum(point, code)
        if self.root is None:
            self.root = NodeLeaf([datum])
        else:
            self.root = self._insert(self.root, datum, 0)

    def _insert(self, node, datum: Datum, depth: int):
        if isinstance(node, NodeLeaf):
            node.data.append(datum)
            if len(node.data) > self.m:
                return self.spread_split(node, depth)
            else:
                return node

        axis = node.spread_splitindex
        if datum.coords[axis] < node.spread_splitvalue:
            node.leftchild = self._insert(node.leftchild, datum, depth + 1)
        else:
            node.rightchild = self._insert(node.rightchild, datum, depth + 1)
        return node

    def spread_split(self, leaf: NodeLeaf, depth: int):
        split_axis, spread = self.max_spread(leaf.data)

        
       

        leaf.data.sort(key=lambda datum: datum.coords[split_axis])

        mid_index = len(leaf.data) // 2
        if len(leaf.data) % 2 == 0:
            split_value = float((leaf.data[mid_index - 1].coords[split_axis] + leaf.data[mid_index].coords[split_axis]) / 2)
        else:
            split_value = float(leaf.data[mid_index].coords[split_axis])
       

        left_data = leaf.data[:mid_index]
        right_data = leaf.data[mid_index:]
        left_child = NodeLeaf(left_data)
        right_child = NodeLeaf(right_data)

        return NodeInternal(split_axis, split_value, left_child, right_child)



        

    def max_spread(self, data: List[Datum]):
        max_spread = float('-inf')
        split_axis = -1

        for axis in range(self.k):
            min_val = min(data, key=lambda d: d.coords[axis]).coords[axis]
            max_val = max(data, key=lambda d: d.coords[axis]).coords[axis]
            spread = max_val - min_val

            if spread > max_spread:
                max_spread = spread
                split_axis = axis

        return split_axis, max_spread

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self, point: tuple[int]):
        datum = Datum(coords=point, code=None)
        self.root, _ = self._delete(self.root, datum, 0)

    def _delete(self, node, datum: Datum, depth: int):
        if node is None:
            return None, False

        if isinstance(node, NodeLeaf):
            for stored_datum in node.data:
                if stored_datum.coords == datum.coords:
                    node.data.remove(stored_datum)
                    if not node.data:
                        return None, True  # node becomes an empty leaf, delete it
                    else:
                        return node, False
            return node, False

        axis = depth % self.k
        if datum.coords[axis] < node.spread_splitvalue:
            node.leftchild, deleted = self._delete(node.leftchild, datum, depth + 1)
        else:
            node.rightchild, deleted = self._delete(node.rightchild, datum, depth + 1)

        if deleted:
            if node.leftchild is None:
                return node.rightchild, True  # replace node with its right child
            elif node.rightchild is None:
                return node.leftchild, True  # replace node with its left child
            else:
                if isinstance(node.leftchild, NodeLeaf) and isinstance(node.rightchild, NodeLeaf):
                    if len(node.leftchild.data) + len(node.rightchild.data) <= self.m:
                        node.data = node.leftchild.data + node.rightchild.data
                        node = NodeLeaf(node.data)
                        return self.spread_split(node, depth), False
                else:
                    return node, False

        return node, False

            
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