# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import json
from typing import Any


class SkipListNode:
    def __init__(self,
                 key: int,
                 height: int = 1
                 ):
        self.key = key
        self.pointers: list[SkipListNode] = [None] * height


class SkipList:
    def __init__(self):
        self.pointers: list[SkipListNode] = []

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        if self.pointers:
            node = self.pointers[0]
            while node is not None:
                yield node
                node = node.pointers[0]

    def search(self, key: int) -> list[int]:
        """ Key guaranteed to be in the list. Return list of keys of nodes visited, including the target. """
        pass

    def insert(self, key: int, height: int):
        """ Key guaranteed not to be in the list already """
        pass

    def delete(self, key: int):
        """ Key guaranteed to be in the list """
        pass


def dump(slist: SkipList) -> str:
    def _to_dict(node: SkipListNode) -> dict[str, Any]:
        return {
            "key": node.key,
            "pointers": [p.key if p else None for p in node.pointers]
        }
    return json.dumps([[p.key if p else None for p in slist.pointers]] + [_to_dict(node) for node in slist])
