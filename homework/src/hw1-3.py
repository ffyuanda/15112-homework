#################################################
# 15-112-n19 hw1-3
# Your Name:
# Your Andrew ID:
# Your Section:
#################################################

import string

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# hw1-3 problems
#################################################

#Edit these functions so they return the correct values.

#Helper functions:
def isPrime(x):
    if(x < 2): return False
    for n in range(2, x):
        if(x % n == 0):

            return False
            break

    return True

def digitCounter(x):
    counter = 0
    while(x > 0):
        x = x // 10
        counter += 1

    return counter

def getKthDigit(n, k):

    if(n < 0):
        n = abs(n)
    output = 0
    divider = 10 ** (k + 1)

    output = n % divider

    output //= 10 ** k

    return output

def numberReverser(n):
    output = 0
    digits = digitCounter(n)
    digits -= 1
    times = 0
    while(digits >= 0):
        output += getKthDigit(n, digits) * 10 ** times
        digits -= 1
        times += 1
    return output

def isEmirpsPrime(n):
    emirps = numberReverser(n)
    return isPrime(emirps)

def getKthCharInfinite(string, number):
    length = len(string)
    i = number % length
    return string[i - 1]


#End of help functions
def nthEmirpsPrime(n):
    found = -1
    guess = 0


    while(found < n):

        guess += 1
        reversed = numberReverser(guess)

        if(isPrime(guess) and isEmirpsPrime(guess) and digitCounter(guess) > 1 and guess !=  reversed):

            found += 1


    return guess



def areAnagrams(s1, s2):
    compare1 = s1.lower()
    compare2 = s2.lower()
    if(len(compare1) != len(compare2)):
        return False
    for x in compare1:
        if(compare1.count(x) != compare2.count(x)): return False

    return True



def longestCommonSubstring(s1, s2):
    longest = ""
    for i in range(0, len(s1)):

        for j in range(i + 1, len(s1) + 1):

            compare = s1[i:j]
            if(s2.count(compare) > 0 and len(compare) >= len(longest)):

                if(len(compare) == len(longest) and compare < longest):
                    longest = compare
                elif(len(compare) > len(longest)):
                    longest = compare
                #longest = compare
            #print(compare)
    return longest

def bestStudentAndAvg(gradebook):

    output = ""
    name = ""
    curr = 0
    largest = -99999999999
    times = 0

    for line in gradebook.splitlines():
       # print("check 1")
        if(line.startswith("#") or len(line) == 0): continue
        #print(line)
        #print(largest)

        for i in line.split(","):
           # print("check 2")

            if(i[0:1] == "-" and i[1:2].isdigit()):
                times += 1
                curr += int(i)

            if(i.isdigit()):
                times += 1 #count the quantity
                curr += int(i)

        curr /= times #average

        curr = roundHalfUp(curr) #round off

        times = 0 #reassign

        if(curr >= largest):

            largest = curr

            for i in line.split(","):

                if(i.isalpha()): name = i

            output = name + ":" + str(largest)

        curr = 0
    return output

def patternedMessage(message, pattern):
    messageMod = message.replace(" ","")
    length = len(messageMod)
    output = ""
    times = 0
    for i in pattern.splitlines():

        for j in i:
            if(j != " "):
                times += 1
                output += getKthCharInfinite(messageMod, times)
            elif(j == " "):
                output += " "#deal with the blank part

        output += "\n"
    return output.strip("\n")

def topLevelFunctionNames(code):
    return 42

#################################################
# hw1-3 Test Functions
################################################

def testNthEmirpsPrime():
    print('Testing nthEmirpsPrime()... ', end='')
    assert(nthEmirpsPrime(0) == 13)
    assert(nthEmirpsPrime(5) == 73)
    assert(nthEmirpsPrime(10) == 149)
    assert(nthEmirpsPrime(20) == 701)
    assert(nthEmirpsPrime(30) == 941)
    print('Passed.')

def testAreAnagrams():
    print("Testing areAnagrams()...", end="")
    assert(areAnagrams("", "") == True)
    assert(areAnagrams("abCdabCd", "abcdabcd") == True)
    assert(areAnagrams("abcdaBcD", "AAbbcddc") == True)
    assert(areAnagrams("abcdaabcd", "aabbcddcb") == False)
    assert(areAnagrams("abc", "abcc") == False)
    print("Passed!")

def testLongestCommonSubstring():
    print("Testing longestCommonSubstring()...", end="")
    assert(longestCommonSubstring("abcdef", "abqrcdest") == "cde")
    assert(longestCommonSubstring("abcdef", "ghi") == "")
    assert(longestCommonSubstring("", "abqrcdest") == "")
    assert(longestCommonSubstring("abcdef", "") == "")
    assert(longestCommonSubstring("abcABC", "zzabZZAB") == "AB")
    print("Passed!")

def testBestStudentAndAvg():
    print("Testing bestStudentAndAvg()...", end="")
    gradebook = """
# ignore  blank lines and lines starting  with  #'s
wilma,91,93
fred,80,85,90,95,100
betty,88
"""
    assert(bestStudentAndAvg(gradebook) ==  "wilma:92")
    gradebook   =   """
#   ignore  blank   lines   and lines   starting    with    #'s
wilma,93,95

fred,80,85,90,95,100
betty,88
"""
    assert(bestStudentAndAvg(gradebook) ==  "wilma:94")
    gradebook = "fred,0"
    assert(bestStudentAndAvg(gradebook) ==  "fred:0")
    gradebook = "fred,-1\nwilma,-2"
    assert(bestStudentAndAvg(gradebook) ==  "fred:-1")
    gradebook = "fred,100"
    assert(bestStudentAndAvg(gradebook) ==  "fred:100")
    gradebook = "fred,100,110"
    assert(bestStudentAndAvg(gradebook) ==  "fred:105")
    gradebook = "fred,49\nwilma" + ",50"*50
    assert(bestStudentAndAvg(gradebook) ==  "wilma:50")
    print("Passed!")

def testPatternedMessage():
    print("Testing patternedMessage()...", end="")

    #this set of test cases is easier to debug
    parms1 = [("A-C D?", """
*** *** ***
** ** ** **
"""),
    ("A", "x y z"),
    ("The pattern is empty!", "")
    ]
    solns1 = [
"""
A-C D?A -CD
?A -C D? A-
""",
"A A A",
""
    ]

    # this set of test cases is a bit more cumbersome, but more rigorous
    parms2 = [
    ("Go Pirates!!!", """
***************
******   ******
***************
"""),
    ("Three Diamonds!","""
  *     *     *
 ***   ***   ***
***** ***** *****
 ***   ***   ***
  *     *     *
"""),
    ("Go Steelers!","""
                          oooo$$$$$$$$$$$$oooo
                      oo$$$$$$$$$$$$$$$$$$$$$$$$o
                   oo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o         o$   $$ o$
   o $ oo        o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o       $$ $$ $$o$
oo $ $ '$      o$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$o       $$$o$$o$
'$$$$$$o$     o$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$o    $$$$$$$$
  $$$$$$$    $$$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$$$$$$$$$$$$$$
  $$$$$$$$$$$$$$$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$$$$$$  '$$$
   '$$$'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     '$$$
    $$$   o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     '$$$o
   o$$'   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$o
   $$$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' '$$$$$$ooooo$$$$o
  o$$$oooo$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   o$$$$$$$$$$$$$$$$$
  $$$$$$$$'$$$$   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     $$$$'
 ''''       $$$$    '$$$$$$$$$$$$$$$$$$$$$$$$$$$$'      o$$$
            '$$$o     '$$$$$$$$$$$$$$$$$$'$$'         $$$
              $$$o          '$$'$$$$$$'           o$$$
               $$$$o                                o$$$'
                '$$$$o      o$$$$$$o'$$$$o        o$$$$
                  '$$$$$oo     '$$$$o$$$$$o   o$$$$'
                     '$$$$$oooo  '$$$o$$$$$$$$$'
                        '$$$$$$$oo $$$$$$$$$$
                                '$$$$$$$$$$$
                                    $$$$$$$$$$$$
                                     $$$$$$$$$$'
                                      '$$$'
""")]
    solns2 = [
"""
GoPirates!!!GoP
irates   !!!GoP
irates!!!GoPira
"""
,
"""
  T     h     r
 eeD   iam   ond
s!Thr eeDia monds
 !Th   ree   Dia
  m     o     n
"""
,
"""
                          GoSteelers!GoSteeler
                      s!GoSteelers!GoSteelers!GoS
                   teelers!GoSteelers!GoSteelers!GoS         te   el er
   s ! Go        Steelers!GoSteelers!GoSteelers!GoSteel       er s! GoSt
ee l e rs      !GoSteeler    s!GoSteelers!    GoSteelers       !GoSteel
ers!GoSte     elers!GoSt      eelers!GoSt      eelers!GoSt    eelers!G
  oSteele    rs!GoSteele      rs!GoSteele      rs!GoSteelers!GoSteeler
  s!GoSteelers!GoSteelers    !GoSteelers!G    oSteelers!GoSt  eele
   rs!GoSteelers!GoSteelers!GoSteelers!GoSteelers!GoSteel     ers!
    GoS   teelers!GoSteelers!GoSteelers!GoSteelers!GoSteelers     !GoSt
   eele   rs!GoSteelers!GoSteelers!GoSteelers!GoSteelers!GoSt       eele
   rs!    GoSteelers!GoSteelers!GoSteelers!GoSteelers!Go Steelers!GoSteele
  rs!GoSteelers  !GoSteelers!GoSteelers!GoSteelers!GoS   teelers!GoSteelers
  !GoSteelers!G   oSteelers!GoSteelers!GoSteelers!Go     Steel
 ers!       GoSt    eelers!GoSteelers!GoSteelers!G      oSte
            elers     !GoSteelers!GoSteelers!         GoS
              teel          ers!GoSteel           ers!
               GoSte                                elers
                !GoSte      elers!GoSteele        rs!Go
                  Steelers     !GoSteelers!   GoStee
                     lers!GoSte  elers!GoSteeler
                        s!GoSteele rs!GoSteel
                                ers!GoSteele
                                    rs!GoSteeler
                                     s!GoSteeler
                                      s!GoS
"""
    ]

    # Test Cases 1
    # These test cases are easier to debug.
    for i in range(len(parms1)):
        msg,pattern = parms1[i]
        soln = solns1[i]
        soln = soln.strip("\n")
        observed = patternedMessage(msg, pattern)
        assert(observed == soln)

    # Test Cases 2
    # Uncomment the for loop below for more rigorous test cases.
    # They are a bit harder to debug.

    # for i in range(len(parms2)):
    #     msg,pattern = parms2[i]
    #     soln = solns2[i]
    #     soln = soln.strip("\n")
    #     observed = patternedMessage(msg, pattern)
    #     assert(observed == soln)
    print("Passed!")

def testTopLevelFunctionNames():
    print("Testing topLevelFunctionNames...", end = " ")
    # You should write your own test cases for this function!
    print("Passed!")

#################################################
# hw1-3 Main
################################################

def testAll():
    testAreAnagrams()
    testNthEmirpsPrime()
    testLongestCommonSubstring()
    testBestStudentAndAvg()
    testPatternedMessage()
    # testTopLevelFunctionNames()


def main():
    testAll()

if __name__ == '__main__':
    main()