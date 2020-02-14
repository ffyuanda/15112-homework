import math

##############
# Helper function
def helperFor3ToN(limit, output, power):
    # Be wrapped by the powersOf3ToN function
    # in order to carry over the value stored in
    # list and the power of 3.
    if limit < 1:
        return None
    curr = 3 ** power
    if curr > limit:
        return output
    output.append(curr)
    return helperFor3ToN(limit, output, power + 1)


##############

def powerSum(n, k):
    #######
    # From the largest term to the smallest term.
    if n < 0 or k < 0:
        return 0

    if n == 1:
        return 1
    return n ** k + powerSum(n - 1, k)


def powersOf3ToN(n):
    return helperFor3ToN(n, [], 0)


#########OOP############
class Asteroid(object):
    def __init__(self, cx, cy, r, v, direction=(0, 1)):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.v = v
        self.direction = (0, 1)

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

    def reactToBulletHit(self):
        self.direction = 0, 0


class ShrinkingAsteroid(Asteroid):
    def __init__(self, cx, cy, r, v, direction=(0, 1), shrinkAmount=5):
        super().__init__(cx, cy, r, v, direction=(0, 1))
        self.shrinkAmount = shrinkAmount

    def reactToBulletHit(self):
        self.r -= self.shrinkAmount

    def bounce(self):
        self.direction = -self.direction[0], -self.direction[1]


class SplittingAsteroid(Asteroid):
    def __init__(self, cx, cy, r, v, direction=(0, 1)):
        super().__init__(cx, cy, r, v, direction=(0, 1))

    def reactToBulletHit(self):
        asteroid1 = SplittingAsteroid(self.cx - self.r, self.cy - self.r,
                                      self.r // 2, self.v, self.direction)
        asteroid2 = SplittingAsteroid(self.cx + self.r, self.cy + self.r,
                                      self.r // 2, self.v, self.direction)
        return asteroid1, asteroid2


######################
# Testing methods.
# ignore_rest

def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = []
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)


def testAsteroidClasses():
    print("Testing Asteroids classes...", end="")
    # A basic Asteroid takes in cx, cy, radius, speed, and optional direction.
    # It's default direction (dx, dy) is (0, 1), or moving down
    asteroid1 = Asteroid(25, 50, 20, 5)
    assert (type(asteroid1) == Asteroid)
    assert (isinstance(asteroid1, Asteroid))
    asteroid1.setDirection((-1, 0))
    assert (asteroid1.getDirection() == (-1, 0))
    assert (str(asteroid1) ==
            "Asteroid at (25, 50) with radius=20 and direction (-1, 0)")

    assert (str([asteroid1]) ==
            "[Asteroid at (25, 50) with radius=20 and direction (-1, 0)]")

    # isCollisionWithWall takes in the canvasWidth and canvasHeight
    # Asteroids collide with walls if any part of them is touching any side
    # of the canvas
    assert (asteroid1.isCollisionWithWall(400, 400) == False)
    asteroid1.moveAsteroid()
    assert (str(asteroid1) ==
            "Asteroid at (20, 50) with radius=20 and direction (-1, 0)")
    assert (asteroid1.getPositionAndRadius() == (20, 50, 20))
    assert (asteroid1.isCollisionWithWall(400, 400) == True)
    # A normal asteroid is stunned when it is hit by a bullet, and it freezes
    asteroid1.reactToBulletHit()
    assert (asteroid1.getDirection() == (0, 0))
    localMethods = ['__init__', '__repr__',
                    'getDirection', 'getPositionAndRadius',
                    'isCollisionWithWall', 'moveAsteroid',
                    'reactToBulletHit', 'setDirection']
    methodsFound = getLocalMethods(Asteroid)
    for method in localMethods:
        assert (method in methodsFound)

    # A Shrinking Asteroid takes in cx, cy, radius, speed,
    # an optional direction (that is (0, 1) by default),
    # and an optional shrinkAmount set to 5 pixels by default.
    # ShrinkAmount is how much the radius of the asteroid decreases when it is
    # hit by a bullet. A Shrinking Asteroid can also bounce off the walls.
    asteroid2 = ShrinkingAsteroid(200, 200, 50, 20)
    assert (type(asteroid2) == ShrinkingAsteroid)
    assert (isinstance(asteroid2, ShrinkingAsteroid))
    assert (isinstance(asteroid2, Asteroid))
    asteroid2.reactToBulletHit()
    assert (asteroid2.getPositionAndRadius() == (200, 200, 45))
    assert (str(asteroid2) ==
            "ShrinkingAsteroid at (200, 200) "
            "with radius=45 and direction (0, 1)")
    asteroid2.setDirection((1, -1))
    asteroid2.bounce()
    assert (asteroid2.getDirection() == (-1, 1))
    asteroid3 = ShrinkingAsteroid(100, 100, 40, 10,
                                  direction=(0, -1), shrinkAmount=20)
    # The asteroid's radius will decrease by the shrinkAmount
    asteroid3.reactToBulletHit()
    assert (asteroid3.getPositionAndRadius() == (100, 100, 20))
    # print(getLocalMethods(ShrinkingAsteroid))

    assert (getLocalMethods(ShrinkingAsteroid) == ['__init__', 'bounce',
                                                   'reactToBulletHit'])

    # A Splitting Asteroid takes in cx, cy, radius, speed, and an optional
    # direction (set to (0, 1) by default). It splits into two smaller
    # Splitting Asteroids when hit by a bullet.
    # The each smaller Splitting Asteroid has radius that is half of
    # the original Splitting Asteroid's and
    # has the original speed and direction
    asteroid4 = SplittingAsteroid(300, 300, 20, 15)
    assert (type(asteroid4) == SplittingAsteroid)
    assert (isinstance(asteroid4, SplittingAsteroid))
    assert (isinstance(asteroid4, Asteroid))
    assert (not isinstance(asteroid4, ShrinkingAsteroid))
    # reactToBulletHit returns 2 new instances of the SplittingAsteroid class
    asteroid5, asteroid6 = asteroid4.reactToBulletHit()
    # The new Splitting Asteroid centers are at the top-left and bottom-right
    # corners of the bounding box surrounding the original asteroid
    # See the test cases below for an example:
    assert (asteroid5.getPositionAndRadius() == (280, 280, 10))
    assert (asteroid6.getPositionAndRadius() == (320, 320, 10))
    assert (str(asteroid6) ==
            "SplittingAsteroid at (320, 320) wit"
            "h radius=10 and direction (0, 1)")
    assert (getLocalMethods(SplittingAsteroid) == ['__init__',
                                                   'reactToBulletHit'])
    print("Done!")


def testpowerSum():
    print("Testing powerSum()...", end="")
    assert (powerSum(1, 2) == 1)
    assert (powerSum(-1, -1) == 0)
    assert (powerSum(3, 4) == 98)
    assert (powerSum(0, 0) == 1)
    print("Passed!")


def testpowersOf3ToN():
    print("Testing powersOf3ToN()...", end="")
    assert (powersOf3ToN(10.5) == [1, 3, 9])
    assert (powersOf3ToN(29) == [1, 3, 9, 27])
    assert (powersOf3ToN(0) == None)
    assert (powersOf3ToN(-1) == None)
    print("Passed!")


def testAll():
    testpowerSum()
    testpowersOf3ToN()
    testAsteroidClasses()


def main():
    testAll()


if __name__ == '__main__':
    main()
