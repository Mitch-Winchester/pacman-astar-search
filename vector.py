import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.threshold = 0.000001
    
    #arithmetic methods for computing vector distance
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
            return None
        
    def __eq__(self, other):
        if abs(self.x - other.x) < self.threshold:
            if abs(self.y - other.y) < self.threshold:
                return True
        return False
    
    #methods to compute magnitude of vectors
    def magnitudeSquared(self):
        return self.x**2 + self.y**2
    
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    
    #method to store a vector
    def copy(self):
        return Vector2(self.x, self.y)
    
    #methods to help keep code clean
    def asTuple(self):
        return self.x, self.y
    
    def asInt(self):
        return int(self.x), int(self.y)
    