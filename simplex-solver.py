import fractions


def normalizeMatrix(matrix):
    minVal = matrix[0][0]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            element = matrix[row][col]
            if element < minVal:
                minVal = element
    if minVal <= 0:
        k = abs(minVal) + 1
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                matrix[row][col] += k

        print("\n\tThe normalized game matrix is:\n")
        printMatrix(matrix)
        print("\n----------------------------------------------\n")
        return k, matrix

    else:
        return 0, matrix


def getMatrix():
    while True:
        print("Welcome to the Simplex solver!")
        matrixFile = input("Enter a text file with your matrix to solve >")
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
    k, G = normalizeMatrix(G)
    return k, G


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
    When there is no negative value in the bottom row, the game is over
    :param matrix:
    :return: pivotRow, pivotCol, gameOver
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

def calculateValueandOptimalStrategiesforGameandPrintOut(tab, k, m, n):
    rows = len(tab)
    cols = len(tab[0])
    # calculate the value of the game - v = 1/V - k
    # where v is the value of the game,
    # V is the value in the bottom right corner of the tableau
    # and k is the constant we defined when normalizing the matrix
    v = tab[rows-1][cols-1]
    value = fractions.Fraction(1/v - k)
    # -------------------------------------------------------------
    print("Value of the game:", value)
    # calculate the optimal strategy for player 1
    # pj=yj/V,j = 1 ...,m where pj is a strategy
    # and yj takes the value at the bottom of the tableau
    # in the corresponding slack variable column j
    ply1opt = []
    for i in range(n, cols-1):
        ply1opt.append(fractions.Fraction((tab[rows-1][i])/v))
    # end="" used for formatting
    print("An Optimal Strategy for Player 1: (", end="")
    print(*ply1opt, sep=", ", end="")
    print(")")
    # calculate the optimal strategy for player 2
    # qi=xi/V, i = 1 ...,n where qi is a strategy
    # and xi takes the value on the far right of the tableau
    # in the corresponding row with 1 in the xi column
    # if the xi column does not have one 1 and the rest of it is 0s
    # then that corresponding qi is 0
    ply2opt = []
    for i in range(0, n):
        xcol = []
        for j in range(0, rows):
            xcol.append(tab[j][i])
        # this makes sure xi has one 1 and the rest of it is 0s
        if xcol.count(0) != rows - 1 or xcol.count(1) != 1:
            ply2opt.append(0)
        # this finds the far right value corresponding with xi's 1
        # and does the xi/V calculation
        else:
            farrightrowindex = xcol.index(1)
            farright = tab[farrightrowindex][cols-1]
            ply2opt.append(fractions.Fraction(farright/v))
    print("An Optimal Strategy for Player 2: (", end="")
    print(*ply2opt, sep=", ", end="")
    print(")")


if __name__ == '__main__':
    solved = False
    k, game = getMatrix()  # get matrix from user and k used to normalize it
    m = len(game)  # m is the number of rows in the original game
    n = len(game[0])  # n is the number of cols in the original game

    # create the first tableau
    tab = makeTableau(game, len(game), len(game[0]))

    cntr = 2
    while not solved:
        r, c, solved = findPivot(tab)
        if not solved:
            tab = calcNextTableau(tab, r, c, cntr)
            cntr += 1

    # now that the game has been solved, do the calculations
    print()  # make a new line before doing calculations
    calculateValueandOptimalStrategiesforGameandPrintOut(tab, k, m, n)
