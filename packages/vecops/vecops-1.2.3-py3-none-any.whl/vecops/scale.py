from vecops.multiplication import Multiplication

class Scale:
    
    @staticmethod
    def scale2D(vector2D : list[list[int]], ratioX = 0, ratioY = 0) -> list[list[int]]:
        '''Scales given vector
           Input matrix format: [[x],[y]]'''

        scaleMatrix = [[ratioX, 0], [0, ratioY]]

        return Multiplication.multiplyMatrices(scaleMatrix, vector2D)

    @staticmethod
    def scale3D(vector3D: list[list[int]], ratioX = 0, ratioY = 0, ratioZ = 0):
        '''Scales given vector
           Input matrix format: [[x],[y],[z]]'''
        
        scaleMatrix = [[ratioX, 0, 0], [0, ratioY, 0], [0, 0, ratioZ]]

        return Multiplication.multiplyMatrices(scaleMatrix, vector3D)