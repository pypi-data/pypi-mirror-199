from vecops.addition import Addition

class Translation:
    @staticmethod
    def move2D(vector2D : list[list[int]], addX = 0.0, addY = 0.0) -> list[list[int]]:
        '''Moves given vector
           Input matrix format: [[x],[y]]'''

        moveMatrix = [[addX],[addY]]
        vector2D = Addition.addMatrices(vector2D, moveMatrix)

        return vector2D

    @staticmethod
    def move3D(vector3D : list[list[int]], addX = 0.0, addY = 0.0, addZ = 0.0):
        '''Moves given vector
           Input matrix format: [[x],[y],[z]]'''

        moveMatrix = [[addX],[addY],[addZ]]

        vector3D = Addition.addMatrices(vector3D, moveMatrix)

        return vector3D