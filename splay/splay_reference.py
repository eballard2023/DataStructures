# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

class SplayNode:
    def __init__(self,
                 key: int,
                 left_child: "SplayNode" = None,
                 right_child: "SplayNode" = None,
                 ):
        self.key = key
        self.left_child = left_child
        self.right_child = right_child


class SplayTree:
    def __init__(self, root: SplayNode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: SplayNode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    @staticmethod
    def rotate_left(root: SplayNode) -> SplayNode:
        right = root.right_child
        root.right_child = right.left_child
        right.left_child = root
        return right

    @staticmethod
    def rotate_right(root: SplayNode) -> SplayNode:
        left = root.left_child
        root.left_child = left.right_child
        left.right_child = root
        return left

    zig_left = rotate_left
    zig_right = rotate_right

    @staticmethod
    def zig_zig_left(root: SplayNode) -> SplayNode:
        root = SplayTree.rotate_left(root)
        root = SplayTree.rotate_left(root)
        return root

    @staticmethod
    def zig_zig_right(root: SplayNode) -> SplayNode:
        root = SplayTree.rotate_right(root)
        root = SplayTree.rotate_right(root)
        return root

    @staticmethod
    def zig_zag_left(root: SplayNode) -> SplayNode:
        root.right_child = SplayTree.rotate_right(root.right_child)
        root = SplayTree.rotate_left(root)
        return root

    @staticmethod
    def zig_zag_right(root: SplayNode) -> SplayNode:
        root.left_child = SplayTree.rotate_left(root.left_child)
        root = SplayTree.rotate_right(root)
        return root

    def splay(self, key: int):
        """ Key may or may not be in tree. May be called at any time during a test, as if a search was performed. """
        def _splay(root: SplayNode) -> tuple[SplayNode, int]:
            """ Returns new root node and the key that is being splayed. """
            if root is None:
                # key not found, flag for parent to become splay target
                return None, None
            if key == root.key:
                # key found, this node is splay target
                return root, key
            elif key < root.key:
                root.left_child, splay_key = _splay(root.left_child)
                if splay_key is None:
                    # root is in-order predecessor of original splay key
                    return root, root.key
            else:
                # key > root.key
                root.right_child, splay_key = _splay(root.right_child)
                if splay_key is None:
                    # root is in-order successor of original splay key
                    return root, root.key

            if root.left_child:
                left = root.left_child
                if left.left_child and left.left_child.key == splay_key:
                    return SplayTree.zig_zig_right(root), splay_key
                if left.right_child and left.right_child.key == splay_key:
                    return SplayTree.zig_zag_right(root), splay_key
            if root.right_child:
                right = root.right_child
                if right.right_child and right.right_child.key == splay_key:
                    return SplayTree.zig_zig_left(root), splay_key
                if right.left_child and right.left_child.key == splay_key:
                    return SplayTree.zig_zag_left(root), splay_key

            return root, splay_key

        self.root, splay_key = _splay(self.root)
        if splay_key:
            # zig
            if self.root.left_child and self.root.left_child.key == splay_key:
                self.root = SplayTree.zig_right(self.root)
            elif self.root.right_child and self.root.right_child.key == splay_key:
                self.root = SplayTree.zig_left(self.root)

    def insert(self, key: int):
        """ Key guaranteed not to be in the tree already. Use algorithm 1 in the notes. """
        if self.root is None:
            self.root = SplayNode(key)
            return

        self.splay(key)
        if self.root == key:
            raise Exception(f"Key {key} already in tree")

        if self.root.key < key:
            new_root = SplayNode(key, self.root, self.root.right_child)
            self.root.right_child = None
        else:
            # self.root.key > key
            new_root = SplayNode(key, self.root.left_child, self.root)
            self.root.left_child = None
        self.root = new_root

    def delete(self, key: int):
        """ Key guaranteed to be in the tree. Use algorithm 1 in the notes. """
        self.splay(key)
        if self.root is None or self.root.key != key:
            raise Exception(f"Key {key} not in tree")
        if self.root.left_child is None:
            # will catch case with no children
            self.root = self.root.right_child
        elif self.root.right_child is None:
            self.root = self.root.left_child
        else:
            # has both children
            right_subtree = SplayTree(self.root.right_child)
            right_subtree.splay(key)
            right_subtree.root.left_child = self.root.left_child
            self.root = right_subtree.root
