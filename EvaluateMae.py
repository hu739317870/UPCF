# -*- coding: utf-8 -*-

from DivideData import DivideData
import os
import sys

class EvalueateMae(object):

    def __init__(self):
        self.test_set = {}
        self.prediction_rate_matrix ={}

    def generate_data_matrix(self, test_set_file, prediction_rate_file):
        for line in DivideData.loadfile(test_set_file):
            user, movie, rate, _ = line.split('::')
            self.test_set.setdefault(user, {})
            self.test_set[user][movie] = float(rate)
        for line in DivideData.loadfile(prediction_rate_file):
            user, movie, rate = line.split('::')
            self.prediction_rate_matrix.setdefault(user, {})
            self.prediction_rate_matrix[user][movie] = float(rate)

    def compute_MAE(self):
        fen_zi = 0
        fen_mu = float(0)
        for user in self.prediction_rate_matrix:
            for movie in self.prediction_rate_matrix[user]:
                fen_zi += abs(self.prediction_rate_matrix[user][movie] - self.test_set[user][movie])
                fen_mu += 1
        mae = fen_zi / fen_mu
        print >> sys.stderr, '%s' % mae

if __name__ == '__main__':
    prediction_rate_file = os.path.join('ml-1m', 'dfs_prediction_rate_pcc.csv')
    test_set_file = os.path.join('ml-1m', 'test_set.csv')
    er = EvalueateMae()
    er.generate_data_matrix(test_set_file, prediction_rate_file)
    er.compute_MAE()
