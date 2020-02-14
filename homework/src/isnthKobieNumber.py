def isKobieNumber(n):
    lastDigit,nextDigit,digit = 0,0,0
    num = 0
    place = 0
    fiveCount = 0
    is112 = False
    nextToOne = False

    while(n > 0):

        digit = n % 10
        num += digit * 10 ** place
        n //= 10
        nextDigit = n % 10
        if (digit == 5):
            fiveCount += 1
            if nextDigit == 1 or lastDigit == 1:
                nextToOne = True
        if(n == 112 or num == 112):
            is112 = True
        lastDigit = digit

        place += 1
    return nextToOne and fiveCount == 1 and is112


def nthKobieNumber(n):
    guess = 0
    found = 0
    while found <= n:
        guess += 1
        if isKobieNumber(guess):
            found += 1
    return guess

print(nthKobieNumber(0))

