#################################################
# 15-112-n19 hw2-2
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################
from builtins import print

import math

#################################################
# Helper functions
#################################################
def drawTriangle(canvas, outerPoints, innerPoints, color):
    length = len(innerPoints)
    innerPoints.insert(0, innerPoints[len(innerPoints) - 1])
    innerPoints.pop()
    for i in range(length):
        if(i == length - 1):
            canvas.create_polygon(outerPoints[i], innerPoints[i],
                                  innerPoints[0], fill=color)
        else:
            canvas.create_polygon(outerPoints[i],innerPoints[i],
                                  innerPoints[i + 1], fill = color )
def drawCircle(canvas, centerX, centerY, diameter, color):

    canvas.create_oval(centerX - diameter // 2,
                       centerY - diameter // 2,
                       centerX + diameter // 2,
                       centerY + diameter // 2, fill=color)

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def isLegalMove(board, currValue):

    nextValue = currValue + 1
    for i in range(0, len(board)):
        if(0 in board[i]): return False #stands for 0 situation
        if(currValue in board[i]):startPoint = (i, board[i].index(currValue))
        if(nextValue in board[i]):nextPoint = (i, board[i].index(nextValue))
    #a template that contains all of the element arount current point
    blockTemplate = [(startPoint[0] - 1, startPoint[1] - 1),
    (startPoint[0] - 1, startPoint[1]),
    (startPoint[0] - 1, startPoint[1] + 1),(startPoint[0], startPoint[1] - 1),
    (startPoint[0], startPoint[1] + 1),(startPoint[0] + 1, startPoint[1] - 1),
    (startPoint[0] + 1, startPoint[1]),(startPoint[0] + 1, startPoint[1] + 1)]

    for i in blockTemplate:
        if(nextPoint == i):
            return True

    return False
def blockReader(board, block):

    blockContainer = []
    length = len(board)
    colRow = math.sqrt(length)#the length of the side of the block
    colRow = int(colRow)

    topLeftX = block // colRow *colRow#calculate each block's coordinators
    topLeftY = block % colRow * colRow
    bottomRightX = topLeftX + colRow - 1
    bottomRightY = topLeftY + colRow - 1

    for i in range(topLeftX, bottomRightX + 1):#get the block into a list

        for j in range(topLeftY, bottomRightY + 1):

            blockContainer.append(board[i][j])

    return (blockContainer)
def drawTexts(canvas,smallX1, smallY1, smallX0, smallY0, board, times):

    length = len(board)
    rowCol = int(math.sqrt(length))
    texts = []
    for i in range(length):
        texts.extend(blockReader(board, i))

    canvas.create_text((smallX1 + smallX0) // 2,
                       (smallY1 + smallY0) // 2,
                       text=texts[times],
                       fill="black",
                       font="Helvetica 10")

def drawGrids(canvas, board, margin, canvasSize):
    length = len(board)
    colRow = int(math.sqrt(length))
    width = (canvasSize - margin * 2) // colRow
    times = 0
    for i in range(colRow):#draw large grids
        for j in range(colRow):
            x0 = j * width + margin #calculate each block's coordinators
            y0 = i *  width + margin
            x1 = x0 + width
            y1 = y0 + width
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=11)

            for m in range(colRow):#draw small grids
                for n in range(colRow):
                    widthSmall = (width - 10) // colRow
                    smallX0 = x0 + n * widthSmall + 6
                    smallY0 = y0 + m * widthSmall + 6
                    smallX1 = smallX0 + widthSmall
                    smallY1 = smallY0 + widthSmall
                    canvas.create_rectangle(smallX0, smallY0, smallX1,
                                            smallY1, fill="white", width=1)
                    drawTexts(canvas,smallX1, smallY1, smallX0,
                              smallY0, board, times)
                    times += 1
######################################################################
# hw2-2 problems
######################################################################

def areLegalValues(values):
    length = len(values)
    intLength = int(math.sqrt(length))
    floatLength = math.sqrt(length)
    if(length == 0): return False
    if(not almostEqual(intLength, floatLength)): return False

    numRange = list(range(0, length + 1))

    for i in values:
        if(values.count(i) > 1 and i != 0):
            return False
        elif(numRange.count(i) < 1):
            return False

    return True

def isLegalRow(board, row):

    rowContainer = []
    rowContainer = board[row]
    return areLegalValues(rowContainer)

def isLegalCol(board, col):

    colContainer = []

    for i in board:
        colContainer.append(i[col])

    return areLegalValues(colContainer)

def isLegalBlock(board, block):

    blockContainer = []
    length = len(board)
    colRow = math.sqrt(length)#the length of the side of the block
    colRow = int(colRow)

    topLeftX = block // colRow *colRow#calculate each block's coordinators
    topLeftY = block % colRow * colRow
    bottomRightX = topLeftX + colRow - 1
    bottomRightY = topLeftY + colRow - 1

    for i in range(topLeftX, bottomRightX + 1):#get the block into a list

        for j in range(topLeftY, bottomRightY + 1):

            blockContainer.append(board[i][j])

    return areLegalValues(blockContainer)

def isLegalSudoku(board):

    for i in range(len(board)):
        if(isLegalRow(board, i) == False): return False
        if(isLegalCol(board, i) == False): return False
        if(isLegalBlock(board,i) == False): return False

    return True

def isKingsTour(board):

    length = len(board)
    largest = length ** 2
    for i in board:
        for j in range(1, largest):
            if( i.count(j) > 1): return False#stands for repeated value

    for i in range(1, largest):
        if(isLegalMove(board, i) == False): return False

    return True

def makeWordSearch(wordList, replaceEmpties):
    return 42

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *

def drawSudokuBoard(canvas, board, margin, canvasSize):

    drawGrids(canvas, board, margin, canvasSize)

def drawStar(canvas, centerX, centerY, diameter, numPoints, color):
    radius = diameter // 2
    innerDiameter = diameter * 3 / 8
    innerRadius = innerDiameter // 2
    innerPoints = []
    outerPoints = []

    # drawCircle(canvas, centerX, centerY, diameter, color)

    drawCircle(canvas, centerX, centerY, innerDiameter, color)

    for points in range(numPoints):
        pointAngle =  math.pi / 2 - (2 * math.pi) * (points/numPoints)
        ndPointAngle = math.pi / 2 - (2 * math.pi) * ((points + 1)/numPoints)
        innerAngle = (pointAngle + ndPointAngle) / 2
        innerAngleX = centerX + innerRadius * math.cos(innerAngle)
        innerAngleY = centerY - innerRadius * math.sin(innerAngle)
        angleX = centerX + radius * math.cos(pointAngle)
        angleY = centerY - radius * math.sin(pointAngle)
        outerPoints.append((angleX, angleY))
        innerPoints.append((innerAngleX, innerAngleY))

        # canvas.create_text(angleX,angleY,text = "A", font = "Arial 16 bold")
        # canvas.create_text(innerAngleX, innerAngleY, text="A", font="Arial 16 bold")
    drawTriangle(canvas, outerPoints, innerPoints, color)

#################################################################
# hw2-2 tests
# Note: You must look at the output of these and confirm
# they work visually.
# Remember that you need to write your own test cases for the isLegalSudoku
# functions, as well as Kings Tour!
# You are not required to write tests for any helper functions
# you write for graphics problems
#################################################################

# add test functions here!

def testareLegalValues():
    print("Testing isKingsTour()...", end ="")
    assert (areLegalValues([1,2,3,4,5,6,7,8,9]) == True)
    assert (areLegalValues([1,1,3,4,5,6,7,8,9]) == False)
    assert (areLegalValues([0,1,2,3,4,5,6,7,8,9]) == False)
    assert (areLegalValues([0, 0, 0, 0, 4, 5, 6, 7, 8]) == True)
    print('Passed!')

def testisLegalSudoku():
    print("Testing isKingsTour()...", end ="")

    assert (isLegalSudoku([
        [1,2,3,4],
        [3,4,5,6],
        [7,8,9,10],
        [11,12,13,14]
    ]) == False)

    assert (isLegalSudoku([
  [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
  [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
  [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
  [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
  [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
  [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
  [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
  [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
  [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
]) == True)
    assert (isLegalSudoku([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 5, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]) == False)
    assert (isLegalSudoku([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [5, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]) == False)
    assert (isLegalSudoku([
        [5, 3, 0, 0, 5, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]) == False)

    print('Passed!')

def testisKingsTour():
    print("Testing isKingsTour()...", end ="")
    assert (isKingsTour([[  3, 2, 1 ],
                            [  6, 4, 0 ],
                            [  5, 7, 8 ]]) == False)
    assert (isKingsTour([[  1, 2, 3 ],
                            [  7, 4, 8 ],
                            [  6, 5, 9 ]]) == False)
    assert (isKingsTour([[3, 2, 1],
                            [6, 4, 9],
                            [5, 7, 8]]) == True)
    assert (isKingsTour(  [ [  1, 14, 15, 16],
                              [ 13,  2,  7,  6],
                              [ 12,  8,  3,  5],
                              [ 11, 10,  9,  4]]) == True)
    print('Passed!')

def runDrawStar(centerX, centerY, diameter, numPoints, color,
                   winWidth=500, winHeight=500):
    root = Tk()
    canvas = Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()

    drawStar(canvas, centerX, centerY, diameter, numPoints, color)

    root.mainloop()

def testDrawStar():
    print("Testing drawStar()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    runDrawStar(250, 250, 500, 5, "gold")
    runDrawStar(300, 400, 100, 4, "blue")
    runDrawStar(300, 200, 300, 9, "red")
    print("Done!")

def getBoard0():
    return [
      [ 1, 2, 3, 4, 5, 6, 7, 8, 9],
      [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
      [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
      [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
      [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
      [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
      [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
      [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
      [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
    ]

def getBoard1():
    return [
        [1,2,3,4],
        [3,4,5,6],
        [7,8,9,10],
        [11,12,13,14]
    ]


def runSudoku(board, canvasSize=400):
    root = Tk()
    canvas = Canvas(root, width=canvasSize, height=canvasSize)
    canvas.pack()
    margin = 10
    drawSudokuBoard(canvas, board, margin, canvasSize)
    root.mainloop()

def testRunSudoku():
    print("Testing runSudoku()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    runSudoku(getBoard0(), 400)
    runSudoku(getBoard1(), 500)
    print("Done!")

def testAll():
    # remember to call the extra test functions you write here!
    # testDrawStar()
    # testRunSudoku()
    testisLegalSudoku()
    # also remember to test out the bonus problem if you attempt it

def main():
    testAll()


if __name__ == '__main__':
    main()