from vecops.length import Length
from vecops.subtraction import Subtraction

class Distance:

    @staticmethod
    def distance2D(A : list[list[int]], B : list[list[int]]) -> float:
        '''Returns distance of given vector B from vector A
           Input matrix format: [[x],[y]]'''

        return Length.length2D(Subtraction.subtractVectors(A,B))
    
    @staticmethod
    def distance3D(A : list[list[int]], B : list[list[int]]) -> float:
        '''Returns distance of given vector B from vector A
           Input matrix format: [[x],[y],[z]]'''
        
        return Length.length3D(Subtraction.subtractVectors(A,B))