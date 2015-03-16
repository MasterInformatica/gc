from time import time

class Timer:
    def __init__(self):
        self.start = time()
    
    def finish(self):
        return self.start - time()
        
