#################################################
# 15-112-n19 hw4-2
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################
import math, random


###################
# helper functions
def flattenHelper(lst, output=[]):
    for item in lst:
        if type(item) == list:
            flattenHelper(item, output)

        else:
            output.append(item)

    return output


def getCourseHelper(courseCatalog, courseNumber, name=[]):
    for item in courseCatalog:
        if type(item) == list:
            name.append(courseCatalog[0])
            name.append(".")
            solution = getCourseHelper(item, courseNumber, name)
            if solution == None:
                name.pop()
                name.pop()
                continue
            return solution
        if item == courseNumber:
            name.append(courseCatalog[0])
            name.append(".")
            name.append(item)
            return name
        if item != courseCatalog[0] and \
                item == courseCatalog[len(courseCatalog) - 1]:
            return None


# taken from hw 2-2
def almostEqual(d1, d2, epsilon=10 ** -7):
    return (abs(d2 - d1) < epsilon)


# taken from hw 2-2
def areLegalValues(values):
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


# taken from hw 2-2
def isLegalRow(board, row):
    rowContainer = []
    rowContainer = board[row]
    return areLegalValues(rowContainer)


# taken from hw 2-2
def isLegalCol(board, col):
    colContainer = []

    for i in board:
        colContainer.append(i[col])

    return areLegalValues(colContainer)


# taken from hw 2-2
def isLegalBlock(board, block):
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


# taken from hw 2-2
def isLegalSudoku(board):
    for i in range(len(board)):
        if (isLegalRow(board, i) == False): return False
        if (isLegalCol(board, i) == False): return False
        if (isLegalBlock(board, i) == False): return False

    return True


#######################


def flatten(lst):
    return flattenHelper(lst, [])


def getCourse(courseCatalog, courseNumber):
    name = getCourseHelper(courseCatalog, courseNumber, [])
    output = ""
    if name == None:
        return None
    for item in name:
        output += item

    return output


def solveSudoku(board, row=0, col=0):
    length = len(board)
    if row == length:
        return board  # base case
    else:  # recursion case
        if col < length and row < length and board[row][col] == 0:
            # the same row and the slot is 0
            for num in range(1, length + 1):
                board[row][col] = num
                if isLegalSudoku(board):
                    solution = solveSudoku(board, row, col + 1)
                    if solution != None: return solution
                if num == length:
                    board[row][col] = 0
                    return None
        elif col < length and row < length and board[row][col] != 0:
            # the same row but the slot is not 0 (skip it)
            return solveSudoku(board, row, col + 1)
        if col >= length:
            # next row
            return solveSudoku(board, row + 1, col=0)


# ignore_rest
# test functions
def testflatten():
    print('Testing flatten()...', end='\n')
    assert (flatten([1, [2]]) == [1, 2])
    assert (flatten([1, 2, [3, [4, 5], 6], 7]) == [1, 2, 3, 4, 5, 6, 7])
    assert (flatten(['wow', [2, [[]]], [True]]) == ['wow', 2, True])
    assert (flatten([]) == [])
    assert (flatten([[]]) == [])


def testgetCourse():
    print('Testing getCourse()...', end='\n')
    courseCatalog = \
        ["CMU",
         ["CIT",
          ["ECE", "18-100", "18-202", "18-213"],
          ["BME", "42-101", "42-201"],
          ],
         ["SCS",
          ["CS",
           ["Intro", "15-110", "15-112"],
           "15-122", "15-150", "15-213"
           ],
          ],
         "99-307", "99-308"
         ]
    assert (getCourse(courseCatalog, "18-100") == "CMU.CIT.ECE.18-100")
    assert (getCourse(courseCatalog, "15-112") == "CMU.SCS.CS.Intro.15-112")
    assert (getCourse(courseCatalog, "15-213") == "CMU.SCS.CS.15-213")
    assert (getCourse(courseCatalog, "99-307") == "CMU.99-307")
    assert (getCourse(courseCatalog, "15-251") == None)


def testSolveSudoku():
    print('Testing solveSudoku()...', end='\n')
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    solved = solveSudoku(board)
    solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    assert (solved == solution)
    print('Passed!')


#############
# OOPy animation
from tkinter import *


# Helper function for drawing the Rocket

def createAsteroids(data):
    # wrapped in the timerFired function to create asteroids
    element = None
    cx = random.randint(0, data.width)
    cy = random.randint(0, data.height)
    r = random.randint(20, 40)
    v = random.randint(5, 20)
    direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    asteroid = random.randint(0, 2)
    if asteroid == 0:  # create Asteroid
        element = Asteroid(cx, cy, r, v, direction)
        return element
    elif asteroid == 1:  # create ShrinkingAsteroid
        element = ShrinkingAsteroid(cx, cy, r, v, direction)
        return element
    elif asteroid == 2:  # create SplittingAsteroid
        element = SplittingAsteroid(cx, cy, r, v, direction)
        return element


class Asteroid(object):
    def __init__(self, cx, cy, r, v, direction=(0, 1), color="purple"):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.v = v
        self.direction = direction
        self.color = color
        self.hitted = False

    def __str__(self):

        return "%s at (%d, %d) with radius=%d and direction (%d, %d)" % \
               (type(self).__name__, self.cx, self.cy, self.r,
                self.direction[0],
                self.direction[1])

    def __repr__(self):
        return "Asteroid at (%d, %d) with radius=" \
               "%d and direction (%d, %d)" % \
               (self.cx, self.cy, self.r, self.direction[0],
                self.direction[1])

    def setDirection(self, coor):
        self.direction = coor[0], coor[1]

    def getDirection(self):
        return (self.direction[0], self.direction[1])

    def isCollisionWithWall(self, width, height):
        if self.cx - self.r > 0 and self.cx + self.r < width \
                and self.cy - self.r > 0 and self.cy + self.r < height:
            return False
        else:
            return True

    def moveAsteroid(self):
        self.cx += self.direction[0] * self.v
        self.cy += self.direction[1] * self.v

    def getPositionAndRadius(self):
        return self.cx, self.cy, self.r

    def reactToBulletHit(self, asteroid, data):
        self.direction = 0, 0

    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                           self.cx + self.r, self.cy + self.r,
                           fill=self.color)

    def getToEdge(self, data):
        # wrap around
        self.cx = self.cx % data.width
        self.cy = self.cy % data.height

    def onTimerFired(self, asteroid, data):
        if type(asteroid) == Asteroid and \
                data.count % 100 == 0 \
                and asteroid.direction == (0, 0):
            data.asteroids.remove(asteroid)


class ShrinkingAsteroid(Asteroid):
    def __init__(self, cx, cy, r, v, direction=(0, 1),
                 shrinkAmount=5, color="pink"):
        super().__init__(cx, cy, r, v, direction=(0, 1))
        self.shrinkAmount = shrinkAmount
        self.color = color
        self.direction = direction

    def reactToBulletHit(self, asteroid, data):
        self.r -= self.shrinkAmount

    def bounce(self):
        self.direction = -self.direction[0], -self.direction[1]

    def getToEdge(self, data):
        # bounce back
        self.direction = (-self.direction[0], -self.direction[1])

    def onTimerFired(self, asteroid, data):
        if type(asteroid) == ShrinkingAsteroid and asteroid.r <= 15:
            data.asteroids.remove(asteroid)


class SplittingAsteroid(Asteroid):
    def __init__(self, cx, cy, r, v, direction=(0, 1), color="blue"):
        super().__init__(cx, cy, r, v, direction=(0, 1))
        self.color = color
        self.direction = direction

    def reactToBulletHit(self, asteroid, data):
        smallestRadius = 3
        if self.r > smallestRadius:
            asteroid1 = SplittingAsteroid(self.cx - self.r, self.cy - self.r,
                                          self.r // 2, self.v, self.direction)
            asteroid2 = SplittingAsteroid(self.cx + self.r, self.cy + self.r,
                                          self.r // 2, self.v, self.direction)

            if type(asteroid) == SplittingAsteroid:
                data.asteroids.append(asteroid1)
                data.asteroids.append(asteroid2)
                data.asteroids.remove(asteroid)

    def onTimerFired(self, asteroid, data):
        # for asteroid in data.asteroids:
        pass


def drawTriangle(canvas, cx, cy, angle, size, fill="black"):
    angleChange = 2 * math.pi / 3
    p1x, p1y = (cx + size * math.cos(angle),
                cy - size * math.sin(angle))
    p2x, p2y = (cx + size * math.cos(angle + angleChange),
                cy - size * math.sin(angle + angleChange))
    p3x, p3y = (cx, cy)
    p4x, p4y = (cx + size * math.cos(angle + 2 * angleChange),
                cy - size * math.sin(angle + 2 * angleChange))

    canvas.create_polygon((p1x, p1y), (p2x, p2y), (p3x, p3y), (p4x, p4y),
                          fill=fill)


# Read this class carefully! You'll need to call the methods!
class Rocket(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.angle = 90

    def rotate(self, numDegrees):
        self.angle += numDegrees

    def makeBullet(self):
        offset = 10
        dx, dy = (offset * math.cos(math.radians(self.angle)),
                  offset * math.sin(math.radians(self.angle)))
        speedLow, speedHigh = 20, 40

        return Bullet(self.cx + dx, self.cy - dy,
                      self.angle, random.randint(speedLow, speedHigh))

    def draw(self, canvas):
        size = 30
        drawTriangle(canvas, self.cx, self.cy,
                     math.radians(self.angle), size, fill="green2")


# Read this class carefully! You'll need to call the methods!
class Bullet(object):
    def __init__(self, cx, cy, angle, speed=20):
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed

    def moveBullet(self):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.cx, self.cy = self.cx + dx, self.cy - dy

    def isCollisionWithAsteroid(self, other):
        # in this case, other must be an asteroid
        if (not isinstance(other, Asteroid)):
            return False
        else:
            return (math.sqrt((other.cx - self.cx) ** 2 +
                              (other.cy - self.cy) ** 2)
                    < self.r + other.r)

    def draw(self, canvas):
        cx, cy, r = self.cx, self.cy, self.r
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                           fill="white", outline=None)

    def onTimerFired(self, data):
        self.moveBullet()


# animations
# Basic Animation Framework

from tkinter import *


####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.asteroids = []
    data.bullets = []
    data.count = 0
    data.rocket = Rocket(data.width // 2, data.height // 2)
    data.numDegrees = 0
    pass


def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(event, data):
    # use event.char and event.keysym

    if event.keysym == "Left":
        data.rocket.rotate(5)
    elif event.keysym == "Right":
        data.rocket.rotate(-5)
    elif event.keysym == "space":
        data.bullets.append(data.rocket.makeBullet())
    pass


def timerFired(data):
    data.count += 1  # counter
    if data.count % 20 == 0:  # every 2s create an asteroid
        data.asteroids.append(createAsteroids(data))


    for bullet in data.bullets:
        # loop through bullets
        bullet.moveBullet()
        for asteroid in data.asteroids:
            # loop through asteroids
            if bullet.isCollisionWithAsteroid(asteroid):
                asteroid.reactToBulletHit(asteroid, data)

    for asteroid in data.asteroids:
        asteroid.moveAsteroid()
        asteroid.onTimerFired(asteroid, data)
        # wrap around / bounce back
        if asteroid.cx < 0 or asteroid.cx > data.width or \
                asteroid.cy < 0 or asteroid.cy > data.height:
            asteroid.getToEdge(data)


def redrawAll(canvas, data):
    # draw in canvas
    data.rocket.draw(canvas)
    for bullet in data.bullets:
        bullet.draw(canvas)
    if len(data.asteroids) > 0:
        for asteroid in data.asteroids:
            asteroid.draw(canvas)
    pass


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
    data.timerDelay = 100  # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


def testAll():
    testflatten()
    testgetCourse()
    testSolveSudoku()
    run(600, 600)


def main():
    testAll()


if __name__ == '__main__':
    main()
