import random

class Subtraction:

    @staticmethod
    def generateRandomMatricesForSubtraction() -> tuple:
        w = random.randint(2,5)
        h = random.randint(2,5)

        A = [[random.randint(1,20) for x in range(w)] for y in range(h)]
        B = [[random.randint(1,20) for x in range(w)] for y in range(h)]
        return (A,B)
    
    @staticmethod
    def subtractMatrices(A : list[list[int]], B : list[list[int]]) -> list[list[int]]:
        '''Subtract given matrix B from matrix A and return result as a new matrix'''

        if len(A) != len(B):
            print("Invalid dimensions!")
            return

        if len(A[0]) != len(B[0]):
            print("Invalid dimensions!")
            return

        Matrix = [[0 for x in range(len(A[0]))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(A[0])):                
                Matrix[i][j] = A[i][j] - B[i][j]
        
        return Matrix
    
    @staticmethod
    def subtractVectors(A : list[list[int]], B : list[list[int]]) -> list[list[int]]:
        '''Subtract given vector B from vector A and return result as a new vector'''

        if len(A) != len(B):
            print("Invalid dimensions!")
            return

        if len(A[0]) != len(B[0]):
            print("Invalid dimensions!")
            return
        
        Vector = [[0 for x in range(len(A[0]))]for y in range(len(A))]

        for i in range(len(A)):
            Vector[i][0] = A[i][0] - B[i][0]

        return Vector