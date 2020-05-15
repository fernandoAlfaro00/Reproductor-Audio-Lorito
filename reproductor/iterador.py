class Cuadrados(object):
    def __init__(self, n=0): 
        
        self.n = n

    def __iter__(self): 
        
        return self

    def next(self):
        actual = self.n**2
        self.n += 1
        return actual