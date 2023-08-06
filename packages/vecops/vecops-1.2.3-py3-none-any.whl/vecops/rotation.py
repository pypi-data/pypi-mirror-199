from vecops.multiplication import Multiplication
from math import sin, cos, pi

class Rotation:

    @staticmethod
    def rotate2D(vector2D : list[list[int]], radX = 0, radY = 0) -> list[list[int]]:
        '''Rotates given vector in order x->y
            Input matrix format: [[x],[y]]'''

        rotationMatrix = [[cos(radX), -sin(radX)],[sin(radX), cos(radX)]]
        
        vector2D = Multiplication.multiplyMatrices(rotationMatrix, vector2D)

        rotationMatrix = [[cos(radY), -sin(radY)],[sin(radY), cos(radY)]]

        vector2D = Multiplication.multiplyMatrices(rotationMatrix, vector2D)

        return vector2D


    @staticmethod
    def rotate3D(vector3D : list[list[int]], radX = 0, radY = 0, radZ = 0) -> list[list[int]]:
        '''Rotates given vector in order x->y->z
            Input matrix format: [[x],[y],[z]]'''

        rotationMatrix = [[1,0,0],[0, cos(radX), -sin(radX)], [0, sin(radX), cos(radX)]]

        vector3D = Multiplication.multiplyMatrices(rotationMatrix, vector3D)

        rotationMatrix = [[cos(radY), 0, sin(radY)], [0,1,0], [-sin(radY), 0, cos(radY)]]

        vector3D = Multiplication.multiplyMatrices(rotationMatrix, vector3D)

        rotationMatrix = [[cos(radZ), -sin(radZ), 0], [sin(radZ), cos(radZ), 0], [0,0,1]]

        vector3D = Multiplication.multiplyMatrices(rotationMatrix, vector3D)

        return vector3D