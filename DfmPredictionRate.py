# -*- coding: utf-8 -*-

import sys
import os
from DivideData import DivideData
from operator import itemgetter

class DfsPredictionRate(object):

    def __init__(self):
        self.train_set = {}
        self.test_set = {}
        self.sim_matrix = {}
        self.average_matrix = {}
        self.prediction_rate_matrix = {}

    def generate_data_matrix(self, train_set_file, test_set_file, sim_file):
        for line in DivideData.loadfile(train_set_file):
            user, movie, rate, _ = line.split('::')
            self.train_set.setdefault(user, {})
            self.train_set[user][movie] = float(rate)
        for line in DivideData.loadfile(test_set_file):
            user, movie, rate, _ = line.split('::')
            self.test_set.setdefault(user, {})
            self.test_set[user][movie] = float(rate)
        for line in DivideData.loadfile(sim_file):
            forward_user, backward_user, sim = line.split('::')
            self.sim_matrix.setdefault(forward_user, {})
            self.sim_matrix[forward_user][backward_user] = float(sim)

    def generate_average_matrix(self):
        for user in self.train_set:
            for movie, rate in self.train_set[user].iteritems():
                self.average_matrix.setdefault(user, 0)
                self.average_matrix[user] += rate / len(self.train_set[user])

    def dfs_prediction_one_user_rate(self, target_user, target_item, n=150):
        fen_zi, fen_mu = float(0), float(0)
        for user, sim in sorted(self.sim_matrix[target_user].iteritems(), key=itemgetter(1), reverse=True)[:n]:
            if target_item in self.train_set[user]:
                fen_zi += (self.train_set[user][target_item] - self.average_matrix[user]) * self.sim_matrix[target_user][user]
                fen_mu += self.sim_matrix[target_user][user]
        if fen_mu == 0:
            return 0
        else:
            return fen_zi / fen_mu

    def dfs_prediction(self):
        for user in self.test_set:
            for movie in self.test_set[user]:
                self.prediction_rate_matrix.setdefault(user, {})
                self.prediction_rate_matrix[user][movie] = self.average_matrix[user] + self.dfs_prediction_one_user_rate(user, movie)
                if self.prediction_rate_matrix[user][movie] > 5:
                    self.prediction_rate_matrix[user][movie] = 5
        print >> sys.stderr, '预测评分成功'

        Prediction_rate_matrix = DivideData.transform_data_structure(self.prediction_rate_matrix)
        DivideData.export_file('ml-1m/prediction_rate_cos_upsim_dfm.csv', Prediction_rate_matrix)
        '''
        更改相似度文件后，记得更改导出的文件名
        '''
        print >> sys.stderr, '导出预测评分数据成功'

if __name__ == '__main__':
    train_set_file = os.path.join('ml-1m', 'train_set.csv')
    test_set_file = os.path.join('ml-1m', 'test_set.csv')
    sim_file = os.path.join('ml-1m', 'COS_UPsim.csv')
    '''
    通过换不同的相似度文件，实现不同相似度算法进行的评分预测
    '''
    dfspr = DfsPredictionRate()
    dfspr.generate_data_matrix(train_set_file, test_set_file, sim_file)
    dfspr.generate_average_matrix()
    dfspr.dfs_prediction()