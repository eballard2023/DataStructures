from __future__ import annotations
import json
import math
from typing import List
from typing import List, Union
import math

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
    def __init__(self,
        splitindex : int,
        splitvalue : float,
        leftchild,
        rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild = leftchild
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
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum
                    in node.data])
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

        axis = node.splitindex
        if datum.coords[axis] < node.splitvalue:
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
        find(self.root, point)

        return json.dumps({"leaveschecked": leaveschecked, "points": [datum.to_json() for datum in knnlist]})










def main():
        kdtree = KDtree(6, 2)

        # Insert the points
        kdtree.insert((1,9,12,8,1,3), "ZRD")
        kdtree.insert((9,17,11,12,3,18), "YYJ")
        kdtree.insert((0,11,16,0,18,16), "WCF")
        kdtree.insert((8,13,1,16,5,13), "YIS")
        kdtree.insert((17,16,10,5,12,14), "DTG")
        kdtree.insert((2,0,7,18,16,7), "BPC")
        kdtree.insert((5,8,2,3,4,6), "UOH")
        kdtree.insert((6,3,13,19,6,17), "DEI")
        kdtree.insert((11,5,5,1,9,4), "VKV")
        kdtree.insert((4,6,6,15,8,1), "UHW")

        # Perform knn search
        knn_result = kdtree.knn(1, (3,1,15,14,12,13))
        print(knn_result)

if __name__ == '__main__':
            main()