import copy
import random

class Multiplication:
    #method for testing 
    @staticmethod
    def generateRandomMatricesForMultiplication() -> tuple:

        w = random.randint(2,5)
        h = random.randint(2,5)
        w2 = random.randint(2,5)
        h2 = w

        A = [[random.randint(1,20) for x in range(w)] for y in range(h)]
        B = [[random.randint(1,20) for x in range(w2)] for y in range(h2)]
        return (A,B)
    
    @staticmethod
    def multiplyMatrices(A:list[list[int]],B:list[list[int]]) -> list[list[int]]:
        '''Multiplies two given matrices [A,B] and return result as a new matrix.'''

        if len(A[0]) != len(B):
            print("Invalid dimensions!")

        Matrix = [[0 for x in range(len(B[0]))] for y in range(len(A))]

        for i in range(0, len(A)):
            for j in range(0, len(B[0])):
                for k in range(0, len(A[0])):
                    Matrix[i][j] += A[i][k] * B[k][j]

        return Matrix

    @staticmethod
    def multiplyByScalar(s:float,A:list[list[int]]) -> list[list[int]]:
        '''Multiplies every element of a given matrix [A] by given scalar [s] and returns result as a new matrix.'''

        Matrix = [[0 for x in range(len(A[0]))] for y in range(len(A))]

        for i in range(0,len(A)):
            for j in range(0,len(A[0])):
                Matrix[i][j] = s * A[i][j]

        return Matrix  

    @staticmethod
    def multiplyByVector(Vec:list, A:list[list[int]]) -> list[list[int]]:
        '''Multiplies given matrix [A] by given vector [Vec] and returns result as a new matrix.'''

        if len(Vec) != len(A[0]):
            print("Invalid dimensions!")
            return

        Matrix = [[0 for x in range(len(A[0]))] for y in range(len(A))]
        
        for i in range(0,len(A)):
            for j in range(0,len(Vec)):
                Matrix[i][j] = A[i][j] * Vec[j]
                
        return Matrix

    #todo: multiplyNMatrices
    @staticmethod
    def multiplyNMatrices(Matrices:list[list[list[int]]]) -> list[list[int]]:
        '''Multiplies all matrices from given list of matrices and returns result as a new matrix.'''

        #check if matrices are multiplicable
        for i in range(1, len(Matrices)):
            if len(Matrices[i]) != len(Matrices[i-1][0]):
                print("Invalid dimensions!") #if for example matrix1 = [i][j] & matrix2 = [i][k] -> not multiplicable ([i][j] & [j][k] would be multiplicable)
                return
        
        Matrix = []

        #matrix0 x matrix1
        for i in range(len(Matrices[0])):
            sum = 0
            l = []
            for j in range(len(Matrices[1][0])):
                sum = 0
                for item in range(len(Matrices[0][i])):
                    sum += Matrices[0][i][item] * Matrices[1][item][j] 
                l.append(sum)
            Matrix.append(l)

        if len(Matrices) > 2:
            for index in range(2, len(Matrices)):
                tempMatrix = []
                for i in range(len(Matrix)): #row of matrix1
                    sum = 0
                    l = []
                    for j in range(len(Matrices[index][0])): #col of matrix2
                        sum = 0
                        for item in range(len(Matrix[i])):
                            sum += Matrix[i][item] * Matrices[index][item][j]
                        l.append(sum)
                    tempMatrix.append(l)
                Matrix = copy.deepcopy(tempMatrix)

        return Matrix

    @staticmethod
    def crossProduct3D(vector1 : list[list[int]], vector2 : list[list[int]]) -> list[list[int]]:
        '''Multiplies given 3D vectors
           Input matrices format: [[x],[y],[z]]'''

        if len(vector1)!= 3 or len(vector2) != 3:
            print("Wrong dimensions!")
            return
        
        productMatrix = [[(vector1[1][0]*vector2[2][0]) - (vector2[1][0]*vector1[2][0])],[(vector1[2][0]*vector2[0][0]) - (vector2[2][0]*vector1[0][0])],[(vector1[0][0]*vector2[1][0])-(vector2[0][0]*vector1[1][0])]]
        return productMatrix
    
    @staticmethod
    def dotProduct2D(vector1 : list[list[int]], vector2 : list[list[int]]) -> int:
        '''Multiplies given 2D vectors
           Input matrices format: [[x],[y]]'''
        
        if len(vector1)!=2 or len(vector2)!= 2:
            print("Wrong dimensions!")
            return
        
        productMatrix = (vector1[0][0] * vector2[0][0]) + (vector1[1][0] * vector2[1][0])
        return productMatrix
        
    @staticmethod
    def dotProduct3D(vector1 : list[list[int]], vector2 : list[list[int]]) -> int:
        '''Multiplies given 3D vectors
           Input matrices format: [[x],[y],[z]]'''
        
        if len(vector1)!=3 or len(vector2)!= 3:
            print("Wrong dimensions!")
            return
        
        productMatrix = ((vector1[0][0] * vector2[0][0]) + (vector1[1][0] * vector2[1][0]) + (vector1[2][0] * vector2[2][0]))
        return productMatrix
        


