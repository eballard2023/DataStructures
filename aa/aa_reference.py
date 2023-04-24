# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

class AANode:
    def __init__(self,
                 key: int,
                 level: int,
                 left_child: "AANode" = None,
                 right_child: "AANode" = None,
                 ):
        self.key = key
        self.level = level
        self.left_child = left_child
        self.right_child = right_child


class AATree:
    def __init__(self, root: AANode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: AANode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    @staticmethod
    def skew(root: AANode) -> AANode:
        left = root.left_child
        root.left_child = left.right_child
        left.right_child = root
        return left

    @staticmethod
    def split(root: AANode) -> AANode:
        right = root.right_child
        root.right_child = right.left_child
        right.left_child = root
        right.level += 1
        return right

    @staticmethod
    def update_level(root: AANode):
        if root.right_child and root.right_child.level == root.level:
            # red right child
            root.right_child.level -= 1
        root.level -= 1

    @staticmethod
    def red_left_child(root: AANode) -> bool:
        if root is None or root.left_child is None:
            return False
        return root.level == root.left_child.level

    @staticmethod
    def red_red_right_child(root: AANode) -> bool:
        """ Whether the root's right child is red AND the right-right grandchild is also red """
        if root is None or root.right_child is None or root.right_child.right_child is None:
            return False
        return root.level == root.right_child.level == root.right_child.right_child.level

    @staticmethod
    def too_high(root: AANode) -> bool:
        """ Whether an update-level is required """
        if root is None:
            return False
        left_level = root.left_child.level if root.left_child else 0
        right_level = root.right_child.level if root.right_child else 0

        return root.level > min(left_level, right_level) + 1

    def insert(self, key: int):
        """ Key guaranteed not to be in the tree already """
        def _insert(root: AANode) -> AANode:
            if root is None:
                return AANode(key, 1)

            if key < root.key:
                root.left_child = _insert(root.left_child)
            elif key > root.key:
                root.right_child = _insert(root.right_child)
            else:
                raise Exception(f"Key {key} already in tree")

            if AATree.red_left_child(root):
                root = AATree.skew(root)
            if AATree.red_red_right_child(root):
                root = AATree.split(root)

            return root

        self.root = _insert(self.root)

    def delete(self, key: int) -> AANode:
        """ Key guaranteed to be in the tree """
        def _delete(root: AANode, key: int):
            if root is None:
                raise Exception(f"Key {key} not in tree")

            if key == root.key:
                if root.left_child is None:
                    if root.right_child is None:
                        # leaf
                        return None
                    else:
                        # has only red right child with no other descendants
                        return root.right_child
                else:
                    # replace with successor
                    succ = root.right_child
                    while succ.left_child is not None:
                        succ = succ.left_child
                    root.key = succ.key
                    root.right_child = _delete(root.right_child, succ.key)
            elif key < root.key:
                root.left_child = _delete(root.left_child, key)
            else:
                # key > root.key
                root.right_child = _delete(root.right_child, key)

            if AATree.too_high(root):
                AATree.update_level(root)
                if AATree.red_left_child(root):
                    root = AATree.skew(root)
                if AATree.red_left_child(root.right_child):
                    root.right_child = AATree.skew(root.right_child)
                if AATree.red_left_child(root.right_child.right_child):
                    root.right_child.right_child = AATree.skew(
                        root.right_child.right_child)
                if AATree.red_red_right_child(root):
                    root = AATree.split(root)
                if AATree.red_red_right_child(root.right_child):
                    root.right_child = AATree.split(root.right_child)

            return root

        self.root = _delete(self.root, key)
