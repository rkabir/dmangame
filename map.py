# A map class, responsible for map functions, like
# finding the square a unit is on or what occupies a square
import math
import random
import logging
log = logging.getLogger("MAP")

class Map:
    def __init__(self, N):
        self.size = N
        self.objectMap = {}
        self.squareMap = {}
        self.__bullet_paths = {}
        self.__unit_paths = {}
        self.__legal_moves = {}

    def getRandomSquare(self):
        return (random.randint(0, self.size), random.randint(0, self.size))

    # Place a map object onto the map
    def placeObject(self, mapobject, square):
        if self.isValidSquare(square):
            self.objectMap[mapobject] = square
            try:
                self.squareMap[square].append(mapobject)
            except KeyError:
                self.squareMap[square] = [mapobject]

    # Remove the object from the map
    def removeObject(self, mapobject):
        if mapobject in self.objectMap:
            self.squareMap[self.objectMap[mapobject]].remove(mapobject)
            del self.objectMap[mapobject]

    # Returns the square mapobject is on
    def getPosition(self, mapobject):
        try:
            return self.objectMap[mapobject]
        except KeyError, e:
            log.debug("Get Position errored with: %s", e)
            return None


    # Returns the mapobject on square
    def getOccupants(self, square):
        if self.isValidSquare(square):
            return self.squareMap[square]
        # Raise an exception

    # Returns all the object on the map
    def getAllObjects(self):
        return self.objectMap.keys()

    def isValidSquare(self, square):
        x,y = square
        return x < self.size and x >= 0 and y < self.size and y >= 0

    # Get all squares within radius n of square
    def getLegalMoves(self, square, n):
        lm_key = str((square, n, ))
        try:
          return self.__legal_moves[lm_key]
        except:
          pass

        log.debug("Calculating legal moves for %s",(str(lm_key)))
        d = set()
        x,y = square
        d.add((x,y))

        for i in xrange (0, n+1):
            for j in xrange(min(n-i, i+1), max(n-i, i+1)):
                # i in x, j in y
                if (x+i < self.size) and (y+j < self.size):
                    d.add((x+i, y+j))
                if (x+i < self.size) and (y-j >= 0):
                    d.add((x+i, y-j))
                if (x-i >= 0) and (y+j < self.size):
                    d.add((x-i, y+j))
                if (x-i >= 0) and (y-j >= 0):
                    d.add((x-i, y-j))

                # j in x, i in y
                if (x+j < self.size) and (y+i < self.size):
                    d.add((x+j, y+i))
                if (x+j < self.size) and (y-i >= 0):
                    d.add((x+j, y-i))
                if (x-j >= 0) and (y+i < self.size):
                    d.add((x-j, y+i))
                if (x-j >= 0) and (y-i >= 0):
                    d.add((x-j, y-i))

        self.__legal_moves[lm_key] = d
        return self.__legal_moves[lm_key]

    # Get the distance between x,y and m,n
    def getDistance(self, start, end):
        x,y = start
        m,n = end
        return math.sqrt((m-x)**2 + (n-y)**2)

    # Get the path a bullet takes from x,y to m,n
    # R is the range on the bullets...why is this here?
    def getBulletPath(self, start, end, R):
        x, y = start
        m, n = end
        bp_key = ",".join(map(str, (x,y,m,n)))
        if not bp_key in self.__bullet_paths:
            path = []
            if x-m is 0:
                    path = [(x, i+1) for i in xrange(min(y, n), min(y, n) + R)]
            elif y-n is 0:
                    path = [(j+1, y) for j in xrange(min(x, m), min(x, m) + R)]
            else:
                    slope = abs(float(n-y)/float(m-x))
                    if slope < 1:
                            xmovement = 1
                            ymovement = slope
                    else:
                            xmovement = 1/slope
                            ymovement = 1
                    if x > m:
                            xmovement = -xmovement
                    if y > n:
                            ymovement = -ymovement
                    index = 0
                    x += .5
                    y += .5
                    while index <= R and self.isValidSquare((x,y)):
                            x += xmovement
                            y += ymovement
                            path.append((int(x), int(y)))
                            index += 1


            self.__bullet_paths[bp_key] = path
        return self.__bullet_paths[bp_key]

    # Get the path a unit takes when travelling from (x,y) to (m,n)
    def getUnitPath(self, start, end):
        x,y = start
        m,n = end
        up_key = ",".join(map(str, (x,y,m,n)))
        if not up_key in self.__unit_paths:
            log.debug("Calculating path from %s to %s", (x, y), (m, n))
            if x == m:
                if y == n:
                    return [(m,n)]
                else:
                    slope = 1.0
            else:
                slope = float(n-y)/float(m-x)

            path = []
            i = 0.0
            j = 0.0
            xdir = 1
            ydir = 1
            if abs(slope) < 1:
                    xmovement = 1
                    ymovement = slope
            else:
                xmovement = 1/slope
                ymovement = 1

            if (x > m):
                xmovement = -xmovement
                xdir = -1
            if (y > n):
                ymovement = -ymovement
                ydir = -1


            # [TODO] Generate this the right way
            while x != m or y != n:
                if x - m != 0:
                    for b in xrange(abs(int(xmovement+i))):
                        x += xdir
                        path.append((x,y))
                        if x == m:
                            break
                    i = (xmovement+i)-int(xmovement+i)

                if y - n != 0:
                    for a in xrange(abs(int(ymovement+j))):
                        y += ydir
                        path.append((x,y))
                        if y == n:
                            break
                    j = (ymovement+j)-int(ymovement+j)

            self.__unit_paths[up_key] = path
        return self.__unit_paths[up_key]


if __name__ == "__main__":
    m = Map(200)
    m.getUnitPath((11, 13),(0, 193))
    #x = "Just a unit"
    #m.placeObject(x, (0,0))
    #m.getPosition(x)
    #m.getOccupant((0,0))
    #m.getAllObjects()
    #m.removeObject(x)
    #m.getAllObjects()
    #m.getPosition(x)
    path = m.getBulletPath((6, 16), (6, 70), int(m.size/8))
    #m.getlegalmoves((5,5), 2)
