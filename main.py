
import os
import statistics
import math
import shutil
import glob
import ntpath
from matplotlib import pyplot as plt
import numpy as np

from multiloop import *
from singleloop import *
from point import *

class ExpResult (object):
    def __init__(self):
        self.storage = dict()

    def append(self, multi):
        azi_angel = multi.get_aziAngle()
        if azi_angel not in self.storage:
            self.storage[azi_angel] = multi
        else:
            self.storage[azi_angel].update(multi)
        return

    def get_all_azimuthal_Hc (self):
        dataX = list()
        dataY = list()
        all_angle = sorted(self.storage)
        for azi in all_angle:
            x = (azi / 180) * math.pi
            dataX.append(x)
            y = self.storage[azi].get_avg_Hc()
            dataY.append(y)
        return dataX, dataY

    def get_all_azimuthal_skewness(self):
        datax = []
        datay = []
        all_angle = sorted(self.storage)
        for azi in all_angle:
            x = (azi / 180) * math.pi
            y = self.storage[azi].get_avg_skewness()
            if type(y) == bool:
                continue
            datax.append(x)
            datay.append(y)
        return datax, datay

    def check_completeness(self):
        flag = True
        maxAngle = max(self.storage)
        for a in range(maxAngle, -1, -15):
            if a not in self.storage:
                flag = False
                break
        return flag

    def rough_fill(self):
        maxAngle = max(self.storage)
        for a in range(maxAngle, -1, -15):
            if a not in self.storage:
                self.storage[a] = MokeTempFile()
        return

    def __str__(self):
        result = ''
        for index in sorted(self.storage):
            result += "{} | < {} | {} >\n".format(index, self.storage[index].get_avg_Hc(),
                                                  self.storage[index].get_avg_skewness())
        return result

    def print_detail(self):
        result = ""
        for index in sorted(self.storage):
            result += str(index) + "\n" + str(self.storage[index])
        return result


def read_file(filename):
    resultData = []
    file = open(filename, encoding="UTF-8-sig")

    for line in file:

        if '\t' in line:
            tempLst = line.split('\t')
            tempVal = Point(float(tempLst[1]), float(tempLst[2]))
            resultData.append(tempVal)

    return resultData

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def delete_previous_plots(basepath, delfilename="DELETE.txt"):
    bpath = os.path.join(basepath, "")



def grand_main(basepath):
    result = ExpResult()
    for pathname in glob.glob(os.path.join(basepath, '*.xlsx')):

        filename = path_leaf(pathname)

        # print("DEBUG 10093", filename)

        tempDATA = read_file(pathname)
        tempMulti = MokeDataFile(basepath, filename, tempDATA)

        if tempMulti.get_avg_skewness() > 1:
            print("DEBUG 10102")
            print(filename)
            print(tempMulti.get_avg_Mr())
            print(tempMulti.get_avg_Ms())
            print(tempMulti.get_avg_skewness())


        result.append(tempMulti)

    HcX, HcY = result.get_all_azimuthal_Hc()
    skewX, skewY = result.get_all_azimuthal_skewness()


    plt.polar(HcX, HcY)
    plt.show()
    plt.close()

    plt.polar(skewX, skewY)
    plt.show()
    plt.close()

    print(result)

    # r = result.print_detail()
    # print(r)
    # a = result.storage[315].separated[1].yIntersection
    # print(a)


if __name__ == '__main__':
    path = "C:\\Users\\J. Cheng\\Dropbox\\AFM_image\\1111_MULTILOOP\\DATA"
    grand_main(path)

