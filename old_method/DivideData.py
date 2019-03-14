# -*- coding: utf-8 -*-

import sys
import random
import csv
import os


class DivideData(object):

    def __init__(self):
        self.trainset = []
        self.testset = []

    def generate_data_set(self, filename, pivot=0.8):
        a, b = 0, 0
        for line in self.loadfile(filename):
            if random.random() < pivot:
                self.trainset.append(line)
                a += 1
            else:
                self.testset.append(line)
                b += 1

        print >> sys.stderr, '划分训练集、测试集成功'
        print >> sys.stderr, '训练集 %s' % a
        print >> sys.stderr, '测试集 %s' % b

        self.export_file('ml-1m/train_set.csv', self.trainset)
        self.export_file('ml-1m/test_set.csv', self.testset)
        print >> sys.stderr, '导出文件成功'

    @staticmethod
    def loadfile(filename):
        fp = open(filename, 'r')
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
            if i % 100000 == 0:
                print >> sys.stderr, '加载 %s(%s)' % (filename, i)
        fp.close()
        print >> sys.stderr, '加载 %s 成功' % filename

    @staticmethod
    def export_file(filename, data):
        with open(filename, "wb") as csvFile:
            csv_writer = csv.writer(csvFile)
            for line in data:
                csv_writer.writerow([line])
        csvFile.close()

    @staticmethod
    def transform_data_structure(data):
        data_set = []
        for movie in data:
            for label in data[movie]:
                line = '%s::%s::%s' % (movie, label, data[movie][label])
                data_set.append(line)
        return data_set

if __name__ == '__main__':
    rating_file = os.path.join('ml-1m', 'ratings.dat')
    dd = DivideData()
    dd.generate_data_set(rating_file)