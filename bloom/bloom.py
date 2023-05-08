from __future__ import annotations
import json
from typing import List
import math

def hash(username: str, j: int, m: int) -> int:
    ascii_convert = [ord(c) for c in username]
    

    ascii_add = sum(ascii_convert)

    concat = ascii_add
    while concat < m:
        concat = int(str(concat) + str(concat))

    jth = concat ** j

    result = int(str(jth)[:len(str(m))])

    result = result % m

    return result








# Bloom Filter Class
# DO NOT MODIFY

class Bloom():
    def __init__(self,
                 m         = int,
                 k         = int,
                 fpmax  = int,
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
       if username in self.usernamedict:
           
           self.usernamedict[username] += 1
       else:
           
           self.usernamedict[username] = 1
           
     
       if self.usernamedict[username] == self.threshold:
         
         self.insert(username)

    # Insert a username into the bloom filter.
    def insert(self, username: str):

        self.n = self.n + 1
        for x in range(1, self.k + 1):
            index = hash(username, x, self.m)
            self.bitarray[index] = 1
        
        
        false_pos = self.false_positive()
       

        if false_pos > self.fpmax:
            self.rebuild()
            
       


    def false_positive(self):
        prob = (1-(1-(1/self.m))**(self.k * self.n))**self.k
        return prob


    # Check if a username is in the bloom filter.
    # Check if a username is in the bloom filter.
    def check(self,username:str) -> str:
        for x in range(1, self.k + 1):
            index = hash(username,x,self.m)
            
            if self.bitarray[index] == 0:
                return json.dumps({'username': username, 'status': 'SAFE'})

        return json.dumps({'username': username, 'status': 'UNSAFE'})

    def rebuild(self):
            
            while self.false_positive() > self.fpmax / 2:
                self.m += 1
                
                # self.k = max(1, int((self.m / self.n) * math.log(2)))

            self.bitarray = [0] * self.m
            print(self.bitarray)
            
            for username in self.usernamedict:
                print(self.usernamedict)
                if self.usernamedict[username] >= self.threshold:
                    for x in range(1, self.k + 1):
                        index = hash(username, x, self.m)
                        self.bitarray[index] = 1
        

        
        
                


        
            
           

            
if __name__ == '__main__':
    bloom_filter = Bloom(7,4,.2,2)
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Jedd")
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Mikael")
    bloom_filter.hack("Peter")
    bloom_filter.hack("Jedd")
    bloom_filter.hack("Jedd")
    bloom_filter.hack("Jedd")
   
    
    # 01111

    print(bloom_filter.dump())

    