#Task 5
from math import sqrt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Point:: x: {self.x} y: {self.y}"

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    

    def Euclidian(self,other):
        distance = sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        return distance

class Vector(Point):
    def __init__(self, x, y):
         super().__init__(x,y)

    def __str__(self):
        return f"Vector:: x: {self.x} y: {self.y}"

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        new_vec = Vector(new_x, new_y)
        return new_vec
    

if __name__ == "__main__":
    p1 = Point(1,2)
    p2 = Point(2,1)
    print(p1)
    print(f"Is 1,2 equal to 2,1: {p1 == p2}\n")
    print(f"distance bewtween points 1,2 and 2,1 is: {p1.Euclidian(p2)}")

    v1 = Vector(3,4)
    v2 = Vector(10,8)
    v3 = v1 + v2
    print(v1)
    print(f"Adding vectors 3,4 with 10, 8 {str(v3)}")
