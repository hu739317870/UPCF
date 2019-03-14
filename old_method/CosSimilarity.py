# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GenerateCOSsim(object):

    def __init__(self):
        self.rate_matrix = {}
        self.COS_sim = {}

    def generate_rate_matrix(self, rate_file):
        for line in DivideData.loadfile(rate_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(user, {})
            self.rate_matrix[user][movie] = float(rate)

    def compute_one_user_COS_sim(self, one_user):
        for user in self.rate_matrix:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for movie in self.rate_matrix[one_user]:
                    if movie in self.rate_matrix[user]:
                        fen_zi += self.rate_matrix[one_user][movie] * self.rate_matrix[user][movie]
                        fen_mu1 += math.pow(self.rate_matrix[one_user][movie], 2)
                        fen_mu2 += math.pow(self.rate_matrix[user][movie], 2)
            else:
                continue
            self.COS_sim.setdefault(one_user, {})
            if fen_mu2 != 0 and fen_mu1 != 0:
                self.COS_sim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))
            else:
                self.COS_sim[one_user][user] = 0

    def generate_COS_sim(self):
        for user in self.rate_matrix:
            self.compute_one_user_COS_sim(user)
        print >> sys.stderr, '计算 COS_sim 成功'

        COS_UPsim_matrix = DivideData.transform_data_structure(self.COS_sim)
        DivideData.export_file('ml-1m/COS_sim.csv', COS_UPsim_matrix)
        print >> sys.stderr, '导出 COS_sim 成功'

if __name__ == '__main__':
    rate_file = os.path.join('ml-1m', 'train_set.csv')
    cosupsim = GenerateCOSsim()
    cosupsim.generate_rate_matrix(rate_file)
    cosupsim.generate_COS_sim()