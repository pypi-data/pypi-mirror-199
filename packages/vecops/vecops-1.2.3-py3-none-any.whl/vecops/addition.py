import random

class Addition:
    #method for testing
    @staticmethod
    def generateRandomMatricesForAddition() -> tuple:
        w = random.randint(2,5)
        h = random.randint(2,5)

        A = [[random.randint(1,20) for x in range(w)] for y in range(h)]
        B = [[random.randint(1,20) for x in range(w)] for y in range(h)]
        return (A,B)

    #adds two matrices
    @staticmethod
    def addMatrices(A:list[list[int]],B:list[list[int]]) -> list[list[int]]:
        '''Adds up A and B and returns result as a new matrix.'''
        if len(A) != len(B):
            print("Invalid dimensions!")
            return

        if len(A[0]) != len(B[0]):
            print("Invalid dimensions!")
            return

        Matrix = [[0 for x in range(len(A[0]))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(A[0])):                
                Matrix[i][j] = A[i][j] + B[i][j]
        
        return Matrix
    
    #todo: addNMatrices
    @staticmethod
    def addNMatrices(Matrices:list[list[list[int]]]) -> list[list[int]]:
        '''Adds up all matrices from given list of matrices and returns result as a new matrix.'''
        for i in range(1, len(Matrices)):
            if (len(Matrices[i]) != len(Matrices[i-1])) or (len(Matrices[i][0]) != len(Matrices[i-1][0])):
                print("Invalid dimensions!")
                return

        Matrix = Matrices[0]
        for index in range(1, len(Matrices)):
            tempMatrix = []
            for i in range(len(Matrix)):
                l = []
                for j in range(len(Matrix[i])):
                    l.append(Matrices[index][i][j] + Matrix[i][j])
                tempMatrix.append(l)
            Matrix = tempMatrix

        return Matrix

    @staticmethod
    def addScalarToMatrix(A:list[list[int]], s:float) -> list[list[int]]:
        '''Adds given scalar [s] to all elements of given matrix [A] and returns result as a new matrix.'''
        Matrix = [[0 for x in range(len(A[0]))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(A[0])):
                Matrix[i][j] = A[i][j] + s

        return Matrix

