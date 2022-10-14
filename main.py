import fractions


def normalizeMatrix(matrix):
    minVal = matrix[0][0]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            element = matrix[row][col]
            if element < minVal:
                minVal = element
    if minVal <= 0:
        normVal = abs(minVal) + 1
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                matrix[row][col] += normVal

        print("\n\tThe normalized game matrix is:\n")
        printMatrix(matrix)
        print("\n----------------------------------------------\n")
        return matrix

    else:
        return matrix


def getMatrix():
    while True:
        print("Welcome to the Simplex solver!")
        # matrixFile = input("Enter a text file with your matrix to solve >")
        matrixFile = "game3-1.txt"
        if matrixFile.endswith(".txt"):
            G = []
            with open(matrixFile) as f:
                lines = f.readlines()
                m = 0
                count = 0
                for line in lines:
                    elements = line.split()
                    tempRow = []
                    for element in elements:
                        tempRow.append(fractions.Fraction(int(element)))
                    G.append(tempRow)
                    n = len(elements)
                    count += n
                    m += 1
            f.close()
            if m * n != count:
                print("Sorry, the matrix you entered was not filled out correctly")
            else:
                break
        else:
            print("Sorry, the file you entered was not a text file")

    print("\n\tThe matrix you entered was:\n")
    printMatrix(G)
    print("\n----------------------------------------------\n")
    G = normalizeMatrix(G)
    return G


def printMatrix(m):
    for i in range(len(m)):
        outString = ""
        for j in range(len(m[0])):
            outString += f'{m[i][j].limit_denominator().__str__(): >7}\t'

        print(outString)


def makeTableau(mat, m, n):
    """
    Prints out format of first tableau
    :param mat: original game matrix
    :param m: rows of 'mat'
    :param n: cols of 'mat'
    """

    # identity matrix is mxm dimensions (row x row from game matrix)
    identityMatrix = createIdentityMatrix(m)

    rows = m + 1
    cols = n + m + 1
    tableau = []
    for i in range(rows):
        tempRow = []
        if i < rows - 1:  # all rows of game matrix
            for j in range(cols):
                if j < n:  # columns of game matrix
                    tempRow.append(mat[i][j])

                elif j < cols - 1:  # columns of identity matrix
                    tempRow.append(identityMatrix[i][j - n])
                else:  # last column in tableau
                    # fill with 1's
                    tempRow.append(fractions.Fraction(1))

        else:  # Last row in tableau
            for j in range(cols):
                if j < n:  # columns of game matrix
                    # fill with -1's
                    tempRow.append(fractions.Fraction(-1))

                elif j < cols - 1:  # columns of identity matrix
                    # fill with zero's
                    tempRow.append(fractions.Fraction(0))

                else:  # last column in tableau
                    # fill with zero
                    tempRow.append(fractions.Fraction(0))
        tableau.append(tempRow)
    print("\n\tTableau #1 :\n")
    printMatrix(tableau)
    return tableau


def createIdentityMatrix(m):
    """
    Returns an Identity matrix with dimensions mxm
    :param m: row and column dimension
    :return: identityMatrix
    """
    oneIDX = 0
    identityMatrix = []
    for i in range(m):
        tempRow = []
        for j in range(m):
            if j == oneIDX:
                tempRow.append(fractions.Fraction(1))
            else:
                tempRow.append(fractions.Fraction(0))
        oneIDX += 1
        identityMatrix.append(tempRow)
    return identityMatrix


def findPivot(matrix):
    """
    **When there is no negative value in the bottom row, the game is over**
    :param matrix:
    :return:
    """
    # find pivot column
    lastRow = matrix[-1][:-1]  # grab last row and remove last column
    pivotCol = 0
    for i in range(len(lastRow)):
        if lastRow[i] < lastRow[pivotCol]:
            pivotCol = i

    if lastRow[pivotCol] >= 0:
        print("\n----------------------------------------------")
        print('\nGame over! \nThere is no negative value left in the bottom row!!')
        return 0, 0, True

    # find pivot row
    pivotRow = 0
    result = matrix[0][-1] / matrix[0][pivotCol]
    for i in range(1, len(matrix) - 1):
        denominator = matrix[i][pivotCol]
        numerator = matrix[i][-1]
        if (numerator / denominator < result) and (numerator / denominator > 0):
            result = numerator / denominator
            pivotRow = i

    print(f'\n{matrix[pivotRow][pivotCol]} is the pivot found at ({pivotRow},{pivotCol})')
    print("\n----------------------------------------------\n")

    return pivotRow, pivotCol, False


def calcNextTableau(tableau, pivotRow, pivotCol, counter):
    newPivotRow = []

    # calculate new pivot row --> divide entire row by pivot value
    pivotVal = tableau[pivotRow][pivotCol]
    for element in tableau[pivotRow]:
        newPivotRow.append(element / pivotVal)
    # -------------------------------------------------------------

    # calculate the remaining rows --> currentVal - (valInPivotCol * newPivotVal)
    newTableau = []
    for i in range(len(tableau)):
        newRow = []
        if i != pivotRow:
            oldRow = tableau[i]
            valInPivotCol = oldRow[pivotCol]  # changes for each row that is being calculated
            for j in range(len(oldRow)):
                result = oldRow[j] - (valInPivotCol * newPivotRow[j])
                newRow.append(result)

            newTableau.append(newRow)

        else:
            newTableau.append(newPivotRow)

    print(f"\n\tTableau #{counter}:\n")
    printMatrix(newTableau)
    return newTableau


if __name__ == '__main__':
    solved = False
    game = getMatrix()
    tab = makeTableau(game, len(game), len(game[0]))

    cntr = 2
    while not solved:
        r, c, solved = findPivot(tab)
        if not solved:
            tab = calcNextTableau(tab, r, c, cntr)
            cntr += 1
        if cntr >= 11:
            break

    # TODO: write function for printing out the final values of the game
    #       1) print value of the game
    #           - max value V is in bottom right corner of last tab
    #           - V = 1/value_of_game
    #           - x variables are the far right values above the last row
    #           - y variables are the last row in the Im columns
    #       2) print mixed strategies for both players
    #           - x1 = ?, x2 = ?, x3 ...
    #           - y1 = ?, y2 = ?, y3 ...

    # TODO: Add case where game ends when number of tableaus
    #       is equal to the number of rows in the OG tableau
    #       ** See game2.txt for testing
    #       *** probably isn't needed because the game should end organically
