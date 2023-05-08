from __future__ import annotations
import json
from typing import List

def hash(username:str,j:int,m:int) -> int:
    # Adjust accordingly
    result = 0
    return(result)

# Bloom Filter Class
# DO NOT MODIFY

class Bloom():
    def __init__(self,
                 m         = int,
                 k         = int,
                 fpmax     = float,
                 threshold = int,
                 bitarray  = List[int],
                 usernamedict   = dict,
                 n         = int):
        self.m         = m
        self.k         = k
        self.fpmax     = fpmax
        self.threshold = threshold
        self.bitarray  = [0] * m
        self.usernamedict   = {}
        self.n         = 0

    def dump(self) -> str:
        def _to_dict(b) -> str:
            dict_repr = ''.join([str(i) for i in self.bitarray])
            return(dict_repr)
        return(_to_dict(self.bitarray))

    # If a username has been hacked, record it.
    # If it's hacked threshold times, insert it into the bloom filter.
    def hack(self,username: str):
        # The dummy line is just to make it run.
        dummy = 0

    # Insert a username into the bloom filter.
    def insert(self,username: str):
        # The dummy line is just to make it run.
        dummy = 0

    # Check if a username is in the bloom filter.
    def check(self,username:str) -> str:
        # Adjust accordingly
        conclusion = 'figure this out'
        return(json.dumps({'username':username,'status':conclusion}))