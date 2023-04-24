# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import csv
import math
import random
import traceback
from typing import Type, Union

import treap
import treap_reference


def print_test_failure(trace: str, reference_result: str, student_result: str):
    print(f"""\
Test failed:
---> Tracefile:
{trace}
---> Your solution:
{student_result}
---> Correct solution:
{reference_result}""")


AnyTreap = Union[treap_reference.Treap, treap.Treap]
AnyNode = Union[treap_reference.TreapNode, treap.TreapNode]


def validate_tree(tree: AnyTreap) -> str:
    def _valid(root: AnyNode) -> str:
        if root is None:
            return None

        left_key = root.left_child.key if root.left_child else -math.inf
        right_key = root.right_child.key if root.right_child else math.inf
        if not (left_key < root.key < right_key):
            return f"Root key {root.key} not in between child keys, left: {left_key}, right: {right_key}"

        left_priority = root.left_child.priority if root.left_child else -math.inf
        right_priority = root.right_child.priority if root.right_child else -math.inf
        if not (root.priority > left_priority and root.priority > right_priority):
            return f"Root key {root.key} does not have greater priority than children, left: {left_priority}, right: {right_priority}"

        if left_reason := _valid(root.left_child):
            return left_reason
        return _valid(root.right_child)

    return _valid(tree.root)


def generate_trace(size: int, final_size: int = None) -> tuple[list[str], set[tuple[int, int]]]:
    """ If final_size is specified < size, then deletions will be inserted so that the tree ends up with final_size nodes.

    Returns a trace and an expected final set of keys and priorities. """
    numbers = list(range(1, size+1))
    random.shuffle(numbers)
    priorities = list(range(1, size+1))
    random.shuffle(priorities)
    if final_size is None or final_size >= size:
        return [f"insert,{n},{p}" for n, p in zip(numbers, priorities)] + ["dump"], set(zip(numbers, priorities))

    to_delete = list(range(1, size+1))
    random.shuffle(to_delete)
    to_delete = to_delete[:size - final_size]
    not_deleted = set(numbers) - set(to_delete)
    for n in to_delete:
        index = numbers.index(n)
        numbers.insert(random.randint(index+1, len(numbers)), -n)

    trace = []
    prio_index = 0
    expected_set = set()
    for n in numbers:
        if n > 0:
            p = priorities[prio_index]
            trace.append(f"insert,{n},{p}")
            if n in not_deleted:
                expected_set.add((n, p))
            prio_index += 1
        else:
            trace.append(f"delete,{-n}")

    return trace + ["dump"], expected_set


def run_trace(trace: list[str], Treap: Type):
    tree: AnyTreap = Treap()
    reader = csv.reader(trace)
    lines = [l for l in reader]
    for l in lines:
        if l[0] == 'insert':
            tree.insert(int(l[1]), int(l[2]))
        if l[0] == 'delete':
            tree.delete(int(l[1]))
        if l[0] == 'dump':
            return tree, treap.dump(tree), validate_tree(tree)


def test_trace(trace: list[str], expected_set: set[tuple[int, int]]):
    ref_tree, ref, ref_invalid_reason = run_trace(trace, treap_reference.Treap)
    assert set(((n.key, n.priority) for n in ref_tree)) == expected_set
    try:
        _, student, student_invalid_reason = run_trace(trace, treap.Treap)
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


if __name__ == "__main__":
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
