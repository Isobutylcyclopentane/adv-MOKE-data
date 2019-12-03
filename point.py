

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_sign(self, mode):
        result = 0
        if mode == 0:
            if self.x == 0:
                pass
            else:
                if self.x < 0:
                    result = -1
                else:
                    result = 1
        elif mode == 1:
            if self.y == 0:
                pass
            else:
                if self.y < 0:
                    result = -1
                else:
                    result = 1
        else:
            print("***ERROR: in class Point, get_sign(), \nInvalid mode input")
        return result

    def is_intersection(self, previous, mode):
        currentSign = self.get_sign(mode)
        previousSign = previous.get_sign(mode)
        if currentSign == previousSign:
            return False
        else:
            return True

    def is_turning(self, previous, next):
        previousDx = self.x - previous.x
        nextDx = next.x - self.x
        if previousDx >= 0 and nextDx <= 0:
            return True
        else:
            return False

    def is_zigzag(self, previous, next):
        previousDx = self.x - previous.x
        nextDx = next.x - self.x
        if (previousDx/abs(previousDx)) != (nextDx/abs(nextDx)):
            return True
        return False

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        else:
            if self.y < other.y:
                return True
            else:
                return False

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

