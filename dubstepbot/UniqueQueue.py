'''
Created on Sep 21, 2013

@author: Kevin
'''
#needed to keep track of processed comments and a queue to remove previous comments
from collections import deque
global queue
global ID
global size
class UniqueQueue():

    def __init__(self):
        self.queue = deque()
        self.ID = set()
        self.size = 0
        
    def append(self, key):
        if key in self.ID:
            return False
        else:
            self.queue.append(key)
            self.ID.add(key)
            self.size+=1
            return True
            
    def popleft(self):
        key = self.queue.popleft()
        self.ID.remove(key)
        self.size-=1
        return key
    
    def contains(self, key):
        return key in self.ID