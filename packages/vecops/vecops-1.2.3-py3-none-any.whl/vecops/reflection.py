from vecops.multiplication import Multiplication
from vecops.subtraction import Subtraction

class Reflection:

    @staticmethod
    def reflection2D(rayVector : list[list[int]], normalVector : list[list[int]]) -> list[list[int]]:
        '''Returns reflected vector
           Input matrices format: [[x],[y]]'''
        
        tempVector = Multiplication.multiplyByScalar((2 * Multiplication.dotProduct2D(normalVector, rayVector)), normalVector)
        resultMatrix = Subtraction.subtractVectors(rayVector, tempVector)

        return resultMatrix
    
    @staticmethod
    def reflection3D(rayVector : list[list[int]], normalVector : list[list[int]]) -> list[list[int]]:
        '''Returns reflected vector
           Input matrices format: [[x],[y],[z]]'''

        tempVector = Multiplication.multiplyByScalar((2 * Multiplication.dotProduct3D(normalVector, rayVector)), normalVector)    
        resultMatrix = Subtraction.subtractVectors(rayVector, tempVector)

        return resultMatrix        

