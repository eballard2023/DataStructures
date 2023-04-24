# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import csv
import math
import random
import traceback
from typing import Type, Union

import aa
import aa_reference


def print_test_failure(trace: str, reference_result: str, student_result: str):
    print(f"""\
Test failed:
---> Tracefile:
{trace}
---> Your solution:
{student_result}
---> Correct solution:
{reference_result}""")


AnyTree = Union[aa_reference.AATree, aa.AATree]
AnyNode = Union[aa_reference.AANode, aa.AANode]


def validate_tree(tree: AnyTree) -> str:
    def _valid(root: AnyNode) -> str:
        if root is None:
            return None

        left_key = root.left_child.key if root.left_child else -math.inf
        right_key = root.right_child.key if root.right_child else math.inf
        if not (left_key < root.key < right_key):
            return f"Root key {root.key} not in between child keys, left: {left_key}, right: {right_key}"

        if aa_reference.AATree.red_left_child(root):
            return f"Root with key {root.key} has red left child"
        if aa_reference.AATree.red_red_right_child(root):
            return f"Root with key {root.key} has red right grandchild"
        left_level = root.left_child.level if root.left_child else 0
        right_level = root.right_child.level if root.right_child else 0
        if root.level != left_level + 1 or (root.level != right_level and root.level != right_level + 1):
            return f"Root with key {root.key} has invalid level relative to children, left: {left_level}, right: {right_level}"

        if left_reason := _valid(root.left_child):
            return left_reason
        return _valid(root.right_child)

    return _valid(tree.root)


def generate_trace(size: int, final_size: int = None) -> tuple[list[str], set[int]]:
    """ If final_size is specified < size, then deletions will be inserted so that the tree ends up with final_size nodes.

    Returns a trace and an expected final set of keys. """
    numbers = list(range(1, size+1))
    random.shuffle(numbers)
    if final_size is None or final_size >= size:
        return [f"insert,{n}" for n in numbers] + ["dump"], set(numbers)

    to_delete = list(range(1, size+1))
    random.shuffle(to_delete)
    to_delete = to_delete[:size - final_size]
    not_deleted = set(numbers) - set(to_delete)
    for n in to_delete:
        index = numbers.index(n)
        numbers.insert(random.randint(index+1, len(numbers)), -n)
    return [f"insert,{n}" if n > 0 else f"delete,{-n}" for n in numbers] + ["dump"], not_deleted


def run_trace(trace: list[str], AATree: Type):
    tree: AnyTree = AATree()
    reader = csv.reader(trace)
    lines = [l for l in reader]
    for l in lines:
        if l[0] == 'insert':
            tree.insert(int(l[1]))
        if l[0] == 'delete':
            tree.delete(int(l[1]))
        if l[0] == 'dump':
            return tree, aa.dump(tree), validate_tree(tree)


def test_trace(trace: list[str], expected_set: set[int]):
    ref_tree, ref, ref_invalid_reason = run_trace(trace, aa_reference.AATree)
    assert set((n.key for n in ref_tree)) == expected_set
    try:
        _, student, student_invalid_reason = run_trace(trace, aa.AATree)
    except Exception:
        student, student_invalid_reason = None, traceback.format_exc()
    if ref_invalid_reason:
        raise Exception(
            "Reference implementation produced invalid AA tree", ref, ref_invalid_reason, trace)
    if ref != student:
        print_test_failure("\n".join(trace), ref, student)
        if student_invalid_reason:
            print("\nIn addition, the student tree is not a valid AA tree.")
            print(student_invalid_reason)
        return False
    return True


def notes_insert_example(AATree: Type, AANode: Type):
    tree: AnyTree = AATree(
        AANode(10, 3,
               AANode(5, 2,
                      AANode(1, 1),
                      AANode(7, 1)
                      ),
               AANode(20, 3,
                      AANode(12, 2,
                             AANode(11, 1),
                             AANode(16, 2,
                                    AANode(13, 1),
                                    AANode(17, 1,
                                           None,
                                           AANode(19, 1))
                                    )
                             ),
                      AANode(30, 2,
                             AANode(25, 1),
                             AANode(45, 1))
                      )
               )
    )
    tree.insert(18)
    return aa.dump(tree)


def notes_delete_example(AATree: Type, AANode: Type):
    tree: AnyTree = AATree(
        AANode(4, 3,
               AANode(2, 2,
                      AANode(1, 1),
                      AANode(3, 1)
                      ),
               AANode(10, 3,
                      AANode(6, 2,
                             AANode(5, 1),
                             AANode(8, 2,
                                    AANode(7, 1),
                                    AANode(9, 1)
                                    )
                             ),
                      AANode(12, 2,
                             AANode(11, 1),
                             AANode(13, 1)
                             )
                      )
               )
    )
    tree.delete(1)
    return aa.dump(tree)


if __name__ == "__main__":
    passed = True

    ref = notes_insert_example(aa_reference.AATree, aa_reference.AANode)
    student = notes_insert_example(aa.AATree, aa.AANode)
    if ref != student:
        print_test_failure("Insert Example 5.1 from the notes", ref, student)
        passed = False

    if passed:
        ref = notes_delete_example(aa_reference.AATree, aa_reference.AANode)
        student = notes_delete_example(aa.AATree, aa.AANode)
        if ref != student:
            print_test_failure(
                "Delete Example 6.2 from the notes", ref, student)
            passed = False

    if passed:
        print("Testing insert only")
        for size in range(1, 201):
            trace, expected_set = generate_trace(size)
            passed = test_trace(trace, expected_set)
            if not passed:
                break

    if passed:
        print("Testing insert and delete")
        for size in range(1, 201):
            trace, expected_set = generate_trace(size, size//2)
            passed = test_trace(trace, expected_set)
            if not passed:
                break

    if passed:
        print("Testing insert and delete down to empty")
        for size in range(1, 201, 40):
            trace, expected_set = generate_trace(size, 0)
            passed = test_trace(trace, expected_set)
            if not passed:
                break
