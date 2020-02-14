import math

def powersOf3ToN(n):
    n = int(n)
    if n < 1:
        return None
    power = math.log(n, 3)

    if n > 1:
        if 3 ** power == 3 ** int(power):
            return powersOf3ToN(n - 1) + [n]
        else:
            return powersOf3ToN(n - 1)
    else:
        return [1]

def lengthOfNum(num):
    numS = str(num)
    length = len(numS)
    return length