# By Andrew Chen, UMD '24
# CMSC420 Spring 2023

import argparse
import csv

import aa

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-tf', '--tracefile')
    args = parser.parse_args()
    tracefile = args.tracefile

    tree = aa.AATree()
    with open(tracefile, "r") as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
        for l in lines:
            if l[0] == 'insert':
                tree.insert(int(l[1]))
            if l[0] == 'delete':
                tree.delete(int(l[1]))
            if l[0] == 'dump':
                print(aa.dump(tree))
