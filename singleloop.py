

import statistics
import math
import os
from scipy import optimize
from point import *
from matplotlib import pyplot as plt

class Singleloop(object):
    def __init__(self, data, xIntersection, yIntersection):
        self.data = data.copy()

        #self.rough_center()

        # print("DEBUG 10015", len(data))

        self.xIntersection = xIntersection.copy()
        self.yIntersection = yIntersection.copy()

        # print("DEBUG 10020")
        # for i in self.xIntersection:
        #     for j in i:
        #         print("DEBUG 10023", j)

        self.Hc_left_raw, self.Hc_right_raw = self.calculate_Hc()

        self.Hc_left, self.Hc_right = self.Hc_left_raw, self.Hc_right_raw

        if type(self.Hc_left_raw) != bool:
            self.center_data()
            self.center_Hc()
        self.Ms = self.calculate_Ms()
        self.Mr_upper, self.Mr_lower = self.calculate_Mr()
        if type(self.Mr_upper) != bool:
            self.center_Mr()

        self.skewness = self.calculate_skewness()
        print("DEBUG 10039 skewness", self.skewness)

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

    def calculate_Hc(self) -> tuple:
        if len(self.xIntersection) < 2:
            return False, False
        elif len(self.xIntersection) > 2:
            return False, True
        else:
            Hc_left_raw = find_point_intersection(self.xIntersection[0],  0)
            Hc_right_raw = find_point_intersection(self.xIntersection[1], 0)

        return Hc_left_raw, Hc_right_raw

    def calculate_Mr(self) -> tuple:
        if len(self.yIntersection) < 2:
            return False, False
        elif len(self.yIntersection) > 2:
            return False, True
        else:

            Mr_upper = find_point_intersection(self.yIntersection[0], 1)
            Mr_lower = find_point_intersection(self.yIntersection[1], 1)
            return Mr_upper, Mr_lower

    def calculate_Ms(self):
        numOfAna = math.ceil(len(self.data) / 20)
        tempData = sorted(self.data, key=lambda x: x.y)
        tempUpper = [p.y for p in tempData[-numOfAna:]]
        tempLower = [p.y for p in tempData[:numOfAna]]


        MsUpper = sum(tempUpper) / len(tempUpper)
        MsLower = sum(tempLower) / len(tempLower)
        uncent = (MsUpper + MsLower) / 2
        Ms = MsUpper - uncent

        return abs(Ms)

    def calculate_skewness(self):
        if type(self.Mr_lower) == bool:
            return False
        else:
            return self.get_Mr() / self.get_Ms()

    def center_Hc(self) -> None:
        if type(self.Hc_left_raw) == bool:
            return
        uncent = (self.Hc_right_raw + self.Hc_left_raw) / 2
        self.Hc_right = self.Hc_right_raw - uncent
        self.Hc_left = self.Hc_left_raw - uncent
        return

    def center_Mr(self) -> None:
        if self.Mr_upper == False:
            return

        uncent = (self.Mr_upper + self.Mr_lower) / 2
        self.Mr_upper = self.Mr_upper - uncent
        self.Mr_lower = self.Mr_lower - uncent
        return

    def get_uncentHor(self) -> float:
        # print("DEBUG 10076", self.Hc_right_raw, self.Hc_left_raw)
        if type(self.Hc_left_raw) == bool:
            return 0
        uncentHor = (self.Hc_right_raw + self.Hc_left_raw) / 2
        return uncentHor

    def center_data(self):
        temp = sorted(self.data)
        tempy = [point.y for point in temp]
        numOfAna = math.ceil(len(tempy) / 20)
        upper = statistics.mean(tempy[:numOfAna])
        lower = statistics.mean(tempy[-numOfAna:])
        uncentVer = (upper + lower) / 2
        uncentHor = self.get_uncentHor()

        #print("DEBUG 10088, uncentHor", uncentHor)

        # print("DEBUG 30076, ver, hor", uncentVer, uncentHor)

        for i in range(len(self.data)):
            self.data[i].y -= uncentVer
            self.data[i].x -= uncentHor
        return

    def get_Hc(self):
        return self.Hc_right


    def get_Mr(self):
        if type(self.Mr_upper) != bool:
            return (abs(self.Mr_upper) + abs(self.Mr_lower)) / 2

        return self.Mr_lower

    def get_Ms(self):
        return self.Ms

    def get_skewness(self):
        return self.skewness

    def plot_and_save(self, Alldata, path, filename,
                      loopCount, location, status=False):
        newFileName = filename.replace(".xlsx", '')
        newPathName = os.path.join(path, location, newFileName)
        if not os.path.isdir(newPathName):
            os.makedirs(newPathName)
        # newFile = open(newPathName, "w+")
        newFileName = newFileName + "({})".format((loopCount + 1)) + ".jpg"
        newPathName = os.path.join(newPathName, newFileName)


        dataX = [point.x for point in Alldata]
        dataY = [point.y for point in Alldata]
        plt.plot(dataX, dataY)


        # print("DEBUG 10117", len(self.data))

        dataX = [point.x for point in self.data]
        dataY = [point.y for point in self.data]

        # print("DEBUG 10110", len(dataX), len(dataY))

        plt.plot(dataX, dataY)

        plt.grid(True)
        plt.savefig(newPathName)
        plt.close()
        return

    def __repr__(self):
        return "<Hc {} |Mr {} |Ms {} |sqr {}>".format(self.get_Hc(),
                                            self.get_Mr(),
                                            self.get_Ms(),
                                            self.get_skewness())

def find_point_intersection(points, mode) -> float:
    dataX = [point.x for point in points]
    dataY = [point.y for point in points]
    popt, pcov = list(optimize.curve_fit(linear, dataX, dataY))
    a, b = popt
    if mode == 0:
        return (-b/a)
    else:
        return b



def linear(x,a,b):
    return a * x + b

'''
def read_file(filename):
    resultData = []
    file = open(filename, encoding="UTF-8-sig")

    for line in file:

        if '\t' in line:
            tempLst = line.split('\t')
            tempVal = Point(float(tempLst[1]), float(tempLst[2]))
            resultData.append(tempVal)

    return resultData
'''