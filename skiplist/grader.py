# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import csv
import json
import random
import traceback
from typing import Type, Union

import skip_list
import skip_list_reference


def print_test_failure(trace: str, reference_result: str, student_result: str):
    print(f"""\
Test failed:
---> Tracefile:
{trace}
---> Your solution:
{student_result}
---> Correct solution:
{reference_result}""")


AnyList = Union[skip_list_reference.SkipList, skip_list.SkipList]
AnyNode = Union[skip_list_reference.SkipListNode, skip_list.SkipListNode]


def validate_list(slist: AnyList) -> str:
    if sorted(slist, key=lambda n: n.key) != list(slist):
        return "List not sorted"

    for h in range(0, slist.height):
        last_key = "head"
        expected_next_at_height = slist.pointers[h]
        for node in slist:
            if node.height > h:
                if node != expected_next_at_height:
                    return f"Node with key {node.key} should have been the pointer target of node with key {last_key} at level {h}"
                last_key = node.key
                expected_next_at_height = node.pointers[h]
        if expected_next_at_height is not None:
            return f"Node with key {last_key} is last with level {h} but does not point to None at that level"

    for n in slist:
        if n.height > slist.height:
            return f"Node with key {node.key} is taller than the head pointer list"

    return None


def random_height():
    max_height = 16
    height = 1
    while height < max_height and random.randint(0, 1) == 1:
        height += 1
    return height


def generate_trace(size: int, final_size: int = None, search=False) -> tuple[list[str], set[int]]:
    """ If final_size is specified < size, then deletions will be inserted so that the tree ends up with final_size nodes.

    Returns a trace and an expected final set of keys. """
    numbers = list(range(1, size+1))
    random.shuffle(numbers)

    if final_size is None or final_size >= size:
        if search:
            search_key = random.randrange(1, size+1)
            final_command = f"search,{search_key}"
        else:
            final_command = "dump"
        return [f"insert,{n},{random_height()}" for n in numbers] + [final_command], set(numbers)

    to_delete = list(range(1, size+1))
    random.shuffle(to_delete)
    to_delete = to_delete[:size - final_size]
    not_deleted = set(numbers) - set(to_delete)
    for n in to_delete:
        index = numbers.index(n)
        numbers.insert(random.randint(index+1, len(numbers)), -n)
    if search:
        search_key = list(not_deleted)[random.randrange(0, final_size)]
        final_command = f"search,{search_key}"
    else:
        final_command = "dump"
    return [f"insert,{n},{random_height()}" if n > 0 else f"delete,{-n}" for n in numbers] + [final_command], not_deleted


def run_trace(trace: list[str], SkipList: Type):
    slist: AnyList = SkipList()
    reader = csv.reader(trace)
    lines = [l for l in reader]
    for l in lines:
        if l[0] == 'insert':
            slist.insert(int(l[1]), int(l[2]))
        if l[0] == 'delete':
            slist.delete(int(l[1]))
        if l[0] == 'search':
            return slist, json.dumps(slist.search(int(l[1]))), validate_list(slist)
        if l[0] == 'dump':
            return slist, skip_list.dump(slist), validate_list(slist)


def test_trace(trace: list[str], expected_set: set[int]):
    ref_list, ref, ref_invalid_reason = run_trace(
        trace, skip_list_reference.SkipList)
    assert set((n.key for n in ref_list)
               ) == expected_set
    try:
        _, student, student_invalid_reason = run_trace(
            trace, skip_list.SkipList)
    except Exception:
        student, student_invalid_reason = None, traceback.format_exc()
    if ref_invalid_reason:
        raise Exception(
            "Reference implementation produced invalid skip list", ref, ref_invalid_reason, trace)
    if ref != student:
        print_test_failure("\n".join(trace), ref, student)
        if student_invalid_reason:
            print("\nIn addition, the student tree is not a valid skip list.")
            print(student_invalid_reason)
        return False
    return True


def notes_search_example(SkipList: Type):
    slist: AnyList = SkipList()
    keys = [3, 10, 11, 30, 37, 42, 80]
    heights = [2, 1, 3, 2, 1, 4, 1]
    for k, h in zip(keys, heights):
        slist.insert(k, h)
    return json.dumps(slist.search(37))


def notes_insert_example(SkipList: Type):
    slist: AnyList = SkipList()
    keys = [3, 10, 11, 30, 37, 42, 80]
    heights = [2, 1, 3, 2, 1, 4, 1]
    for k, h in zip(keys, heights):
        slist.insert(k, h)
    slist.insert(32, 4)
    return skip_list.dump(slist)


def notes_delete_example(SkipList: Type):
    slist: AnyList = SkipList()
    keys = [3, 10, 11, 30, 32, 37, 42, 80]
    heights = [2, 1, 3, 2, 4, 1, 4, 1]
    for k, h in zip(keys, heights):
        slist.insert(k, h)
    slist.delete(32)
    return skip_list.dump(slist)


if __name__ == "__main__":
    passed = True

    ref = notes_search_example(skip_list_reference.SkipList)
    student = notes_search_example(skip_list.SkipList)
    if ref != student:
        print_test_failure("Insert Example 6.1 from the notes", ref, student)
        passed = False

    if passed:
        ref = notes_insert_example(skip_list_reference.SkipList)
        student = notes_insert_example(skip_list.SkipList)
        if ref != student:
            print_test_failure(
                "Insert Example 6.1 from the notes", ref, student)
            passed = False

    if passed:
        ref = notes_delete_example(skip_list_reference.SkipList)
        student = notes_delete_example(skip_list.SkipList)
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
        print("Testing insert only with search")
        for size in range(1, 201):
            trace, expected_set = generate_trace(size, search=True)
            passed = test_trace(trace, expected_set)
            if not passed:
                break

    if passed:
        print("Testing insert and delete with search")
        for size in range(1, 201):
            trace, expected_set = generate_trace(size, size//2+1, search=True)
            passed = test_trace(trace, expected_set)
            if not passed:
                break
