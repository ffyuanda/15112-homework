def isLegal(board, queenRow, queenCol):
    # A board is legal if no two queens can attack each other
    # We only need to check the most recently placed queen
    for row in range(len(board)):
        for col in range(len(board[0])):
            if queenRow == row and queenCol == col:
                continue
            elif board[row][col] == "Q":
                if ((queenRow == row) or
                    (queenCol == col) or
                    (queenRow + queenCol == row + col) or
                    (queenRow - queenCol == row - col)):
                    return False
    return True

def solve(board, row):
    if (row == len(board)):
        return board
    else:
        for col in range(len(board[row])):
            board[row][col] = "Q"
            if isLegal(board, row, col):
                solution = solve(board, row + 1)
                if (solution != None):
                    return solution
            board[row][col] = " "
        return None