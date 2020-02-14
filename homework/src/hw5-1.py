#################################################
# 15-112-n19 hw5-1
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################

"""
################################################################################
def slow1(lst): # N is the length of the list lst
    assert(len(lst) >= 2)
    a = lst.pop() #This is O(1)
    b = lst.pop(0) #This is O(N)
    lst.insert(0, a) #This is O(N)
    lst.append(b) #This is O(1)

A. It swaps the first and last element of the input list.

B. The resulting Big-O of the whole function is O(N).

C.
def fast1(lst):
    lst[0],lst[len(lst) - 1] = lst[len(lst) - 1],lst[0] #This is O(1)

D. The resulting Big-O of the improved function is O(1).



################################################################################
def slow2(lst): # N is the length of the list lst
    counter = 0 # This is O(1)
    for i in range(len(lst)):# This is O(n)
        if lst[i] not in lst[:i]:# This is O(end - start), which is O(n) in
                                 # the worst case.
            counter += 1 # This is O(1)
    return counter # This is O(1)

A. This function basically counts the number of the unique elements in the list.

B. The resulting Big-O of the whole function is O(n ** 2).

C.
def fast2(lst):
    s = set(lst) #This is O(1)
    return len(s) #This is O(1)

D. The resulting Big-O of the whole function is O(1).


################################################################################
import string
def slow3(s): # N is the length of the string s
    maxLetter = "" #This is O(1)
    maxCount = 0 #This is O(1)
    for c in s: #This is O(n)
        for letter in string.ascii_lowercase: #This is O(26)
            if c == letter: #This is O(1)
                if s.count(c) > maxCount or \
                   s.count(c) == maxCount and c < maxLetter: #This is O(N)
                    maxCount = s.count(c) #This is O(N)
                    maxLetter = c #This is O(1)
    return maxLetter #This is O(1)

A. This function basically find the lowercase
English letter which appears most frequently
and which should follow the alphabetical order.

B. The resulting Big-O of the whole function is O(n ** 2).

C.
def fast3(s):
    d = dict() #This is O(1)
    maxLetter = "" #This is O(1)
    maxCount = 0 #This is O(1)
    for i in range(len(s)): #This is O(N)
        if s[i] not in d: #This is O(1)
            d[s[i]] = 1 #This is O(1)
        else: #This is O(1)
            d[s[i]] += 1 #This is O(1)

    for key in d: #This is O(N)
        if d[key] > maxCount and key in string.ascii_lowercase: #This is O(26)
            maxCount = d[key] #This is O(1)
            maxLetter = key #This is O(1)
        if d[key] == maxCount and key < maxLetter and\
            key in string.ascii_lowercase: #This is O(26)
            maxLetter = key #This is O(1)

    return maxLetter #This is O(1)


D. The resulting Big-O of the whole function is O(n).

################################################################################
def slow4(a, b): # a and b are lists with the same length N
    n = len(a) #This is O(1)
    assert(n == len(b)) #This is O(1)
    result = abs(a[0] - b[0]) #This is O(1)
    for c in a: #This is O(n)
        for d in b: #This is O(n)
            delta = abs(c - d) #This is O(1)
            if (delta > result): #This is O(1)
                result = delta #This is O(1)
    return result #This is O(1)

A. This function finds the biggest abs difference comparing each element between
 a and b, and it returns that largest value produced by that combination.

B. The resulting Big-O of this function is O(n ** 2).

C.
def fast4(a, b):
    n = len(a) #This is O(1)
    assert (n == len(b)) #This is O(1)
    if min(a) < min(b): #This is O(n)
        return abs(min(a) - max(b)) #This is O(n)
    else:
        return abs(max(a) - min(b)) #This is O(n)

D. The resulting Big-O of the whole function is O(n).

################################################################################
"""

def largestSumOfPairs(a):
    if len(a) <= 1:
        return None
    largest = max(a)
    a.remove(max(a))
    secLargest = max(a)
    return largest + secLargest

def friendsOfFriends(d):
    outputDict = dict()
    l = list()
    for person in d: # person is the person's name in input dict
        for f in d[person]: # f is the friend of each person in the input dict
            for fof in d[f]: # fof stands for friend of friend
                if fof != person and fof not in d[person]:
                    # fof is not the person herself and is not one of her
                    # direct friends.
                    l.append(fof)
        outputDict[person] = set(l)
        l = []
    return outputDict

def testlargestSumOfPairs():
    print('Testing largestSumOfPairs()...', end="")
    assert (largestSumOfPairs([]) == None)
    assert (largestSumOfPairs([1,2,3,4,5]) == 9)
    assert (largestSumOfPairs([8,2,4,8]) == 16)
    assert (largestSumOfPairs([1,1,1,1,1]) == 2)
    assert (largestSumOfPairs([0,0,0]) == 0)
    assert (largestSumOfPairs([1]) == None)
    print("Passed!")

def testfriendsOfFriends():
    print('Testing friendsOfFriends()...', end="")
    d = {}
    d["jon"] = set(["arya", "tyrion"])
    d["tyrion"] = set(["jon", "jaime", "pod"])
    d["arya"] = set(["jon"])
    d["jaime"] = set(["tyrion", "brienne"])
    d["brienne"] = set(["jaime", "pod"])
    d["pod"] = set(["tyrion", "brienne", "jaime"])
    d["ramsay"] = set()
    result1 = {
 'tyrion': {'arya', 'brienne'},
 'pod': {'jon'},
 'brienne': {'tyrion'},
 'arya': {'tyrion'},
 'jon': {'pod', 'jaime'},
 'jaime': {'pod', 'jon'},
 'ramsay': set()
}
    assert (friendsOfFriends(d) == result1)
    print("Passed!")

def testAll():
    testlargestSumOfPairs()
    testfriendsOfFriends()

def main():
    testAll()

if __name__ == '__main__':
    main()