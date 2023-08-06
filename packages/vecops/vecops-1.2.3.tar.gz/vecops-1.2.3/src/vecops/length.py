from vecops.multiplication import Multiplication
from math import sqrt

class Length:

    @staticmethod
    def length2D(vector : list[list[int]]) -> float:
        '''Returns length of given 2D vector
           Input matrix format: [[x],[y]]'''

        return sqrt(Multiplication.dotProduct2D(vector, vector))
    
    @staticmethod
    def length3D(vector : list[list[int]]) -> float:
        '''Returns length of given 3D vector
           Input matrix format: [[x],[y],[z]]'''

        return sqrt(Multiplication.dotProduct3D(vector,vector))