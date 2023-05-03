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
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild) if node.leftchild is not None
                    else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None
                    else None)
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
    def delete(self, point: tuple[int]):
        if self.root is None:
            return

        self.root, _ = self._delete(self.root, point)

    def _delete(self, node, point: tuple[int]):
        if node is None:
            return None, False

        if isinstance(node, NodeLeaf):
            for i, datum in enumerate(node.data):
                if datum.coords == point:
                    node.data.pop(i)
                    break
            if not node.data:
                return None, True
            else:
                return node, False

        deleted = False
        if point[node.splitindex] < node.splitvalue:
            node.leftchild, deleted = self._delete(node.leftchild, point)
        else:
            node.rightchild, deleted = self._delete(node.rightchild, point)

        if deleted:
            if node.leftchild is None:
                return node.rightchild, True
            elif node.rightchild is None:
                return node.leftchild, True

        return node, False

   
    def calc_d2(self, point1: tuple[int], point2: tuple[int]) -> float:
        return sum([(point1[i] - point2[i])**2 for i in range(self.k)])

    def compare(self, point: tuple[int], node: NodeLeaf, knnlist: List[Datum], k: int) -> List[Datum]:
        # Add the datum from the node to the knnlist if it isn't full
        if len(knnlist) < k:
            knnlist.append(Datum(node.coords, node.code))
        else:
            # Compare the d^2 value from point to each datum's coords
            max_dsquared = 0
            max_index = -1
            for i, knn_datum in enumerate(knnlist):
                temp = self.calc_d2(point, knn_datum.coords)
                if temp > max_dsquared:
                    max_dsquared = temp
                    max_index = i
            # Replace the largest d^2 value in the knnlist with the datum if its d^2 value is smaller
            if self.calc_d2(point, node.coords) < max_dsquared:
                knnlist[max_index] = Datum(node.coords, node.code)
        return knnlist
    def should_traverse_subtree(node, point, max_dist):
        axis = node.splitindex
        return abs(point[axis] - node.splitvalue) <= max_dist

        
    def knn(self, k: int, point: tuple[int]) -> str:

        def should_traverse_subtree(node, point, max_dist):
            axis = node.splitindex
            bounding_box_dist = abs(point[axis] - node.splitvalue)
            return bounding_box_dist ** 2 <= max_dist ** 2


        def find(node, point, depth=0):
            nonlocal leaveschecked, knnlist

            if isinstance(node, NodeLeaf):
                new_data = [datum for datum in node.data if datum not in knnlist]
                if not new_data:
                    return

                leaveschecked += 1
                knnlist.extend(new_data)
                knnlist.sort(key=lambda datum: distance(datum.coords, point))
                knnlist = knnlist[:k]  # Trim the list to keep the nearest k elements
            else:
                split = node.splitindex
                if point[split] < node.splitvalue:
                    find(node.leftchild, point, depth + 1)
                    if should_traverse_subtree(node, point, distance(knnlist[-1].coords, point)):
                        find(node.rightchild, point, depth + 1)
                else:
                    find(node.rightchild, point, depth + 1)
                    if should_traverse_subtree(node, point, distance(knnlist[-1].coords, point)):
                        find(node.leftchild, point, depth + 1)

        def distance(p1, p2):
            return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))

        knnlist = []
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