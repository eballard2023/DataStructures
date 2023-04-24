# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

from typing import Union


class SkipListNode:
    def __init__(self,
                 key: int,
                 height: int = 1
                 ):
        self.key = key
        self.pointers: list[SkipListNode] = [None] * height

    @property
    def height(self):
        return len(self.pointers)


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

    @property
    def height(self):
        return len(self.pointers)

    class KeyNotFoundException(Exception):
        def __init__(self, search_path: list[SkipListNode]):
            self.search_path = search_path

    def _search(self, key: int, delete_mode=False) -> Union[list[int], list[SkipListNode]]:
        """ When used for just searching, returns as specified for search.
        When used for insert, expecting not to find the key, will produce a KeyNotFoundException that contains the nodes that overshot, i.e. the ones with pointers that need to be updated. 
        When used for delete, specify delete_mode=True. Then returns a list for the nodes at each height with a pointer to the deletion target. """
        search_path: list[SkipListNode] = []
        curr_node = None
        ptrs = self.pointers
        h = len(ptrs) - 1
        while True:
            while True:
                if h < 0:
                    raise SkipList.KeyNotFoundException(search_path)
                next_node = ptrs[h]
                if next_node is None or next_node.key > key:
                    h -= 1
                    continue
                elif next_node.key == key:
                    if delete_mode:
                        search_path.append(curr_node)
                        if h == 0:
                            return list(reversed(search_path))
                        h -= 1
                        continue
                    else:
                        search_path.append(next_node)
                        return [node.key for node in search_path]
                elif next_node.key < key:
                    break
            if not delete_mode:
                search_path.append(next_node)
            ptrs = next_node.pointers
            curr_node = next_node

    def search(self, key: int) -> list[int]:
        """ Key guaranteed to be in the list. Return list of keys of nodes visited, including the target. """
        return self._search(key)

    def insert(self, key: int, height: int):
        """ Key guaranteed not to be in the list already """
        try:
            self._search(key)
        except SkipList.KeyNotFoundException as x:
            # expecting such an exception
            search_path = x.search_path
        else:
            raise Exception(f"Key {key} already in list")

        new_node = SkipListNode(key, height)

        if self.height < height:
            self.pointers += [None] * (height - self.height)

        if not search_path:
            # empty search, overshot immediately every time and only the head needs to be updated
            for h in range(0, height):
                new_node.pointers[h] = self.pointers[h]
                self.pointers[h] = new_node
            return

        # head pointers that go over the first node in the search path
        for h in range(search_path[0].height, height):
            new_node.pointers[h] = self.pointers[h]
            self.pointers[h] = new_node

        # search node pointers that go over the next node in the search path
        for i in range(0, len(search_path) - 1):
            node = search_path[i]
            next_node = search_path[i+1]

            for h in range(next_node.height, min(node.height, height)):
                new_node.pointers[h] = node.pointers[h]
                node.pointers[h] = new_node

        # last node in the search path
        last_node = search_path[-1]
        for h in range(0, min(last_node.height, new_node.height)):
            new_node.pointers[h] = last_node.pointers[h]
            last_node.pointers[h] = new_node

    def delete(self, key: int):
        """ Key guaranteed to be in the list """
        search_path = self._search(key, delete_mode=True)
        # replace None, indicating a head pointer, with self
        search_path = [n if n else self for n in search_path]

        delete_target = search_path[0].pointers[0]
        for h, node in enumerate(search_path):
            node.pointers[h] = delete_target.pointers[h]
