import math

class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multByV2(self, v2):
        return V2(self.x*v2.x, self.y*v2.y)

    def multByV2_2(self, x, y):
        return V2(self.x*x, self.y*y)

    def dotByV2(self, v2):
        return self.x*v2.x + self.y*v2.y

    def dotByV2_2(self, x, y):
        return self.x*x + self.y*y

    def multByV1(self, a, flag= 0):
        if flag == 0:
            return V2(self.x*a, self.y*a)
        if flag == 1:
            return self.x*a + self.y*a

    def INT(self):
        self.x = int(self.x)
        self.y = int(self.y)
        return self

    def getMagnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        a = math.sqrt(self.x*self.x + self.y*self.y)
        return V2(self.x/a, self.y/a)

    def array(self):
        return [self.x, self.y]

    def ADD(self):
        return self.x+self.y

    def add(self, v):
        self.x += v.x
        self.y += v.y
        return self
    
    def neg(self):
        self.x *= -1
        self.y *= -1
        return self

class Matrix2x2:

    def __init__(self, v1, v2):
        self.x1 = v1.x
        self.x2 = v2.x
        self.y1 = v1.y
        self.y2 = v2.y
        self.firstVec = [self.x1, self.y1]
        self.firstV2 = V2(self.x1, self.y1)
        self.secondVec = [self.x2, self.y2]
        self.secondV2 = V2(self.x2, self.y2)
        self.thirdV2 = V2(self.x1, self.x2)
        self. fourthV2 = V2(self.y1, self.y2)
        self.matrixArray = [self.firstVec, self.secondVec]

    def multByV2(self, v2):
        a = self.firstV2.multByV1(v2.x)
        b = self.secondV2.multByV1(v2.y)
        return V2(a.x+b.x, a.y+b.y)

    def multByV2_2(self, x, y):
        a = self.firstV2.multByV1(x)
        b = self.secondV2.multByV1(y)
        return V2(a.x+b.x, a.y+b.y)

    def retMultByV2(self, v2):
        a = self.firstV2.multByV1(v2.x)
        b = self.secondV2.multByV1(v2.y)
        return a.x+b.x, a.y+b.y

    def retMultByV2_2(self, x, y):
        a = self.firstV2.multByV1(x)
        b = self.secondV2.multByV1(y)
        return a.x+b.x, a.y+b.y

    def multByV1(self, a):
        A = V2(self.x1 * a, self.x2 * a)
        B = V2(self.y1 * a, self.y2 * a)
        return Matrix2x2(A, B)

    def getDet(self):
        return self.x1*self.y2 - self.y1*self.x2

    def getInverse(self):
        a = 1/self.getDet()
        A = V2(self.y2, -self.x2)
        B = V2(-self.y1, self.x1)
        return Matrix2x2(A, B).multByV1(a)

    def multByM2x2_1(self, matrix):
        # get all dot products
        a = self.firstV2.dotByV2(matrix.thirdV2)
        b = self.secondV2.dotByV2(matrix.thirdV2)
        c = self.firstV2.dotByV2(matrix.fourthV2)
        d = self.secondV2.dotByV2(matrix.fourthV2)

        A = V2(a, b)
        B = V2(c, d)

        return Matrix2x2(A, B)
        
    def at(self, row, colm):
        return self.matrixArray[colm][row]

    def ADD(self):
        return V2(self.x1+self.x2, self.y1+self.y2)

    def negate(self):       # TODO --------------------------------------------------------------------
        pass


class Matrix2x2_t(Matrix2x2):
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.firstVec = [self.x1, self.y1]
        self.firstV2 = V2(self.x1, self.y1)
        self.secondVec = [self.x2, self.y2]
        self.secondV2 = V2(self.x2, self.y2)
        self.thirdV2 = V2(self.x1, self.x2)
        self. fourthV2 = V2(self.y1, self.y2)
        self.matrixArray = [self.firstVec, self.secondVec]


def make_rotation_Matrix_from_angle(angleInRad):
    a = V2(math.cos(angleInRad), math.sin(angleInRad))
    b = V2(math.sin(angleInRad), -math.cos(angleInRad))
    return Matrix2x2(a, b)