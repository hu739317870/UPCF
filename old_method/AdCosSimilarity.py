# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GenerateADCOSsim(object):

    def __init__(self):
        self.rate_matrix = {}
        self.ADCOS_sim = {}
        self.average_movie = {}

    def generate_rate_matrix(self, rate_file):
        for line in DivideData.loadfile(rate_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(user, {})
            self.rate_matrix[user][movie] = float(rate)

    def compute_average_movie(self):
        trans_matrix = {}
        for user in self.rate_matrix:
            for movie in self.rate_matrix[user]:
                trans_matrix.setdefault(movie, {})
                trans_matrix[movie][user] = float(self.rate_matrix[user][movie])

        for movie in trans_matrix:
            for user in trans_matrix[movie]:
                self.average_movie.setdefault(movie, 0)
                self.average_movie[movie] += float(trans_matrix[movie][user]) / len(trans_matrix[movie])

    def compute_one_user_ADCOS_sim(self, one_user):
        for user in self.rate_matrix:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for movie in self.rate_matrix[one_user]:
                    if movie in self.rate_matrix[user]:
                        fen_zi += (self.rate_matrix[one_user][movie] - self.average_movie[movie]) * \
                                  (self.rate_matrix[user][movie] - self.average_movie[movie])
                        fen_mu1 += math.pow(self.rate_matrix[one_user][movie] - self.average_movie[movie], 2)
                        fen_mu2 += math.pow(self.rate_matrix[user][movie] - self.average_movie[movie], 2)
            else:
                continue
            self.ADCOS_sim.setdefault(one_user, {})
            if fen_mu1 != 0 and fen_mu2 != 0:
                self.ADCOS_sim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))
            else:
                self.ADCOS_sim[one_user][user] = 0

    def generate_ADCOS_sim(self):
        for user in self.rate_matrix:
            self.compute_one_user_ADCOS_sim(user)
        print >> sys.stderr, '计算 ADCOS_sim 成功'

        ADCOS_UPsim_matrix = DivideData.transform_data_structure(self.ADCOS_sim)
        DivideData.export_file('ml-1m/ADCOS_sim.csv', ADCOS_UPsim_matrix)
        print >> sys.stderr, '导出 ADCOS_sim 成功'

if __name__ == '__main__':
    user_profile_file = os.path.join('ml-1m', 'train_set.csv')
    adcosupsim = GenerateADCOSsim()
    adcosupsim.generate_rate_matrix(user_profile_file)
    adcosupsim.compute_average_movie()
    adcosupsim.generate_ADCOS_sim()