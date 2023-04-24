# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

class TreapNode:
    def __init__(self,
                 key: int,
                 priority: int,
                 left_child: "TreapNode" = None,
                 right_child: "TreapNode" = None,
                 ):
        self.key = key
        self.priority = priority
        self.left_child = left_child
        self.right_child = right_child


class Treap:
    def __init__(self, root: TreapNode = None):
        self.root = root

    def __iter__(self):
        """ Do not modify """
        return self.iterator()

    def iterator(self):
        """ Do not modify """
        def _iterator(root: TreapNode):
            if root is None:
                return
            yield from _iterator(root.left_child)
            yield root
            yield from _iterator(root.right_child)
        return _iterator(self.root)

    @staticmethod
    def rotate_left(root: TreapNode) -> TreapNode:
        right = root.right_child
        root.right_child = right.left_child
        right.left_child = root
        return right

    @staticmethod
    def rotate_right(root: TreapNode) -> TreapNode:
        left = root.left_child
        root.left_child = left.right_child
        left.right_child = root
        return left

    def insert(self, key: int, priority: int):
        """ Key and priority individually guaranteed not to be in the tree already """
        def _insert(root: TreapNode) -> TreapNode:
            if root is None:
                return TreapNode(key, priority)
            if key < root.key:
                root.left_child = _insert(root.left_child)
                if root.left_child.priority > root.priority:
                    root = Treap.rotate_right(root)
                return root
            elif key > root.key:
                root.right_child = _insert(root.right_child)
                if root.right_child.priority > root.priority:
                    root = Treap.rotate_left(root)
                return root
            else:
                raise Exception(f"Key {key} already in tree")

        self.root = _insert(self.root)

    def delete(self, key: int):
        """ Key guaranteed to be in the tree.

        Use algorithm presented in notes where a priority of -math.inf is assigned before rotating to leaf. """
        def _delete(root: TreapNode) -> TreapNode:
            if root is None:
                raise Exception(f"Key {key} not in tree")
            if key < root.key:
                root.left_child = _delete(root.left_child)
                return root
            elif key > root.key:
                root.right_child = _delete(root.right_child)
                return root
            else:
                # key == root.key
                # Note that it is actually not necessary to reassign the priority
                # root.priority = -math.inf
                return _rotate_to_leaf(root)

        def _rotate_to_leaf(root: TreapNode) -> TreapNode:
            if root.left_child is None:
                if root.right_child is None:
                    # chop off leaf
                    return None
                else:
                    # only right child
                    # optimization compared to notes example: simply promote the child
                    return root.right_child
            else:
                if root.right_child is None:
                    # only left child
                    return root.left_child
                else:
                    # has two children
                    if root.left_child.priority > root.right_child.priority:
                        root = Treap.rotate_right(root)
                        root.right_child = _rotate_to_leaf(root.right_child)
                        return root
                    else:
                        # root.left_child.priority < root.right_child.priority
                        root = Treap.rotate_left(root)
                        root.left_child = _rotate_to_leaf(root.left_child)
                        return root

        self.root = _delete(self.root)
