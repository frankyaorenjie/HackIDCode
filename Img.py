#!/usr/bin/python

import Image
import numpy
import urllib2
import time
import math
import sys
import os
from pychart import *

theme.get_options()

class Img(object):
    
    def __init__(self,img_path):
        try:
            self.__img_url = urllib2.urlopen(img_path)
            self.__file_name = time.strftime("%Y%m%d%H%M%S")+".jpeg"
            o = open(self.__file_name,"aw")
            o.writelines(self.__img_url.readlines())
            o.close()
        except:
            self.__file_name = img_path
        self.__img = Image.open(self.__file_name)

    def getSize(self):
        return self.__img.size

    def RGB2I(self,RGB_list):
        R,G,B = RGB_list
        return round((R+G+B)/3,2)
    
    def getRGBMatrix(self):
        self.__RGB_Matix = numpy.int16(numpy.asarray(self.__img))
        return self.__RGB_Matix

    def getHSIMatrix(self):
        HSI_Matrix = []
        for line in self.__RGB_Matix:
            RGB_line = []
            for element in line:
                RGB_line.append(self.RGB2I(element))
            HSI_Matrix.append(RGB_line)
        return HSI_Matrix

def plotStat(data_list):
    ar = area.T(size = (150, 120),
                y_grid_interval = 10,
                x_axis = axis.X(label="Lightness"),
                y_axis = axis.Y(label="Times"),
                legend = legend.T(), x_range = (0,300), y_range = (0, None))
    ar.add_plot(bar_plot.T(label="L", data=data_list))
    ar.draw()

def UP(a, b):
    return int((a+b-1)/b)

def matrix2data(dual, interval):
    n = UP(360, interval)
    d = {}
    result = []
    for i in range(0,n+1):
        d[i] = 0
    for line in dual:
        for element in line:
            d[UP(element, interval)] += 1
    keys = d.keys()
    for key in keys:
        result.append((key,d[key]))
    return result

def matrix2image(im, matrix):
    n1 = len(matrix)
    n2 = len(matrix[0])
    for i in range(0, n1):
        for j in range(0, n2):
            im.putpixel((j,i), tuple(matrix[i][j]))
    return im

def replacePixel(im, HSI_matrix, HSI_old, new, r):
    n1 = len(HSI_matrix)
    n2 = len(HSI_matrix[0])
    for i in range(0, n1):
        for j in range(0, n2):
            if abs(HSI_matrix[i][j] - HSI_old) < r:
                im.putpixel((j,i), new)
    return im

def colRate(HSI_matrix):
    rate = []
    n1 = len(HSI_matrix)
    n2 = len(HSI_matrix[0])
    for j in range(0, n2):
        col_rate = 0
        for i in range(0, n1):
            col_rate += HSI_matrix[i][j]
        rate.append(col_rate/n1)
    return rate

if __name__ == "__main__":
    os.popen("rm *.jpeg")
    path = "http://hub.hust.edu.cn/randomImage.action"
    #path = ""
    img = Img(path)
    RGB_matrix = img.getRGBMatrix()
    im = Image.new("RGB", img.getSize())
    HSI_matrix = img.getHSIMatrix()
    #black_im = matrix2image(im, RGB_matrix)
    white_im = matrix2image(im, RGB_matrix)
    data = matrix2data(HSI_matrix, 1)
    max_H = sorted(data, key=lambda data:data[1], reverse=True)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    #black_im = replacePixel(black_im, HSI_matrix, max_H[0][0], BLACK, 8)
    white_im = replacePixel(white_im, HSI_matrix, max_H[0][0], WHITE, 60)
    #black_im.save("2balck_test.jpeg")
    white_im.save("2white_test.jpeg")
    wim = Img("2white_test.jpeg")
    wim.getRGBMatrix()
    print wim.getHSIMatrix()
    print colRate(wim.getHSIMatrix())
    print plotStat(matrix2data(HSI_matrix, 1))
