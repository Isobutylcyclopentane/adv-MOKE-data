#for data that contains multiple loops

import statistics
from point import *
import os
from singleloop import *
import math

class MokeDataFile(object):
    def __init__(self, globalPath, filename, data):

        self.globalPath = globalPath
        self.filename = filename
        self.aziAngle = self.find_Azi_angle()
        self.data = data.copy()
        self.rough_center()
        self.separated = self.analyze()



        self.Hc = self.calculate_avg_Hc()
        self.Mr = self.calculate_avg_Mr()
        self.Ms = self.calculate_avg_Ms()
        self.skewness = self.calculate_avg_skewness()
        # self.separated = temporary[0]
        # self.xInter = temporary[1]
        # self.yInter = temporary[2]

    def rough_center(self):

        numOfAna = math.ceil(len(self.data) / 20)

        tempStorage = sorted(self.data)
        tempY = [point.y for point in tempStorage]

        allyMax = statistics.mean(tempY[-numOfAna:])
        allyMin = statistics.mean(tempY[:numOfAna])

        adjY = (allyMax + allyMin) / 2
        for pointIndex in range(len(self.data)):
            self.data[pointIndex].y -= adjY

        return


    def analyze(self) -> dict:

        loopCount = 0
        temp = []
        xintertemp = []
        yintertemp = []
        result = dict()
        for i in range(len(self.data)):
            # print("DEBUG 20033 self.data[i]", self.data[i])
            # print("DEBUG 20034", len(temp), len(xintertemp), len(yintertemp))
            if i == 0:
                temp.append(self.data[i])
                continue
            if i + 1 == len(self.data):
                temp.append(self.data[i])
                result[loopCount] = Singleloop(temp, xintertemp, yintertemp)
                temp.clear()
                xintertemp.clear()
                yintertemp.clear()
                break

            currentPoint = self.data[i]
            previousPoint = self.data[i-1]
            nextPoint = self.data[i+1]

            temp.append(currentPoint)

            if currentPoint.is_intersection(previousPoint, 1):
                xintertemp.append((previousPoint, currentPoint))
            if currentPoint.is_intersection(previousPoint, 0):
                yintertemp.append((previousPoint, currentPoint))




                if i + 4 < len(self.data):
                    next2 = self.data[i+2]
                    next3 = self.data[i+3]
                    next4 = self.data[i+4]
                    if next2.is_zigzag(nextPoint, next3):
                        continue
                    if next3.is_zigzag(next2, next4):
                        continue


                result[loopCount] = Singleloop(temp, xintertemp, yintertemp)
                temp.clear()
                xintertemp.clear()
                yintertemp.clear()
                loopCount += 1
                # print("DEBUG a loop completed", loopCount)

        return result

    def calculate_avg_Hc(self) -> float:
        dataSet = []
        for loopCount in self.separated:
            loop = self.separated[loopCount]
            # print("DEBUG 30072", loop, len(loop.data))
            if loop.get_Hc() == False:
                print("***ERROR: in file", self.filename + \
                      "({})".format(loopCount),": Incomplete data set")
                loop.plot_and_save(self.data, self.globalPath, self.filename,
                                   loopCount, "INCOMPLETE", True)
            elif loop.get_Hc() == True:
                print("***WARNING: in file", self.filename + \
                      "({})".format(loopCount),
                      ": multiple penetration appears in one loop")
                loop.plot_and_save(self.data, self.globalPath, self.filename,
                                   loopCount, "REJECTED", True)
            else:
                dataSet.append(loop.get_Hc())
                loop.plot_and_save(self.data, self.globalPath, self.filename,
                                   loopCount, "ANALYSED")
        if len(dataSet) == 0:
            return False
        result = statistics.mean(dataSet)
        return result

    def calculate_avg_Mr(self) -> float:
        dataset = []
        for loopCount in self.separated:
            loop = self.separated[loopCount]
            if type(loop.get_Mr()) == bool:
                continue
            else:
                dataset.append(loop.get_Mr())
        if len(dataset) == 0:
            return False
        result = statistics.mean(dataset)
        return result

    def calculate_avg_Ms(self):
        dataset = []
        for loopCount in self.separated:
            loop = self.separated[loopCount]
            if type(loop.get_Mr) == bool:
                continue
            else:
                dataset.append(loop.get_Ms())
        if len(dataset) == 0:
            return False
        result = statistics.mean(dataset)
        return result

    def calculate_avg_skewness(self):
        dataset = []
        for loopCount in self.separated:
            loop = self.separated[loopCount]
            if (type(loop.get_skewness()) == bool):
                continue
            dataset.append(loop.get_skewness())
        if len(dataset) == 0:
            return False
        result = statistics.mean(dataset)
        # if result > 1:
        #     return self.get_avg_Mr() / self.get_avg_Ms()
        return result

    def find_Azi_angle(self):
        temp = self.filename.split('_')[0].split(' ')[-1]
        result = int(temp)
        if result > 360:
            result -= 360
        return result

    def update(self, other):
        self.Hc = update_helper(self.Hc, other.Hc)
        self.Mr = update_helper(self.Mr, other.Mr)
        self.Ms = update_helper(self.Ms, other.Ms)
        self.skewness = update_helper(self.skewness, other.skewness)
        for loopIndex in other.separated:
            self.separated[max(self.separated)+1] = other.separated[loopIndex]
        return

    def get_avg_Hc(self):
        return abs(self.Hc)

    def get_avg_Mr(self):
        return abs(self.Mr)

    def get_avg_Ms(self):
        return abs(self.Ms)

    def get_avg_skewness(self):
        return abs(self.skewness)

    def get_aziAngle(self):
        return self.aziAngle

    def get_data(self):
        return self.data

    def __repr__(self):
        result = ""
        for loopCount in self.separated:
            result += "({})".format(loopCount) + \
                      str(self.separated[loopCount]) + '\n'
        return result


    '''
    def analyze(self):

        loopCount = 0
        loopResult = dict()
        xInterResult = dict()
        yInterResult = dict()

        temp = []
        for i in range(len(self.data)):

            if i == 0:
                continue
            if i + 1 == len(self.data):
                temp.append(data[i])
                loopCount += 1
                break

            currentPoint = self.data[i]
            previousPoint = self.data[i-1]
            nextPoint = self.data[i+1]

            temp.append(currentPoint)

            if currentPoint.is_intersection(previousPoint, 0):
                if loopCount not in xInterResult:
                    xInterResult[loopCount] = []

                xInterResult[loopCount].append(previousPoint, currentPoint)
            if currentPoint.is_intersection(previousPoint, 1):
                if loopCount not in yInterResult:
                    yInterResult[loopCount] = []
                yInterResult[loopCount].append(previousPoint, currentPoint)

            if currentPoint.is_turning(previousPoint, nextPoint):
                if loopCount not in loopResult:
                    loopResult[loopCount] = temp.copy()
                temp.clear()
                loopCount += 1
    '''
    '''
                    if i == 0:
                        continue
                    previousPoint = self.data[i-1]
                    currentPoint = self.data[i]
                    previousSignX = get_sign(previousPoint, 0)
                    currentPointX = get_sign(currentPoint, 0)
                    previousSignY = get_sign()

                    dxLast = previousPoint[0] - currentPoint[0]
                    if (i+2) ==len(self.data):
                        temp.append(self.data[i+1])
                        temp.append(self.data[i+2])
                        break

                    temp.append(currentPoint)

                    nextPoint1 = self.data[i+1]
                    nextPoint2 = self.data[i+2]
                    dxNext = nextPoint1 - nextPoint2

                    if (dxLast < 0) and (dxNext > 0):
                        loopCount += 1
                        loopResult[loopCount] = temp.copy()
                        temp.clear()
    '''
    '''
        return loopResult, xInterResult, yInterResult


    def get_average_Hc(self):
        for loop in self.xInter:
            data = self.xInter[loop]
            if (len(data) > 2):

                print("***WARNING: multiple x-intersections appeared in single loop")
                print("\texperiment data rejected")
                plot_and_save(self.globalPath, self.filename, "MULTI_INTERSECTION", data)
                continue
            elif len(data < 2):
                plot_and_save(self.globalPath, self.filename, "INCOMPLETE", data)
                print("ERROR: Incomplete loop\n\texperiment data rejected")
            else:

def find_point_intersection(points):
    xset = [x[0] for x in points]
    yset = [y[0] for y in points]


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def plot_and_save (path, filename, location, expData):

    newFileName = filename.replace(".xlsx", ".jpg")
    newPathName = path + "\\GRAPHS" + "\\"+ location

    if not os.path.isdir(newPathName):
        os.makedirs(newPathName)

    newPathName += '\\' + "CENTERED_" + newFileName
    dataX = np.array([point.x for point in expData])
    dataY = np.array([point.y for point in expData])
    plt.plot(dataX, dataY)
    plt.grid(True)
    plt.savefig(newPathName)
    plt.close()
    return
'''

class MokeTempFile(object):
    def __init__(self):
        return

    def get_avg_Hc(self):
        return 0

    def get_avg_skewness(self):
        return 0


def read_file(filename):
    resultData = []
    file = open(filename, encoding="UTF-8-sig")

    for line in file:

        if '\t' in line:
            tempLst = line.split('\t')
            tempVal = Point(float(tempLst[1]), float(tempLst[2]))
            resultData.append(tempVal)

    return resultData

def update_helper(d1, d2):

    if (type(d1) == bool) and (type(d2 == bool)):
        return False

    if type(d1) == bool:
        return d2
    elif type(d2) == bool:
        return d1
    else:
        return (d1 + d2) / 2

if __name__ == '__main__':
    path = "C:\\Users\\J. Cheng\\Dropbox\\AFM_image\\1111_MULTILOOP\\DATA"
    fname = "AlCo 0.2v 50 pionts Azimuthal 0_5b.xlsx"
    filename = os.path.join(path, fname)
    d = read_file(filename)

    test = MokeDataFile(path, fname, d)
    # print("DEBUG 20269 len(test)", len(test.separated))

    print(test.get_avg_Hc())
    print(test.get_avg_Ms())