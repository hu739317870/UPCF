# -*- coding: utf-8 -*-

import sys
import os
import csv
from DivideData import DivideData
from operator import itemgetter

class EvaluatePRinDifferentN(object):

    def __init__(self):
        self.train_set = {}
        self.test_set = {}
        self.prediction_rate_matrix = {}
        self.number_matrix = {}

    def generate_data_matrix(self, train_set_file, test_set_file, prediction_rate_file):
        for line in DivideData.loadfile(train_set_file):
            user, movie, rate, _ = line.split('::')
            self.train_set.setdefault(user, {})
            self.train_set[user][movie] = float(rate)
        for line in DivideData.loadfile(test_set_file):
            user, movie, rate, _ = line.split('::')
            self.test_set.setdefault(user, {})
            self.test_set[user][movie] = float(rate)
        for line in DivideData.loadfile(prediction_rate_file):
            user, movie, prediction_rate = line.split('::')
            self.prediction_rate_matrix.setdefault(user, {})
            self.prediction_rate_matrix[user][movie] = float(prediction_rate)

    def generate_number_matrix(self):
        for user in self.test_set:
            for movie, rate in self.test_set[user].iteritems():
                self.number_matrix.setdefault(user, 0)
                if rate >= 4:
                    self.number_matrix[user] += 1

    def evaluate_PR_in_different_n(self, n=2):
        mae_list = []
        while n <= 20:
            p, r = 0, 0
            for user in self.test_set:
                if int(user) in range(100, 200):
                    count_rs = float(0)
                    for movie, prediction_rate in sorted(self.prediction_rate_matrix[user].iteritems(),
                                                         key=itemgetter(1),
                                                         reverse=True)[:n]:
                        if self.test_set[user][movie] >= 4:
                            count_rs += 1
                    p += (count_rs / n)
                    if self.number_matrix[user] == 0:
                        r += 0
                    else:
                        r += (count_rs / self.number_matrix[user])
            p = p / 100
            r = r / 100
            a = [n, p, r]
            mae_list.append(a)
            print >> sys.stderr, 'n = %s 时的 p = %f, r = %f ' % (n, p, r)
            n += 1
        self.export_file('ml-1m/coldstart_pr_cosup_dfm.csv', mae_list)

    def export_file(self, filename, data):
        with open(filename, "wb") as csvFile:
            csv_writer = csv.writer(csvFile)
            for line in data:
                csv_writer.writerow(line)
        csvFile.close()

if __name__ == '__main__':
    train_set_file = os.path.join('ml-1m', 'train_set.csv')
    test_set_file = os.path.join('ml-1m', 'test_set.csv')
    sim_file = os.path.join('ml-1m', 'coldstart_prediction_rate.csv')
    '''
    通过换不同的相似度文件，实现不同相似度算法进行的评分预测
    '''
    epridn = EvaluatePRinDifferentN()
    epridn.generate_data_matrix(train_set_file, test_set_file, sim_file)
    epridn.generate_number_matrix()
    epridn.evaluate_PR_in_different_n()