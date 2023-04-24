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
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
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
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
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
            self.insert_aux(datum, self.root, depth=0)
        


        
        

        thisisaplaceholder = True

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        thisisaplaceholder = True

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
            else:
                self.split(datum, node, depth)
        else:
            axis = depth % self.k
            if datum.coords[axis] <= node.splitvalue:
                self.insert_aux(datum, node.leftchild, depth + 1)
            else:
                self.insert_aux(datum, node.rightchild, depth + 1)
    
    def split(self, datum:Datum, node, depth: int) -> None:
        data = node.data + [datum]
        print
        axis = depth % self.k

        data.sort(key=lambda d: d.coords[axis])

        #split index
        median_indx = len(data) // 2
        
        #split value
        if len(data) % 2 == 0:
            median_val = (data[median_indx - 1].coords[axis] + data[median_indx].coords[axis]) / 2
        else:
            median_val = float(data[median_indx].coords[axis])


        #everything to left of median
        left = data[:median_indx]

        #everything to right of median
        right = data[median_indx:]

        left_leaf = NodeLeaf(left)
        right_leaf = NodeLeaf(right)


        new_node = NodeInternal(splitindex= axis , splitvalue = median_val, leftchild = left_leaf, rightchild = right_leaf)

        
        if node is self.root:
            self.root = new_node
        else:
            parent = self.parent_search(self.root, node, depth = 0)

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

        if target_node.coords[axis] <= current_node.splitvalue:
            return self.parent_search(current_node.leftchild, target_node, depth + 1)
        else:
            return self.parent_search(current_node.rightchild, target_node, depth + 1)

    


