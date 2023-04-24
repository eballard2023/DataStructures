# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import csv
import math
import random
import traceback
from typing import Type, Union

import splay
import splay_reference


def print_test_failure(trace: str, reference_result: str, student_result: str):
    print(f"""\
Test failed:
---> Tracefile:
{trace}
---> Your solution:
{student_result}
---> Correct solution:
{reference_result}""")


AnyTree = Union[splay_reference.SplayTree, splay.SplayTree]
AnyNode = Union[splay_reference.SplayNode, splay.SplayNode]


def validate_tree(tree: AnyTree) -> str:
    def _valid(root: AnyNode) -> str:
        if root is None:
            return None

        left_key = root.left_child.key if root.left_child else -math.inf
        right_key = root.right_child.key if root.right_child else math.inf
        if not (left_key < root.key < right_key):
            return f"Root key {root.key} not in between child keys, left: {left_key}, right: {right_key}"

        if left_reason := _valid(root.left_child):
            return left_reason
        return _valid(root.right_child)

    return _valid(tree.root)


def generate_trace(size: int, final_size: int = None, splays: int = 0) -> tuple[list[str], set[int]]:
    """ If final_size is specified < size, then deletions will be inserted so that the tree ends up with final_size nodes.

    Returns a trace and an expected final set of keys. """
    numbers = list(range(1, size+1))
    random.shuffle(numbers)
    if (final_size is None or final_size >= size) and splays == 0:
        return [f"insert,{n}" for n in numbers] + ["dump"], set(numbers)

    to_delete = list(range(1, size+1))
    random.shuffle(to_delete)
    to_delete = to_delete[:size - final_size]
    not_deleted = set(numbers) - set(to_delete)
    for n in to_delete:
        index = numbers.index(n)
        numbers.insert(random.randint(index+1, len(numbers)), -n)
    trace = [f"insert,{n}" if n >
             0 else f"delete,{-n}" for n in numbers]

    for _ in range(0, splays):
        n = random.randint(0, len(trace))
        n = numbers[random.randrange(0, size)]
        trace.insert(n, f"splay,{n}")

    return trace + ["dump"], not_deleted


def run_trace(trace: list[str], SplayTree: Type):
    tree: AnyTree = SplayTree()
    reader = csv.reader(trace)
    lines = [l for l in reader]
    for l in lines:
        if l[0] == 'insert':
            tree.insert(int(l[1]))
        if l[0] == 'delete':
            tree.delete(int(l[1]))
        if l[0] == 'splay':
            tree.splay(int(l[1]))
        if l[0] == 'dump':
            return tree, splay.dump(tree), validate_tree(tree)


def test_trace(trace: list[str], expected_set: set[int]):
    ref_tree, ref, ref_invalid_reason = run_trace(
        trace, splay_reference.SplayTree)
    assert set((n.key for n in ref_tree)) == expected_set
    try:
        _, student, student_invalid_reason = run_trace(trace, splay.SplayTree)
    except Exception:
        student, student_invalid_reason = None, traceback.format_exc()
    if ref_invalid_reason:
        raise Exception(
            "Reference implementation produced invalid splay tree", ref, ref_invalid_reason, trace)
    if ref != student:
        print_test_failure("\n".join(trace), ref, student)
        if student_invalid_reason:
            print("\nIn addition, the student tree is not a valid splay tree.")
            print(student_invalid_reason)
        return False
    return True


def notes_insert_example(SplayTree: Type, SplayNode: Type):
    tree: AnyTree = SplayTree(
        SplayNode(30,
                  SplayNode(10),
                  SplayNode(50,
                            None,
                            SplayNode(60,
                                      SplayNode(55,
                                                None,
                                                SplayNode(57)
                                                )
                                      )
                            )
                  )
    )
    tree.insert(59)
    return splay.dump(tree)


def notes_delete_example(SplayTree: Type, SplayNode: Type):
    tree: AnyTree = SplayTree(
        SplayNode(59,
                  SplayNode(57,
                            SplayNode(50,
                                      SplayNode(30,
                                                SplayNode(10)
                                                ),
                                      SplayNode(55)
                                      )
                            ),
                  SplayNode(60)
                  )
    )
    tree.delete(30)
    return splay.dump(tree)


if __name__ == "__main__":
    passed = True

    ref = notes_insert_example(
        splay_reference.SplayTree, splay_reference.SplayNode)
    student = notes_insert_example(splay.SplayTree, splay.SplayNode)
    if ref != student:
        print_test_failure("Insert Example 6.1 from the notes", ref, student)
        passed = False

    if passed:
        ref = notes_delete_example(
            splay_reference.SplayTree, splay_reference.SplayNode)
        student = notes_delete_example(splay.SplayTree, splay.SplayNode)
        if ref != student:
            print_test_failure(
                "Delete Example 7.1 from the notes", ref, student)
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

    if passed:
        print("Testing insert and delete with splays")
        for size in range(1, 201):
            trace, expected_set = generate_trace(size, size//2, size//2)
            passed = test_trace(trace, expected_set)
            if not passed:
                break

    if passed:
        print("Testing insert and delete down to empty with splays")
        for size in range(1, 201, 40):
            trace, expected_set = generate_trace(size, 0, size//2)
            passed = test_trace(trace, expected_set)
            if not passed:
                break
