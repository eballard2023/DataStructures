# This is provided to you so that you can test your bst.py file with a particular tracefile.

import argparse
import csv
import bloom

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-tf', '--tracefile')
    args = parser.parse_args()
    tracefile = args.tracefile

    t = None
    with open(tracefile, "r") as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
        for l in lines:
            if l[0][0] == '#':
                next
            if l[0] == 'hash':
                print(bloom.hash(l[1],int(l[2]),int(l[3])))
            if l[0] == 'initialize':
                t = bloom.Bloom(m = int(l[1]), k = int(l[2]), threshold = int(l[3]), fpmax = float(l[4]))
            if l[0] == 'hack':
                t.hack(l[1])
            if l[0] == 'check':
                print(t.check(l[1]))
            if l[0] == 'dump':
                print(t.dump())