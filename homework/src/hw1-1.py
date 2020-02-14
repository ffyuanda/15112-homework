#################################################
# 15-112-n19 hw1-1
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################

import math


#################################################
# Helper functions
#################################################

# From lecture, do not change this function
def almostEqual(d1, d2, epsilon=10 ** -7):
    return (abs(d2 - d1) < epsilon)


#################################################
# hw1-1 problems
#################################################

# Edit these functions so they return the correct values.

def distance(x1, y1, x2, y2):
    length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return length


def isRightTriangle(x1, y1, x2, y2, x3, y3):
    a = distance(x1, y1, x2, y2)
    b = distance(x1, y1, x3, y3)
    c = distance(x2, y2, x3, y3)
    if (a > b and a > c):
        if (almostEqual(a ** 2, b ** 2 + c ** 2)):
            return True
    if (b > a and b > c):
        if (almostEqual(b ** 2, a ** 2 + c ** 2)):
            return True
    if (c > b and c > a):
        if (almostEqual(c ** 2, b ** 2 + a ** 2)):
            return True
    else:
        return False

    return False


def getKthDigit(n, k):
    if (n < 0):
        n = abs(n)

    output = 0

    divider = 10 ** (k + 1)

    output = n % divider

    output //= 10 ** k

    return output


def isPerfectSquare(n):
    if (type(n) == str):
        return False
    if (n < 0):
        return False

    if (type(n) != int and type(n) != float):
        print("check")
        return False

    compare = (int)(math.sqrt(n))

    if (math.sqrt(n) == compare):
        return True

    return False


print(isPerfectSquare(17))


#################################################
# hw1-1 Test Functions
################################################

def testDistance():
    print('Testing distance()...', end='')
    assert (almostEqual(distance(3.0, 0.0, 0.0, 4.0), 5.0))
    assert (almostEqual(distance(-1.0, 2.0, 3.0, 2.0), 4.0))
    assert (almostEqual(distance(-5, 5, 5, -5), 14.142135623730951))
    assert (almostEqual(distance(100.5, 50.2, 100.5, 50.2), 0.0))
    assert (almostEqual(distance(1000, 1000, -1000, -1000), 2828.42712474619))
    print('Passed.')


def testIsRightTriangle():
    print('Testing isRightTriangle()... ', end='')
    assert (isRightTriangle(0, 0, 0, 3, 4, 0) == True)
    assert (isRightTriangle(1, 1.3, 1.4, 1, 1, 1) == True)
    assert (isRightTriangle(9, 9.12, 8.95, 9, 9, 9) == True)
    assert (isRightTriangle(0, 0, 0, math.pi, math.e, 0) == True)
    assert (isRightTriangle(0, 0, 1, 1, 2, 0) == True)
    assert (isRightTriangle(0, 0, 1, 2, 2, 0) == False)
    assert (isRightTriangle(1, 0, 0, 3, 4, 0) == False)
    print('Passed.')


def testGetKthDigit():
    print('Testing getKthDigit()... ', end='')
    assert (getKthDigit(809, 0) == 9)
    assert (getKthDigit(809, 1) == 0)
    assert (getKthDigit(809, 2) == 8)
    assert (getKthDigit(809, 3) == 0)
    assert (getKthDigit(0, 100) == 0)
    assert (getKthDigit(-809, 0) == 9)
    print('Passed.')


def testIsPerfectSquare():
    print('Testing isPerfectSquare()... ', end='')
    assert (isPerfectSquare(0) == True)
    assert (isPerfectSquare(1) == True)
    assert (isPerfectSquare(16) == True)
    assert (isPerfectSquare(1234 ** 2) == True)
    assert (isPerfectSquare(15) == False)
    assert (isPerfectSquare(17) == False)
    assert (isPerfectSquare(-16) == False)
    assert (isPerfectSquare(1234 ** 2 + 1) == False)
    assert (isPerfectSquare(1234 ** 2 - 1) == False)
    assert (isPerfectSquare(4.0000001) == False)
    assert (isPerfectSquare('Do not crash here!') == False)
    print('Passed.')


#################################################
# hw1-1 Main
################################################

def testAll():
    testDistance()
    testIsRightTriangle()
    testGetKthDigit()
    testIsPerfectSquare()


def main():
    testAll()


if __name__ == '__main__':
    main()
