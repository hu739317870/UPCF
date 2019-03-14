# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GeneratePCCsim(object):

    def __init__(self):
        self.rate_matrix = {}
        self.PCC_sim = {}
        self.average_user = {}

    def generate_rate_matrix(self, rate_file):
        for line in DivideData.loadfile(rate_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(user, {})
            self.rate_matrix[user][movie] = float(rate)

    def compute_average_user(self):
        for user in self.rate_matrix:
            for movie in self.rate_matrix[user]:
                self.average_user.setdefault(user, 0)
                self.average_user[user] += float(self.rate_matrix[user][movie]) / len(self.rate_matrix[user])

    def compute_one_user_PCC_sim(self, one_user):
        for user in self.rate_matrix:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for movie in self.rate_matrix[one_user]:
                    if movie in self.rate_matrix[user]:
                        fen_zi += (self.rate_matrix[one_user][movie] - self.average_user[one_user]) * \
                                  (self.rate_matrix[user][movie] - self.average_user[user])
                        fen_mu1 += math.pow(self.rate_matrix[one_user][movie] - self.average_user[one_user], 2)
                        fen_mu2 += math.pow(self.rate_matrix[user][movie] - self.average_user[user], 2)
            else:
                continue
            self.PCC_sim.setdefault(one_user, {})
            if fen_mu2 != 0 and fen_mu1 != 0:
                self.PCC_sim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))
            else:
                self.PCC_sim[one_user][user] = 0

    def generate_PCC_sim(self):
        for user in self.rate_matrix:
            self.compute_one_user_PCC_sim(user)
        print >> sys.stderr, '计算 PCC_sim 成功'

        PCC_sim_matrix = DivideData.transform_data_structure(self.PCC_sim)
        DivideData.export_file('ml-1m/PCC_sim.csv', PCC_sim_matrix)
        print >> sys.stderr, '导出 PCC_sim 成功'

if __name__ == '__main__':
    rate_file = os.path.join('ml-1m', 'train_set.csv')
    pccsim = GeneratePCCsim()
    pccsim.generate_rate_matrix(rate_file)
    pccsim.compute_average_user()
    pccsim.generate_PCC_sim()