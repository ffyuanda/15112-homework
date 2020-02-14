#################################################
# 15-112-n19 hw-tetris
# Your Name:Shaoxuan Yuan
# Your Andrew ID:shaoxuan
# Your Section:B
# Collaborators: N/A (By myself)
#################################################
import random


#################################################
# Helper functions
def fallingPieceIsLegal(data):
    #######################
    # Check if the current coordinates and
    # positions for the falling piece is legal
    # according to the rule of Tetris:
    # 1. If it is still in the board
    # 2. If it is crashing into another block
    ###########################
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            # Target at the existing part of the Tetris block
            if (data.fallingPiece[row][col] == True):
                # check if the Tetris is in the board
                if (data.fallingPieceRow < 0 or
                        data.fallingPieceRow + data.fallingPieceRows >
                        data.rows or
                        data.fallingPieceCol < 0 or
                        data.fallingPieceCol + data.fallingPieceCols >
                        data.cols):
                    return False
                # check if the Tetris crash into another non-empty cell
                if (data.board[data.fallingPieceRow + row]
                [data.fallingPieceCol + col]
                        != data.emptyColor):
                    return False

    return True


def starterBoard(rows, cols):
    #######################
    # Return a starter board whose cells are
    # all blue (empty)
    ######################
    board = []
    for row in range(rows):
        board += [["blue"] * cols]
    return board


def drawCell(canvas, data, row, col):
    #########################
    # Draw a single cell according to
    # the data given
    ########################

    # calculate each block's coordinates
    x0 = col * data.cellWidth + data.margin
    x1 = (col + 1) * data.cellWidth + data.margin
    y0 = row * data.cellHeight + data.margin
    y1 = (row + 1) * data.cellHeight + data.margin
    element = data.board[row][col]

    canvas.create_rectangle(x0, y0, x1, y1, fill=element, width=1
                            )


def drawCellForTetris(canvas, data, row, col):
    ###########################
    # Draw the cell specifically for the Tetris
    # block cause the Tetris should be drawn over the
    # surface of the whole board
    ##########################
    x0 = col * data.cellWidth + data.margin
    x1 = (col + 1) * data.cellWidth + data.margin
    y0 = row * data.cellHeight + data.margin
    y1 = (row + 1) * data.cellHeight + data.margin
    color = data.fallingPieceColor

    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=1
                            )


def drawBackground(canvas, data):
    #######################
    # Draw the orange back ground
    # for the gaming board
    #######################
    x0 = 0
    x1 = data.width
    y0 = 0
    y1 = data.height
    backGroundColor = "orange"
    canvas.create_rectangle(x0, y0, x1, y1, fill=backGroundColor,
                            width=0)


def drawBoard(canvas, data):
    #######################
    # Wrapper function for the drawCell:
    # loop through the whole board and draw
    # each single cell by calling drawCell
    # function
    ########################3
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)


def newFallingPiece(data):
    ########################
    # Initialize a new falling piece of Tetris
    # according to the data given
    ##########################

    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)

    # get a random shape of the Tetris
    data.fallingPiece = data.tetrisPieces[randomIndex]
    # get a random color for the shape
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]

    # calculate the lines of columns and rows for the whole
    # piece of Tetris entity (including the False and True part)
    data.fallingPieceCols = len(data.fallingPiece[0])
    data.fallingPieceRows = len(data.fallingPiece)

    # initialize the Tetris at mid-top of the board (initial position)
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols // 2 - data.fallingPieceCols // 2
    if not fallingPieceIsLegal(data):
        data.isGameOver = True


def drawFallingPiece(canvas, data):
    ########################
    # Output the falling piece onto the canvas
    ###########################
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            if (data.fallingPiece[row][col] == True):
                if (fallingPieceIsLegal(data)):
                    # if the current falling piece's position
                    # is legal.
                    drawCellForTetris(canvas, data,
                                      row + data.fallingPieceRow,  # offset
                                      col + data.fallingPieceCol)
                    # store the current value into "last value", which
                    # is the last position of the Tetris block
                    # in order to roll back to the last version
                    data.oldRow = data.fallingPieceRow
                    data.oldCol = data.fallingPieceCol
                    data.oldPiece = data.fallingPiece
                else:
                    # if the current falling piece's position is
                    # illegal.
                    drawCellForTetris(canvas, data, row + data.oldRow,  # offset
                                      col + data.oldCol)
                    data.fallingPieceRow = data.oldRow
                    data.fallingPieceCol = data.oldCol
                    data.fallingPiece = data.oldPiece


def moveFallingPiece(data, drow, dcol):
    #####################
    # this function is used to
    # move the falling piece by given
    # the moving direction in row and
    # column.
    ###########################
    if (drow == 0 and dcol == -1):  # Left
        data.fallingPieceCol -= 1
    elif (drow == 0 and dcol == 1):  # Right
        data.fallingPieceCol += 1
    elif (drow == 1 and dcol == 0):  # Down
        data.fallingPieceRow += 1
        if not fallingPieceIsLegal(data):
            placeFallingPiece(data)
    elif (drow == -1 and dcol == 0):  # Down
        data.fallingPieceRow -= 1

    return False


def placeFallingPiece(data):
    #########################
    # This function is used to transfer
    # the data (color, row, col) stored in the
    # falling piece to the big board behind.
    ########################
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            if (data.fallingPiece[row][col] == True):
                data.board[row + data.oldRow] \
                    [col + data.oldCol] = data.fallingPieceColor

    newFallingPiece(data)
    # Try to remove a full row immediately
    # after place a falling piece.
    removeFullRows(data)
    pass


def rotateFallingPiece(data):
    # Store a chunk of old values for the restoration
    oldNumRows, oldNumCols = data.fallingPieceRows, data.fallingPieceCols
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    oldPiece = data.fallingPiece
    # flip the columns and rows
    newNumRows, newNumCols = oldNumCols, oldNumRows
    # newCenterRow should be the same with the old one
    oldCenterRow = data.fallingPieceRow + oldNumRows // 2
    newRow = oldCenterRow - newNumRows // 2
    # newCenterCol should be the same with the old one
    oldCenterCol = data.fallingPieceCol + oldNumCols // 2
    newCol = oldCenterCol - newNumCols // 2
    # modify the original row and col value
    data.fallingPieceRow, data.fallingPieceCol = newRow, newCol
    data.fallingPieceRows, data.fallingPieceCols = newNumRows, newNumCols
    data.fallingPiece = rotateValue(data.fallingPiece)
    if (not fallingPieceIsLegal(data)):  # check the legal state
        data.fallingPieceRow, data.fallingPieceCol = oldRow, oldCol
        data.fallingPieceRows, data.fallingPieceCols = oldNumRows, oldNumCols
        data.fallingPiece = oldPiece


def rotateValue(oldPiece):
    ###########################
    # return a new piece which rotated 90 degrees from the old one
    # and dump the data into a new-formed piece.
    ##########################
    oldNumRows = len(oldPiece)
    oldNumCols = len(oldPiece[0])
    newPiece = []
    for col in range(oldNumCols):
        carrier = []
        for row in range(oldNumRows):
            carrier.append(oldPiece[row][col])
        carrier.reverse()  # take the value in order
        newPiece.append(carrier)
    return newPiece


def removeFullRows(data):
    ########################
    # Remove a row which is full in the board
    # and add a new row to the top of the board
    # and and the score by 1.
    #########################
    length = len(data.board)
    for row in range(length):
        if data.emptyColor not in data.board[row]:
            data.board.pop(row)
            data.board.insert(0, [data.emptyColor] * length)
            data.score += 1
    pass


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *
import math


def init(data):
    # load data.xyz as appropriate
    data.started = False
    data.score = 0
    data.board = starterBoard(15, 10)
    data.emptyColor = "blue"
    data.width = 400
    data.height = 600
    data.margin = 25
    data.rows = 15
    data.cols = 10
    data.cellWidth = (data.width - 2 * data.margin) / data.cols
    data.cellHeight = (data.height - 2 * data.margin) / data.rows

    ###########################
    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [True, True, True, True]
    ]

    jPiece = [
        [True, False, False],
        [True, True, True]
    ]

    lPiece = [
        [False, False, True],
        [True, True, True]
    ]

    oPiece = [
        [True, True],
        [True, True]
    ]

    sPiece = [
        [False, True, True],
        [True, True, False]
    ]

    tPiece = [
        [False, True, False],
        [True, True, True]
    ]

    zPiece = [
        [True, True, False],
        [False, True, True]
    ]
    data.tetrisPieces = [iPiece, jPiece, lPiece,
                         oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink",
                              "cyan", "green", "orange"]
    data.fallingPiece = ""
    data.fallingPieceColor = ""

    data.fallingPieceRow = 0
    data.fallingPieceCol = 0

    data.fallingPieceCols = 0
    data.fallingPieceRows = 0

    data.oldRow = 0
    data.oldCol = 0
    data.oldPiece = None

    data.timer = 0
    data.isGameOver = False
    pass


def mousePressed(event, data):
    # use event.x and event.y
    # placeFallingPiece(data)
    if data.started == False:
        data.started = True
        newFallingPiece(data)
    pass


def keyPressed(event, data):
    # use event.char and event.keysym
    if (data.isGameOver == False):
        if (event.keysym == "Left"):
            moveFallingPiece(data, 0, -1)
        elif (event.keysym == "Right"):
            moveFallingPiece(data, 0, 1)
        elif (event.keysym == "Down"):
            moveFallingPiece(data, 1, 0)
        elif (event.keysym == "Up"):
            rotateFallingPiece(data)
    if event.keysym == "r":
        init(data)
    pass


def timerFired(data):
    pointThreeSeconds = 3
    if (data.isGameOver == False):
        data.timer += 1
        if data.timer % pointThreeSeconds == 0:
            moveFallingPiece(data, +1, 0)
    pass


def redrawAll(canvas, data):
    # draw in canvas
    if data.started == False:
        canvas.create_text(data.width // 2, data.height // 2,
                           text="Click to start",
                           fill="purple",
                           font="Times 30 bold")
    if data.started == True:
        drawBackground(canvas, data)
        drawBoard(canvas, data)
        if (data.isGameOver == False):
            drawFallingPiece(canvas, data)
            canvas.create_text(data.width // 2, 12,
                               text="Score: %d" % data.score, fill="red",
                               font="Times 20 bold")
        if data.isGameOver == True:  # game over
            canvas.create_rectangle(data.margin, data.height // 5,
                                    data.width - data.margin,
                                    data.height // 2.5,
                                    fill="black")
            canvas.create_text(data.width // 2,
                               (data.height // 5 + data.height // 2.5) // 2,
                               text="GAME OVER\nClick \"r\" to restart",
                               fill="gold",
                               font="Times 30 bold")


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
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
    timerFiredWrapper(canvas, data)
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


def playTetris(rows=15, cols=10):
    # use the rows and cols to compute the appropriate window size here!
    run()

playTetris()