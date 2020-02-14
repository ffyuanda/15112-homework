#################################################
# 15-112-n19 hw2-3-sudoku
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *
import math
import copy


####################################
# Helper functions are here
def getAvailableCells(data):
    #########################
    # This function is used find out the
    # cells in the board which are available
    # for the user's input(i.e. not occupied by the
    # initial values
    #########################

    availableCells = []
    for row in range(data.rows):
        for col in range(data.cols):
            if data.originalBoard[row][col] == "":
                availableCells.append((row, col))
    return availableCells


def almostEqual(d1, d2, epsilon=10 ** -7):
    return (abs(d2 - d1) < epsilon)


def areLegalValues(values):
    #####################
    # Helper function from the hw2-2
    ######################
    length = len(values)
    intLength = int(math.sqrt(length))
    floatLength = math.sqrt(length)
    if (length == 0): return False
    if (not almostEqual(intLength, floatLength)): return False

    numRange = list(range(0, length + 1))

    for i in values:
        if (values.count(i) > 1 and i != 0):
            return False
        elif (numRange.count(i) < 1):
            return False

    return True


def isLegalRow(board, row):
    #####################
    # Helper function from the hw2-2
    ######################
    rowContainer = []
    rowContainer = board[row]
    return areLegalValues(rowContainer)


def isLegalCol(board, col):
    #####################
    # Helper function from the hw2-2
    ######################
    colContainer = []

    for i in board:
        colContainer.append(i[col])

    return areLegalValues(colContainer)


def isLegalBlock(board, block):
    #####################
    # Helper function from the hw2-2
    ######################
    blockContainer = []
    length = len(board)
    colRow = math.sqrt(length)  # the length of the side of the block
    colRow = int(colRow)

    topLeftX = block // colRow * colRow  # calculate each block's coordinators
    topLeftY = block % colRow * colRow
    bottomRightX = topLeftX + colRow - 1
    bottomRightY = topLeftY + colRow - 1

    for i in range(topLeftX, bottomRightX + 1):  # get the block into a list

        for j in range(topLeftY, bottomRightY + 1):
            blockContainer.append(board[i][j])

    return areLegalValues(blockContainer)


def drawGrids(canvas, data):
    #####################
    # This function would wrapped in the drawSudokuBoard function
    # which is used to draw board and texts from the data value.
    # This function is adapted from the hw2-2
    ######################
    availableCells = getAvailableCells(data)
    for row in range(data.rows):  # draw large grids
        for col in range(data.cols):
            # calculate each block's coordinators
            x0 = col * data.cellWidth + data.margin
            x1 = (col + 1) * data.cellWidth + data.margin
            y0 = row * data.cellHeight + data.margin
            y1 = (row + 1) * data.cellHeight + data.margin
            element = data.board[row][col]

            # draw the initial elements
            if(element != "" and (row,col) not in availableCells):
                canvas.create_rectangle(x0, y0, x1, y1, fill="grey", width= 1
                                        )
                canvas.create_text((x1 + x0) // 2,
                                   (y1 + y0) // 2,
                                   text=data.board[row][col],
                                   fill="black",
                                   font="Times 15")

            # draw the modified elements
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="white", width = 1
                                        )
                canvas.create_text((x1 + x0) // 2,
                                   (y1 + y0) // 2,
                                   text=data.board[row][col],
                                   fill="black",
                                   font="Times 15")


def starterBoard():

    #####################
    # initialize a board for the
    # Sudoku game
    #####################
    return [
  [ "", "", "", 4, 5, 6, 7, 8, 9],
  [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
  [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
  [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
  [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
  [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
  [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
  [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
  [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
]


# Adapted from 15-112 course note
def getCellBounds(row, col, data):
    ##################
    # Help to convert the row and col variables
    # into the actual pixels' positions on the
    # board in the canvas.
    ####################
    x0 = data.margin + col * data.cellWidth
    x1 = data.margin + (col + 1) * data.cellWidth
    y0 = data.margin + row * data.cellHeight
    y1 = data.margin + (row + 1) * data.cellHeight
    return (x0, y0, x1, y1)


# Adapted from 15-112 course note
def pointInGrid(x, y, data):
    ##################
    # Check if the clicking point
    # is in the area of the game board
    ##################
    return ((data.margin <= x <= data.width - data.margin) and
            (data.margin <= y <= data.height - data.margin))


# Adapted from 15-112 course note
def getCell(x, y, data):
    ###################
    # Get the row and col according to the
    # clicking point and return the value
    # get to the row and col in data values.
    ####################
    if not pointInGrid(x, y, data):
        return data.selection

    row = (y - data.margin) // data.cellHeight
    col = (x - data.margin) // data.cellWidth

    return (row, col)


###################################
# Add your hw2-1 and hw2-2 functions here!
# You may need to modify them a bit.
# Those are: isLegalSudoku and
# drawSudokuBoard
# ###################################

def isLegalSudoku(board):
    ###################
    # A combination of the three functions
    # before in order to find out if the whole
    # board is in an legal order.
    ####################
    for i in range(len(board)):
        if (isLegalRow(board, i) == False): return False
        if (isLegalCol(board, i) == False): return False
        if (isLegalBlock(board, i) == False): return False

    return True


def drawSudokuBoard(canvas, data):
    ###################
    # Wrapper of the drawGrids function.
    ##################
    drawGrids(canvas, data)


####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.board = starterBoard()
    # used to record the unchanged board in order to
    # return the unoccupied cells' positions at first
    data.originalBoard = copy.deepcopy(starterBoard())
    data.selection = (1, 1)
    data.width = 500
    data.height = 500
    data.margin = 6
    data.rows = len(data.board)
    data.cols = len(data.board[0])
    data.cellWidth = (data.width - 2 * data.margin) / data.cols
    data.cellHeight = (data.height - 2 * data.margin) / data.rows

    pass


def mousePressed(event, data):
    # use event.x and event.y
    # trying to modify the data.selection according
    # to mousePressed

    ######################################
    # Check if the state of the Sudoku board
    # is legal,if it is legal, return congratulations and
    # stop all the action in from the keyboard and mouse.
    ######################################
    if (not isLegalSudoku(data.board)):
        (row, col) = getCell(event.x, event.y, data)
        data.selection = (row, col)


def keyPressed(event, data):
    # use event.char and event.keysym
    # check Sudoku state

    ######################################
    # Check if the state of the Sudoku board
    # is legal,if it is legal, return congratulations and
    # stop all the action in from the keyboard and mouse.
    ######################################
    if(not isLegalSudoku(data.board)):
        row = int(data.selection[0])
        col = int(data.selection[1])


        if event.keysym == "Up":# When user click the "Up" key
            data.selection = (data.selection[0] - 1, data.selection[1])
        elif event.keysym == "Down":# When user click the "Down" key
            data.selection = (data.selection[0] + 1, data.selection[1])
        elif event.keysym == "Left":# When user click the "Left" key
            data.selection = (data.selection[0], data.selection[1] - 1)
        elif event.keysym == "Right":# When user click the "Right" key
            data.selection = (data.selection[0], data.selection[1] + 1)

        if(data.selection[1] < 0): # left side wall
            data.selection = (data.selection[0], data.cols - 1)
        elif (data.selection[1] > data.cols - 1): # right side wall
            data.selection = (data.selection[0], 0)
        elif (data.selection[0] < 0): # up side wall
            data.selection = (data.rows - 1, data.selection[1])
        elif (data.selection[0] > data.rows - 1): # down side wall
            data.selection = (0, data.selection[1])

        if(data.originalBoard[row][col] == ""): #cannot change initial values
            if(event.char == "0" or event.char == "1" or
            event.char == "2"# cell input
            or event.char == "3" or event.char == "4"or event.char == "5"
            or event.char == "6"or event.char == "7" or event.char == "8"
            or event.char == "9"):
                input = event.char
                data.board[row][col] = int(input)

            if(event.keysym == "BackSpace"):# clear the cell
                data.board[row][col] = ""


    pass


def redrawAll(canvas, data):
    # draw in canvas
    drawSudokuBoard(canvas, data)
    # Adapted from 15-112 course note
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            if (data.selection == (row, col)):
                canvas.create_rectangle(x0, y0, x1, y1, fill="cyan")
                canvas.create_text((x1 + x0) // 2,
                                   (y1 + y0) // 2,
                                   text=data.board[row][col],
                                   fill="black",
                                   font="Times 15")
    if (isLegalSudoku(data.board)):
        ######################################
        # Check if the state of the Sudoku board
        # is legal,if it is legal, return congratulations and
        # stop all the action in from the keyboard and mouse.
        ######################################
        canvas.create_text(data.width / 2, data.height / 2,
                           text = "Congratulations",
                           fill = "red",
                           font = "Times 45 bold")
    pass


####################################
# use the run function as-is
####################################

def runSudoku(width=500, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

runSudoku(1000, 1000)
