#################################################
# 15-112-n19 hw1-2
# Your Name:
# Your Andrew ID:
# Your Section:
#################################################

import math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

#################################################
# hw1-2 problems
#################################################

def countMultiplesOfSeven(x, y):

    count = 0
    for seven in range(x, y + 1):
        if(seven % 7 == 0):
            count += 1

    return count





def digitCounter(x):
    counter = 0
    while(x > 0):
        x = x // 10
        counter += 1

    return counter

def rotateNumber(x):

    firstDigit = x % 10
    remainder = x // 10



    output = firstDigit * 10 ** (digitCounter(x) - 1) + remainder
    return output

def isPrime(x):
    if(x < 2): return False
    for n in range(2, x):
        if(x % n == 0):

            return False
            break

    return True





def isCircularPrime(x):
    if(isPrime(x) == False): return False
    digitNumber = digitCounter(x)
    #print(digitNumber)
    curr = x
    while(digitNumber > 0):
        curr = rotateNumber(curr)

        if(isPrime(curr) == False):
            return False
        digitNumber -= 1

    return True

# print(isCircularPrime(173))

def nthCircularPrime(n):
    counter = -1
    x = 0
    while(counter < n):
        if(isCircularPrime(x)):
            #print("check1")
            counter += 1
            #print(counter)
        if(counter == n):
            #print("check2")
            return x
        x += 1
        #print(counter)
    return x



def carrylessAdd(x, y):
    xDigitNum = digitCounter(x)
    yDigitNum = digitCounter(y)
    totalDigitNum = max(xDigitNum,yDigitNum)
    output = 0
    place = 0
    #print(xDigitNum, yDigitNum)
    while(place < totalDigitNum):
        xCurr = x % 10
        yCurr = y % 10
        x //= 10
        y //= 10
        totalCurr = xCurr + yCurr
        totalCurr %= 10
        output += totalCurr * 10 ** place
        place += 1



    return output



#################################################
# hw1-2 Test Functions
################################################

def testCountMultiplesOfSeven():
    print('Testing countMultiplesOfSeven()... ', end='')
    assert(countMultiplesOfSeven(3, 16) == 2)
    assert(countMultiplesOfSeven(13, 15) == 1)
    assert(countMultiplesOfSeven(7, 22) == 3)
    assert(countMultiplesOfSeven(8, 28) == 3)
    assert(countMultiplesOfSeven(15, 18) == 0)
    assert(countMultiplesOfSeven(15, 6) == 0)
    print('Passed!')

def testRotateNumber():
    print('Testing rotateNumber()... ', end='')
    assert(rotateNumber(1234) == 4123)
    assert(rotateNumber(4123) == 3412)
    assert(rotateNumber(3412) == 2341)
    assert(rotateNumber(2341) == 1234)
    assert(rotateNumber(5) == 5)
    assert(rotateNumber(111) == 111)
    print('Passed!')

def testIsCircularPrime():
    print('Testing isCircularPrime()... ', end='')
    assert(isCircularPrime(2) == True)
    assert(isCircularPrime(11) == True)
    assert(isCircularPrime(13) == True)
    assert(isCircularPrime(79) == True)
    assert(isCircularPrime(197) == True)
    assert(isCircularPrime(1193) == True)
    assert(isCircularPrime(42) == False)
    print('Passed!')

def testNthCircularPrime():
    print('Testing nthCircularPrime()... ', end='')
    assert(nthCircularPrime(0) == 2)
    assert(nthCircularPrime(4) == 11)
    assert(nthCircularPrime(5) == 13)
    assert(nthCircularPrime(11) == 79)
    assert(nthCircularPrime(15) == 197)
    assert(nthCircularPrime(25) == 1193)
    print('Passed!')

def testCarrylessAdd():
    print('Testing carrylessAdd()... ', end='')
    assert(carrylessAdd(0, 0) == 0)
    assert(carrylessAdd(4, 5) == 9)
    assert(carrylessAdd(23, 57) == 70)
    assert(carrylessAdd(785, 376) == 51)
    assert(carrylessAdd(102, 108) == 200)
    assert(carrylessAdd(865, 23) == 888)
    print('Passed!')

#################################################
# hw1-2 Main
################################################

def testAll():
    testCountMultiplesOfSeven()
    testRotateNumber()
    testIsCircularPrime()
    testNthCircularPrime()
    testCarrylessAdd()

def main():
    testAll()

if __name__ == '__main__':
    main()