import copy


class Inverse:
    
    @staticmethod
    def findDeterminant(A:list[list[int]]) -> int:
        '''Finds the determinant of a given matrix [A] and returns him as an int.'''

        #In case we don't want to change our original matrix by calling this method.
        B = copy.deepcopy(A)  

        if len(B[0]) != len(B):
            print("Matrix is not square!")
            return

        sgn = 0
        nullCol = False

        for i in range(0,len(B)-1):
            for j in range(i,len(B)):

                if B[i][j] == 0:

                    for k in range(i+1, len(B)):

                        if B[k][j] != 0:
                            B[k], B[i] = B[i], B[k]
                            sgn += 1
                            nullCol = True
                            break
                    if nullCol == True:
                        nullCol = False
                    else:
                        nullCol = True

                if nullCol == True:
                    nullCol = False
                    continue

                for k in range(i+1, len(B)):
                    C = copy.deepcopy(B[k][j] / B[i][j])

                    for l in range(0, len(B[0])):
                        B[k][l] += B[i][l] * C * (-1)
                break

        sum = B[0][0]

        for i in range(1,len(B)):
            sum *= B[i][i]

        return (int)(sum * ((-1)**sgn))

    @staticmethod
    def isRegular(A:list[list[int]]) -> bool:
        '''Checks if given matrix [A] is regular and return boolean (true/false) value.'''

        if len(A[0]) != len(A):
            print("Matrix is not square!")
            return
        
        B = copy.deepcopy(A)
        
        if Inverse.findDeterminant(B) == 0:
            return False

        return True

    @staticmethod
    def REF(A:list[list[int]]) -> list[list[int]]:
        '''Finds out row echelon form of a given matrix [A] and returns result as a new matrix.'''

        nullCol = False
        
        for i in range(0,len(A)-1):
            for j in range(i,len(A)):

                if A[i][j] == 0:

                    for k in range(i+1, len(A)):

                        if A[k][j] != 0:
                            A[k], A[i] = A[i], A[k]
                            nullCol = True
                            break
                    if nullCol == True:
                        nullCol = False
                    else:
                        nullCol = True

                if nullCol == True:
                    nullCol = False
                    continue

                for k in range(i+1, len(A)):
                    C = A[k][j] / A[i][j]

                    for l in range(0, len(A[0])):
                        A[k][l] += A[i][l] * C * (-1)
                break 
        
        for i in range(0,len(A)):
            for j in range(0,len(A[0])):

                if A[i][j] != 0:
                    C = A[i][j]

                    for k in range(j,len(A[0])):
                        A[i][k] /= C
                    break

        return A
                            
    @staticmethod
    def RREF(A:list[list[int]]) -> list[list[int]]:
        '''Finds out reduced row echelon form of a given matrix [A] and returns result as a new matrix.'''

        Inverse.REF(A)

        for i in reversed(range(1, len(A))):
            for j in range(0,len(A[0])):

                if A[i][j] != 0:

                    for k in reversed(range(0,i)):
                        C = A[k][j] / A[i][j]

                        for l in range(j, len(A[0])):
                            A[k][l] += A[i][l] * C * (-1)
                    break

        return A

    @staticmethod
    def invertMatrix(A:list[list[int]]) -> list[list[int]]:
        '''Inverts given matrix [A] and returns result as a new matrix.'''

        if len(A[0]) != len(A):
            print("Matrix is not square!")
            return
        
        In = [[0 for x in range(len(A))] for y in range(len(A))]

        for i in range(0,len(A)):
            In[i][i] = 1

        found = False
        sgn = 0

        for i in range(0,len(A)):
            if A[i][i] == 0: #A[i][i] = pivot
                for j in range(i+1, len(A)):

                    if A[j][i] != 0:

                        A[i], A[j] = A[j], A[i]
                        In[i], In[j] = In[j], In[i]

                        sgn += 1
                        found = True

                if found == False:
                    print("Rows are not linearly independent!")
                    return
                found = False

            for j in range(i+1, len(A)):
                if A[j][i] != 0:
                    C = A[j][i] / A[i][i]

                    for k in range(0, len(A)):
                        A[j][k] += A[i][k] * C * (-1)
                        In[j][k] += In[i][k] * C * (-1)

        for i in reversed(range(1, len(A))):
            for j in reversed(range(0,i)):

                if A[j][i] != 0:
                    C = A[j][i] / A[i][i]                        
                    A[j][i] += A[i][i] * C * (-1)
                        
                    for k in range(0, len(A)):
                        In[j][k] += In[i][k] * C * (-1)
            
            
        for i in range(0,len(A)):
            for j in range(0,len(A)):
                In[i][j] /= A[i][i]
            A[i][i] /= A[i][i]
            
        return In

    @staticmethod
    def transposeMatrix(A:list[list[int]]) -> list[list[int]]:
        '''Transposes given matrix [A] and returns result as a new matrix.'''

        Matrix = [[0 for x in range(len(A))] for y in range(len(A[0]))]
        
        for i in range(len(A)):
            for j in range(len(A[0])):
                Matrix[j][i] = A[i][j]

        return Matrix

    
