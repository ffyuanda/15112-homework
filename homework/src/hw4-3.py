#################################################
# 15-112-n19 hw4-3
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################



def findRTPWrapper(digits, num, place=0):
    if digits < 1: return None
    if place >= digits:
        return num
    else:
        for digit in range(1, 10):
            num = modNthDigit(num, place, digit)
            if isPrime(nthDigitNum(num, place)):
                result = findRTPWrapper(digits, num, place + 1)
                if result != None: return result
                continue
            if digit == 9: return None


def findRTP(digits):
    return (findRTPWrapper(digits, 10 ** (digits - 1)))


def nthDigitNum(num, n):
    numS = str(num)

    digit = numS[0:n + 1]
    return int(digit)


def modNthDigit(num, n, target):
    numS = str(num)
    numS = numS[0:n] + str(target) + numS[n + 1:]
    return int(numS)


def isPrime(n):
    if (n < 2):
        return False
    for factor in range(2, n):
        if (n % factor == 0):
            return False
    return True


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line(object):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.color = "black"
        self.width = 2

    def draw(self, canvas):
        canvas.create_line(self.point1.x, self.point1.y,
                           self.point2.x, self.point2.y,
                           fill=self.color,
                           width=self.width)


class Gate(object):
    def __init__(self, x=0, y=0):
        self.inputGates = []
        self.outputGates = []
        self.inputValues = []
        self.outputValue = None
        self.maxInputGates = 0

        ##### For tkinter#######
        self.IOLength = 6
        self.x = x
        self.y = y
        self.inputColor = "green"
        self.outputColor = "red"
        self.IOWidth = 0.2
        self.pinx = self.x
        self.piny = self.y

        pass

    def getInputGates(self):
        return self.inputGates

    def getOutputGates(self):
        return self.outputGates

    def connectTo(self, other):
        if type(other) == Output:
            if len(other.inputGates) > 0:
                return
        self.outputGates.append(other)
        if other.getMaxInputGates() >= len(other.inputGates):
            other.inputGates.append(self)
            other.inputValues.append((self, self.outputValue))

    def getMaxInputGates(self):
        return self.maxInputGates

    def setInputValue(self, fromGate, value):
        pass

    #####For tkinter######
    def draw(self, canvas):
        pass

    def distance(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        pass

    def clickOnPins(self, event, data):
        pass


class Input(Gate):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

        self.maxInputGates = 0
        self.ovalR = 8

        self.pinx = self.x + self.ovalR + self.IOLength
        self.piny = self.y
        self.points = 0
        self.power = False


    def setInputValue(self, fromGate, value):

        for item in self.outputGates:
            if len(self.inputValues) == 0:
                self.inputValues.append((fromGate, value))
            else:
                self.inputValues[0] = (self.inputValues[0][0], value)
            self.outputValue = value
            item.setInputValue(self, self.outputValue)

        pass

    def draw(self, canvas):
        adjust = 1

        canvas.create_oval(self.x - self.ovalR, self.y - self.ovalR,
                           self.x + self.ovalR, self.y + self.ovalR,
                           fill=self.outputColor, width=0)
        canvas.create_oval(self.x - self.ovalR + adjust, self.y - self.ovalR + adjust,
                           self.x + self.ovalR - adjust, self.y + self.ovalR - adjust,
                           fill="black")
        canvas.create_line(self.x + self.ovalR, self.y,
                           self.x + self.ovalR + self.IOLength,
                           self.y, fill=self.outputColor, width=self.IOWidth)

    def clickOnPins(self, event, data):

        if (self.distance(event.x, event.y, self.pinx, self.piny) <
                0.5 * self.IOLength):

            if type(self) == Input and len(data.points) == 0 and self.points == 0:
                print("YES")
                data.points.append(Point(self.pinx, self.piny))
                self.points += 1
                data.fromGateIndex = data.gates.index(self)
        self.powerControl(event,data)

    def powerControl(self,event,data):
        if (self.distance(event.x, event.y, self.x, self.y) <
                self.ovalR):
            self.power = not self.power

            self.setInputValue(None,self.power)

            pass




class Output(Gate):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.maxInputGates = 1
        self.ovalR = 8
        self.pinx = self.x - self.ovalR - self.IOLength
        self.piny = self.y
        self.points = 0

    def setInputValue(self, fromGate, value):
        for i in range(len(self.inputValues)):
            if self.inputValues[i][0] == fromGate:
                self.inputValues[i] = (self.inputValues[i][0], value)
                self.outputValue = value

    def draw(self, canvas):
        adjust = 1
        canvas.create_oval(self.x - self.ovalR, self.y - self.ovalR,
                           self.x + self.ovalR, self.y + self.ovalR,
                           fill="green", width=0)
        canvas.create_oval(self.x - self.ovalR + adjust, self.y - self.ovalR + adjust,
                           self.x + self.ovalR - adjust, self.y + self.ovalR - adjust,
                           fill="black")
        canvas.create_line(self.x - self.ovalR, self.y,
                           self.x - self.ovalR - self.IOLength,
                           self.y, fill=self.outputColor, width=self.IOWidth)
        pass

    def clickOnPins(self, event, data):
        if (self.distance(event.x, event.y, self.pinx, self.piny) <
                self.IOLength):

            if type(self) == Output and len(data.points) == 1 and self.points == 0:
                print("YES")
                data.points.append(Point(self.pinx, self.piny))
                self.points += 1
                data.toGateIndex = data.gates.index(self)


class Not(Gate):

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.maxInputGates = 1

        self.x = x
        self.y = y
        self.b1x = self.x  # bottom-left vertex
        self.b1y = self.y - 2 * self.IOLength
        self.b2x = self.x  # bottom-right vertex
        self.b2y = self.y + 2 * self.IOLength
        self.b3x = self.x + 3.5 * self.IOLength  # top vertex
        self.b3y = self.y
        self.IOCircleR = 1.5

        self.pinInx = self.x - self.IOLength
        self.pinIny = self.y
        self.pinOutx = self.b3x + self.IOLength
        self.pinOuty = self.b3y
        self.points = 0
        self.outPoints = 0

    def setInputValue(self, fromGate, value):
        for i in range(len(self.inputValues)):

            if self.inputValues[i][0] == fromGate:
                self.inputValues[i] = (self.inputValues[i][0], value)
                self.outputValue = not value

        for i in range(len(self.outputGates)):
            self.outputGates[i].setInputValue(self, self.outputValue)
        pass

    def draw(self, canvas):
        canvas.create_line(self.x - self.IOLength, self.y,
                           self.x, self.y,
                           fill=self.inputColor,
                           width=self.IOWidth)
        canvas.create_polygon(self.b1x, self.b1y,
                              self.b2x, self.b2y,
                              self.b3x, self.b3y,
                              fill=self.outputColor, )
        canvas.create_oval(self.b3x, self.b3y - self.IOCircleR,
                           self.b3x + 2 * self.IOCircleR,
                           self.b3y + self.IOCircleR, fill="white")
        canvas.create_line(self.b3x, self.b3y,
                           self.b3x + self.IOLength, self.b3y,
                           fill=self.inputColor,
                           width=self.IOWidth)

    def clickOnPins(self, event, data):
        if (self.distance(event.x, event.y, self.pinInx, self.pinIny) <
                self.IOLength):
            if type(self) == Not and len(data.points) == 1 and self.points == 0:
                print("YES")
                data.points.append(Point(self.pinInx, self.pinIny))
                self.points += 1
                data.toGateIndex = data.gates.index(self)
        elif (self.distance(event.x, event.y, self.pinOutx, self.pinOuty) <
              self.IOLength):
            if type(self) == Not and len(data.points) == 0 and self.outPoints == 0:
                print("YES")
                data.points.append(Point(self.pinOutx, self.pinOuty))
                self.outPoints += 1
                data.fromGateIndex = data.gates.index(self)

    pass


class And(Gate):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.maxInputGates = 2

        self.b1x = self.x  # bottom-left vertex
        self.b1y = self.y - self.IOLength
        self.b2x = self.x  # bottom-right vertex
        self.b2y = self.y + self.IOLength
        self.b3x = self.x
        self.b3y = self.b2y + self.IOLength
        self.b4x = self.x + 3 * self.IOLength
        self.b4y = self.b3y
        self.b5x = self.b4x + 2 * self.IOLength
        self.b5y = self.y
        self.b6x = self.b4x
        self.b6y = self.b1y - self.IOLength
        self.b7x = self.x
        self.b7y = self.b1y - self.IOLength

        self.pinIn1x = self.x - self.IOLength
        self.pinIn1y = self.y - self.IOLength
        self.pinIn2x = self.x - self.IOLength
        self.pinIn2y = self.y + self.IOLength
        self.pinOutx = self.b5x + self.IOLength
        self.pinOuty = self.b5y
        self.points = 0
        self.outPoints = 0

    def setInputValue(self, fromGate, value):
        for i in range(len(self.inputValues)):
            # make sure that the gate value is the one we want to change
            # which comes from the outer recursion
            if self.inputValues[i][0] == fromGate:
                self.inputValues[i] = (self.inputValues[i][0], value)

                # circuit output rules
                if self.inputValues[0][1] == None or self.inputValues[1][1] == None:
                    self.outputValue = None

                elif self.inputValues[0][1] and self.inputValues[1][1]:
                    self.outputValue = True

                else:
                    self.outputValue = False

        for i in range(len(self.outputGates)):
            self.outputGates[i].setInputValue(self, self.outputValue)

        pass

    def draw(self, canvas):
        canvas.create_line(self.pinIn1x, self.pinIn1y,
                           self.x, self.y - self.IOLength,
                           fill=self.inputColor,
                           width=self.IOWidth)
        canvas.create_line(self.pinIn2x, self.pinIn2y,
                           self.x, self.y + self.IOLength,
                           fill=self.inputColor,
                           width=self.IOWidth)
        canvas.create_polygon(self.b7x, self.b7y, self.b6x, self.b6y,
                              self.b5x, self.b5y, self.b4x, self.b4y,
                              self.b3x, self.b3y, fill=self.outputColor)

        canvas.create_line(self.b5x, self.b5y, self.pinOutx,
                           self.pinOuty, fill=self.inputColor,
                           width=self.IOWidth)

    def clickOnPins(self, event, data):
        if (self.distance(event.x, event.y, self.pinIn1x, self.pinIn1y) <
                self.IOLength):
            if type(self) == And and len(data.points) == 1 and self.points < 2:
                print("YES")
                data.points.append(Point(self.pinIn1x, self.pinIn1y))
                self.points += 1
                data.toGateIndex = data.gates.index(self)
        elif (self.distance(event.x, event.y, self.pinIn2x, self.pinIn2y) <
              self.IOLength):
            if type(self) == And and len(data.points) == 1 and self.points < 2:
                print("YES")
                data.points.append(Point(self.pinIn2x, self.pinIn2y))
                self.points += 1
                data.fromGateIndex = data.gates.index(self)
        elif (self.distance(event.x, event.y, self.pinOutx, self.pinOuty) <
              self.IOLength):
            if type(self) == And and len(data.points) == 0  and self.outPoints == 0:
                print("YES")
                data.points.append(Point(self.pinOutx, self.pinOuty))
                self.outPoints += 1
                data.fromGateIndex = data.gates.index(self)


class Or(Gate):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.maxInputGates = 2

        ##### For tkinter######
        self.b1x = self.x
        self.b1y = self.y - self.IOLength
        self.b2x = self.x
        self.b2y = self.y + self.IOLength
        self.b3x = self.x - 0.5 * self.IOLength
        self.b3y = self.b2y + self.IOLength
        self.b4x = self.b3x
        self.b4y = self.b1y - self.IOLength
        self.b5x = self.x + self.IOLength
        self.b5y = self.b4y
        self.b6x = self.b5x
        self.b6y = self.b3y
        self.b7x = self.x + 4 * self.IOLength
        self.b7y = self.y

        self.pinIn1x = self.x - self.IOLength
        self.pinIn1y = self.y - self.IOLength
        self.pinIn2x = self.x - self.IOLength
        self.pinIn2y = self.y + self.IOLength
        self.pinOutx = self.b7x + self.IOLength
        self.pinOuty = self.b7y
        self.points = 0
        self.outPoints = 0

    def draw(self, canvas):
        canvas.create_line(self.x - self.IOLength, self.y - self.IOLength,
                           self.x, self.y - self.IOLength,
                           fill=self.inputColor,
                           width=self.IOWidth)
        canvas.create_line(self.x - self.IOLength, self.y + self.IOLength,
                           self.x, self.y + self.IOLength,
                           fill=self.inputColor,
                           width=self.IOWidth)
        canvas.create_polygon(self.b1x, self.b1y, self.b4x, self.b4y,
                              self.b5x, self.b5y, self.b7x, self.b7y,
                              self.b6x, self.b6y, self.b3x, self.b3y,
                              self.b2x, self.b2y, fill=self.outputColor)
        canvas.create_line(self.b7x, self.b7y, self.b7x + self.IOLength,
                           self.b7y, fill=self.inputColor,
                           width=self.IOWidth)

    def setInputValue(self, fromGate, value):
        for i in range(len(self.inputValues)):
            # make sure that the gate value is the one we want to change
            # which comes from the outer recursion
            if self.inputValues[i][0] == fromGate:
                self.inputValues[i] = (self.inputValues[i][0], value)
                # circuit output rules
                if self.inputValues[0][1] or self.inputValues[1][1]:
                    self.outputValue = True
                elif self.inputValues[0][1] == None or self.inputValues[1][1] == None:
                    self.outputValue = None
                else:
                    self.outputValue = False

        for i in range(len(self.outputGates)):
            self.outputGates[i].setInputValue(self, self.outputValue)

            pass

    def clickOnPins(self, event, data):
        if (self.distance(event.x, event.y, self.pinIn1x, self.pinIn1y) <
                self.IOLength):
            if type(self) == Or and len(data.points) == 1 and self.points < 2:
                print("YES")
                data.points.append(Point(self.pinIn1x, self.pinIn1y))
                self.points += 1
                data.toGateIndex = data.gates.index(self)
        elif (self.distance(event.x, event.y, self.pinIn2x, self.pinIn2y) <
              self.IOLength):
            if type(self) == Or and len(data.points) == 1 and self.points < 2:
                print("YES")
                data.points.append(Point(self.pinIn2x, self.pinIn2y))
                self.points += 1
                data.fromGateIndex = data.gates.index(self)
        elif (self.distance(event.x, event.y, self.pinOutx, self.pinOuty) <
              self.IOLength):
            if type(self) == Or and len(data.points) == 0 and self.outPoints == 0:
                print("YES")
                data.points.append(Point(self.pinOutx, self.pinOuty))
                self.outPoints += 1
                data.fromGateIndex = data.gates.index(self)


def twoPointConnection(data):
    if len(data.points) == 2:
        print(data.points)
        data.lines.append(Line(data.points[0], data.points[1]))
        data.gates[data.fromGateIndex].connectTo(data.gates[data.toGateIndex])
        data.points = []



def addGates(event, data):
    if data.currGate == "Not" and event.x > data.menu.gridWidth:
        currGate = Not(event.x, event.y)
        data.gates.append(currGate)
        data.currGate = None

    elif data.currGate == "Or" and event.x > data.menu.gridWidth:
        currGate = Or(event.x, event.y)
        data.gates.append(currGate)
        data.currGate = None

    elif data.currGate == "And" and event.x > data.menu.gridWidth:
        currGate = And(event.x, event.y)
        data.gates.append(currGate)
        data.currGate = None
    elif data.currGate == "Input" and event.x > data.menu.gridWidth:
        currGate = Input(event.x, event.y)
        data.gates.append(currGate)
        data.currGate = None
    elif data.currGate == "Output" and event.x > data.menu.gridWidth:
        currGate = Output(event.x, event.y)
        data.gates.append(currGate)
        data.currGate = None



# ignore_rest
####################################
# customize these functions
####################################
from tkinter import *

def init(data):
    # load data.xyz as appropriate
    data.points = []
    data.lines = []
    data.gates = []
    data.currGate = None
    data.fromGateIndex = 0
    data.toGateIndex = 0
    data.menu = Menu(data)

class Menu(object):

    def __init__(self, data):
        self.gridHeight = data.height // 5
        self.gridWidth = data.width // 8

    def getCellBounds(self, n):
        return (0, n * self.gridHeight,
                self.gridWidth, (n + 1) * self.gridHeight)

    def getGateBounds(self, n):
        adjust = 10
        return ((self.getCellBounds(n)[0] +
                 self.getCellBounds(n)[2]) // 2 - adjust,
                (self.getCellBounds(n)[1] +
                 self.getCellBounds(n)[3]) // 2)

    def drawGates(self, n, canvas):
        adjust = 8
        if n == 0:  # Not

            instance = Not(self.getGateBounds(n)[0], self.getGateBounds(n)[1])
            instance.draw(canvas)
            canvas.create_text(self.gridWidth // 2,
                               (self.gridHeight) * (n + 1) - adjust,
                               text="NotGate", font="Times 10")
        elif n == 1:  # Or
            instance = Or(self.getGateBounds(n)[0], self.getGateBounds(n)[1])
            instance.draw(canvas)
            canvas.create_text(self.gridWidth // 2,
                               (self.gridHeight) * (n + 1) - adjust,
                               text="OrGate", font="Times 10")
        elif n == 2:  # And
            instance = And(self.getGateBounds(n)[0], self.getGateBounds(n)[1])
            instance.draw(canvas)
            canvas.create_text(self.gridWidth // 2,
                               (self.gridHeight) * (n + 1) - adjust,
                               text="AndGate", font="Times 10")
        elif n == 3:  # Input
            instance = Input(self.getGateBounds(n)[0], self.getGateBounds(n)[1])
            instance.draw(canvas)
            canvas.create_text(self.gridWidth // 2,
                               (self.gridHeight) * (n + 1) - adjust,
                               text="Input", font="Times 10")
        elif n == 4:  # Output
            instance = Output(self.getGateBounds(n)[0], self.getGateBounds(n)[1])
            instance.draw(canvas)
            canvas.create_text(self.gridWidth // 2,
                               (self.gridHeight) * (n + 1) - adjust,
                               text="Output", font="Times 10")

    def draw(self, canvas):
        for n in range(5):
            canvas.create_rectangle(self.getCellBounds(n), fill="white",
                                    width="1")
            self.drawGates(n, canvas)

    def choose(self, event, data):
        if event.x < self.gridWidth:
            if event.y < self.gridHeight * 1:
                data.currGate = "Not"
            elif event.y > self.gridHeight * 1 and \
                    event.y < self.gridHeight * 2:

                data.currGate = "Or"
            elif event.y > self.gridHeight * 2 and \
                    event.y < self.gridHeight * 3:
                data.currGate = "And"
            elif event.y > self.gridHeight * 3 and \
                    event.y < self.gridHeight * 4:
                data.currGate = "Input"
            elif event.y > self.gridHeight * 4 and \
                    event.y < self.gridHeight * 5:
                data.currGate = "Output"

def mousePressed(event, data):
    # use event.x and event.y
    data.menu.choose(event, data)
    # twoPointConnection(event, data)
    for gate in data.gates:
        gate.clickOnPins(event, data)

        twoPointConnection(data)

    addGates(event, data)


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "space":
        for item in data.gates:

            print(item.outputGates)
    pass


def timerFired(data):
    pass


def redrawAll(canvas, data):
    # draw in canvas
    for line in data.lines:
        line.draw(canvas)
    for gate in data.gates:
        gate.draw(canvas)
    data.menu.draw(canvas)

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


# test functions


def testGateClass0_basics():
    gate1 = Gate()
    gate2 = Gate()
    assert (gate1.getInputGates() == [])
    assert (gate1.getOutputGates() == [])

    assert (gate1.inputValues == [])
    assert (gate1.outputValue == None)

    # you can connect gates to each other!
    gate1.connectTo(gate2)
    assert (gate1.getOutputGates() == [gate2])
    assert (gate2.getInputGates() == [gate1])

    # gate2 now has gate1 as an input, but since gate1.outputValue = None,
    # gate2.inputValues == [(gate1,None)]
    assert (gate2.inputValues == [(gate1, None)])


def testGateClass1_inputToOutput():
    # Connect an input gate to an output gate
    in1 = Input()
    out1 = Output()
    in1.connectTo(out1)

    assert (in1.getInputGates() == [])
    assert (in1.getMaxInputGates() == 0)  # an input gate can't have any inputs
    assert (in1.getOutputGates() == [out1])
    assert (out1.getInputGates() == [in1])
    assert (out1.getMaxInputGates() == 1)
    assert (out1.getOutputGates() == [])

    assert (in1.inputValues == [])
    assert (in1.outputValue == None)
    assert (out1.inputValues == [(in1, None)])
    assert (out1.outputValue == None)

    in2 = Input()
    in2.connectTo(out1)
    # since out1 has a maximum of one input, and it already has in1 as an input,
    # this shouldn't do anything!
    assert (in2.getOutputGates() == [])
    assert (out1.getInputGates() == [in1])

    # setInputValue should take in two values - a fromGate and a value, which
    # represent the gate the input is coming from, and the value of that gate.
    # Here, in1 is an input gate, meaning that it's input isn't coming from
    # anywhere! So, the fromGate = None, and the value = True in this case.

    # be careful to examine the test cases to figure out what happens to the
    # gates you're connected to once you set the input value!
    in1.setInputValue(None, True)

    assert (in1.inputValues == [(None, True)])
    assert (in1.outputValue == True)
    assert (out1.inputValues == [(in1, True)])
    assert (out1.outputValue == True)
    # and set the input to False
    in1.setInputValue(None, False)
    assert (in1.inputValues == [(None, False)])
    assert (in1.outputValue == False)
    assert (out1.inputValues == [(in1, False)])
    assert (out1.outputValue == False)


def testGateClass2_oneNotGate():
    in1 = Input()
    out1 = Output()
    not1 = Not()
    in1.connectTo(not1)
    not1.connectTo(out1)

    assert (in1.outputValue == not1.outputValue == out1.outputValue == None)

    in1.setInputValue(None, False)
    assert (not1.inputValues == [(in1, False)])
    assert (out1.inputValues == [(not1, True)])
    assert (out1.outputValue == True)

    in1.setInputValue(None, True)
    assert (not1.inputValues == [(in1, True)])
    assert (out1.inputValues == [(not1, False)])
    assert (out1.outputValue == False)


def testGateClass3_oneAndGate():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    and1 = And()
    in1.connectTo(and1)
    in2.connectTo(and1)
    and1.connectTo(out1)

    assert (out1.outputValue == None)
    in1.setInputValue(None, False)
    assert (and1.inputValues == [(in1, False), (in2, None)])
    assert (and1.outputValue == None)  # not ready, need both inputs
    in2.setInputValue(None, False)
    assert (and1.inputValues == [(in1, False), (in2, False)])
    assert (and1.outputValue == False)
    assert (out1.outputValue == False)

    in1.setInputValue(None, True)
    assert (and1.inputValues == [(in1, True), (in2, False)])
    assert (out1.outputValue == False)

    in2.setInputValue(None, True)
    assert (and1.inputValues == [(in1, True), (in2, True)])
    assert (out1.outputValue == True)


def testGateClass4_oneOrGate():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    or1 = Or()
    in1.connectTo(or1)
    in2.connectTo(or1)
    or1.connectTo(out1)

    assert (or1.inputValues == [(in1, None), (in2, None)])
    assert (or1.outputValue == None)
    assert (out1.outputValue == None)
    in1.setInputValue(None, False)
    assert (or1.inputValues == [(in1, False), (in2, None)])
    assert (or1.outputValue == None)  # not ready, need both inputs
    in2.setInputValue(None, False)
    assert (or1.inputValues == [(in1, False), (in2, False)])
    assert (or1.outputValue == False)
    assert (out1.outputValue == False)

    in1.setInputValue(None, True)
    assert (or1.inputValues == [(in1, True), (in2, False)])
    assert (out1.outputValue == True)

    in2.setInputValue(None, True)
    assert (or1.inputValues == [(in1, True), (in2, True)])
    assert (out1.outputValue == True)


def testGateClass5_xor():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    and1 = And()
    and2 = And()
    not1 = Not()
    not2 = Not()
    or1 = Or()
    in1.connectTo(and1)
    in1.connectTo(not1)
    in2.connectTo(and2)
    in2.connectTo(not2)
    not1.connectTo(and2)
    not2.connectTo(and1)
    and1.connectTo(or1)
    and2.connectTo(or1)
    or1.connectTo(out1)

    in1.setInputValue(None, False)
    in2.setInputValue(None, False)
    assert (out1.outputValue == False)

    in1.setInputValue(None, True)
    in2.setInputValue(None, False)
    assert (out1.outputValue == True)

    in1.setInputValue(None, False)
    in2.setInputValue(None, True)
    assert (out1.outputValue == True)

    in1.setInputValue(None, True)
    in2.setInputValue(None, True)
    assert (out1.outputValue == False)


def testGateClass():
    print("Testing Gate class... ", end="")
    testGateClass0_basics()
    testGateClass1_inputToOutput()
    testGateClass2_oneNotGate()
    testGateClass3_oneAndGate()
    testGateClass4_oneOrGate()
    testGateClass5_xor()
    print("Passed!")


def testfindRTP():
    print('Testing findRTP()...', end="")
    assert (findRTP(8) == 23399339)
    assert (findRTP(1) == 2)
    assert (findRTP(0) == None)
    assert (findRTP(3) == 233)
    print("Passed!")


def testAll():
    testfindRTP()
    testGateClass()
    run(800, 600)


def main():
    testAll()


if __name__ == '__main__':
    main()
