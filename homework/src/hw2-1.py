#################################################
# 15-112-n19 hw2-1
# Your Name:
# Your Andrew ID:
# Your Section:
#################################################

import math
import string
import copy

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def moveOneStep(a, step):

    length = len(a)
    digit = a[0]
    temp = 0
    place = 0
    for i in range(0, length):


        if(step == 1):
            place = (i + 1) % length
            temp = a[place]
            a[place] = digit
            digit = temp

    return a

def getScore(letterScores, s):
    place = ord(s) - 97
    score = letterScores[place]
    return score

def existInHand(word, hand):

    handCopy = copy.copy(hand)
    for i in word:

        if(i in handCopy):
            handCopy.remove(i)
            continue

        else: return False
        handCopy = copy.copy(hand)

    return True

#################################################
# hw2-1 problems
#################################################

def lookAndSay(a):
    curr = 0 #current digit
    prev = 0 #previous digit
    resultList = []
    counter = 1

    for i in range(1, len(a)):

        curr = a[i]
        prev = a[i - 1]

        if(curr != prev):
            resultList.append((counter, prev))
            counter = 1

        elif(curr == prev):
            print(i)
            counter += 1
            prev = curr

        if(i == len(a) - 1): #for last digit situation
            resultList.append((counter, curr))
    return resultList

def inverseLookAndSay(a):
    resultList = []
    occurence = 0
    digit = 0
    for i in range(0, len(a)):#loop thorough the input

        occurence = a[i][0]
        digit = a[i][1]
        resultList += [digit] * occurence

    return resultList

def nondestructiveRotateList(a, n):

    length = len(a)
    resultList = [0] * length
    digit = 0
    place = 0

    for i in range(0, length):
        digit = a[i]
        place = (i + n) % length #calculate the place the digit should be in the newly created list
        resultList[place] = digit

    return resultList

def destructiveRotateList(a, n):

    length = len(a)
    digit = a[0]

    temp = 0
    baseIndex = 0
    currIndex = 0
    if(n > 0):
        for i in range(0, n):
            a = moveOneStep(a, 1)
    elif(n == 0):
        return a
    elif(n < 0):

        for i in range(0, length - abs(n)):
            a = moveOneStep(a, 1)

def bestScrabbleScore(dictionary, letterScores, hand):

    score = 0
    largest = 0
    output = []


    for word in dictionary:

        if(existInHand(word, hand)):

            for i in word:

                score += getScore(letterScores, i)

        if(score > largest):
            largest = score
            output = []
            output.append(word)

        elif(score == largest and largest != 0):

            output.append(word)

        score = 0


    if(len(output) == 1):
        return (output[0], largest)
    elif(len(output) == 0):
        return None

    return (output, largest)

def runSimpleProgram(program, args):
    return 42


#################################################
# hw2-1 test cases
# Note:
#   There are fewer test cases than usual below.
#   You'll want to add your own!
#################################################

def _verifyLookAndSayIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    lookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

# add more test cases here!
def testLookAndSay():
    print("Testing lookAndSay()...", end="")
    assert(_verifyLookAndSayIsNondestructive() == True)
    assert(lookAndSay([]) == [])
    assert(lookAndSay([1,1,1]) ==  [(3,1)])
    assert(lookAndSay([-1,2,7]) ==  [(1,-1),(1,2),(1,7)])
    assert(lookAndSay([3,3,8,-10,-10,-10]) == [(2,3),(1,8),(3,-10)])
    print("Passed!")

def _verifyInverseLookAndSayIsNondestructive():
    a = [(1,2), (2,3)]
    b = copy.copy(a)
    inverseLookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

# add more test cases here!
def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(_verifyInverseLookAndSayIsNondestructive() == True)
    assert(inverseLookAndSay([]) == [])
    assert(inverseLookAndSay([(3,1)]) == [1,1,1])
    inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10]
    print("Passed!")

def _verifynondestructiveRotateListIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    nondestructiveRotateList(a,1) # ignore result, just checking for destructiveness here
    return (a == b)

def testNondestructiveRotateList():
    print("Testing nondestructiveRotateList()...", end="")
    _verifynondestructiveRotateListIsNondestructive()
    assert(nondestructiveRotateList([1,2,3,4], 1) == [4,1,2,3])
    print("Passed!")

def testDestructiveRotateList():
    print("Testing destructiveRotateList()...", end="")

    # A single test case
    L = [1,2,3,4]
    r = destructiveRotateList(L,1)
    assert(r == None)
    assert(L == [4,1,2,3])

    print("Passed!")

# there are lots of test cases here :)
def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) == (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) == ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) == None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) == (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) == (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) == ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) == ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) == None)
    print("Passed!")

def testRunSimpleProgram():
    print("Testing runSimpleProgram()...", end="")
    largest = """! largest: Returns max(A0, A1)
                   L0 - A0 A1
                   JMP+ L0 a0
                   RTN A1
                   a0:
                   RTN A0"""
    assert(runSimpleProgram(largest, [5, 6]) ==  6)
    assert(runSimpleProgram(largest, [6, 5]) == 6)

    sumToN = """! SumToN: Returns 1 + ... + A0
                ! L0 is a counter, L1 is the result
                L0 0
                L1 0
                loop:
                L2 - L0 A0
                JMP0 L2 done
                L0 + L0 1
                L1 + L1 L0
                JMP loop
                done:
                RTN L1"""
    assert(runSimpleProgram(sumToN, [5]) ==  1+2+3+4+5)
    assert(runSimpleProgram(sumToN, [10]) == 10*11//2)
    print("Passed!")

#################################################
# hw2-1 Main
################################################

def testAll():
    testLookAndSay()
    testInverseLookAndSay()
    testNondestructiveRotateList()
    testDestructiveRotateList()
    testBestScrabbleScore()
    # testRunSimpleProgram() # uncomment this if you want to do the bonus!

def main():
    testAll()

if __name__ == '__main__':
    main()
