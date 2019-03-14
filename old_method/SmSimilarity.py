# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GenerateSMsim(object):

    def __init__(self):
        self.rate_matrix = {}
        self.SM_sim = {}
        self.s_p = {}
        self.s_n = {}
        self.transform_rate_matrix = {}

    def generate_rate_matrix(self, rate_file):
        for line in DivideData.loadfile(rate_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(user, {})
            self.rate_matrix[user][movie] = float(rate)

    def generate_transform_rate_matrix(self):
        for user in self.rate_matrix:
            for movie in self.rate_matrix[user]:
                self.transform_rate_matrix.setdefault(movie, {})
                self.transform_rate_matrix[movie][user] = self.rate_matrix[user][movie]

    def compute_singularities(self):
        count_p = 0
        count_n = 0
        for movie, users in self.transform_rate_matrix.iteritems():
            for user, rate in users.iteritems():
                if rate == 5:
                    count_p += 1
                else:
                    count_n += 1
            self.s_p.setdefault(movie, 0)
            self.s_p[movie] = 1 - (count_p / len(self.transform_rate_matrix[movie]))
            self.s_n.setdefault(movie, 0)
            self.s_n[movie] = 1 - (count_n / len(self.transform_rate_matrix[movie]))

    def compute_one_user_SM_sim(self, one_user):
        for user in self.rate_matrix:
            count1, count2, count3 = 0, 0, 0
            sum1, sum2, sum3 = 0, 0, 0
            if user != one_user:
                for movie in self.rate_matrix[one_user]:
                    if movie in self.rate_matrix[user]:
                        if self.rate_matrix[one_user][movie] >= 4 and self.rate_matrix[user][movie] >= 4:
                            sum1 += (1 - pow(self.rate_matrix[one_user][movie] / 5 - self.rate_matrix[user][movie] / 5, 2)) * self.s_p[movie] * \
                                    self.s_p[movie]
                            count1 += 1
                        elif self.rate_matrix[one_user][movie] < 4 and self.rate_matrix[user][movie] < 4:
                            sum2 += (1 - pow(self.rate_matrix[one_user][movie] / 5 - self.rate_matrix[user][movie] / 5, 2)) * self.s_n[movie] * \
                                    self.s_n[movie]
                            count2 += 1
                        else:
                            sum3 += (1 - pow(self.rate_matrix[one_user][movie] / 5 - self.rate_matrix[user][movie] / 5, 2)) * self.s_p[movie] * \
                                    self.s_n[movie]
                            count3 += 1
                if count1 == 0: count1 = 1
                if count2 == 0: count2 = 1
                if count3 == 0: count3 = 1
                sim = ((sum1 / count1) + (sum2 / count2) + (sum3 / count3)) / 3
                self.SM_sim.setdefault(one_user, {})
                self.SM_sim[one_user][user] = sim

    def generate_SM_sim(self):
        for user in self.rate_matrix:
            self.compute_one_user_SM_sim(user)
        print >> sys.stderr, '计算 SM_sim 成功'

        SM_sim_matrix = DivideData.transform_data_structure(self.SM_sim)
        DivideData.export_file('ml-1m/SM_sim.csv', SM_sim_matrix)
        print >> sys.stderr, '导出 SM_sim 成功'

if __name__ == '__main__':
    rate_file = os.path.join('ml-1m', 'train_set.csv')
    smsim = GenerateSMsim()
    smsim.generate_rate_matrix(rate_file)
    smsim.generate_transform_rate_matrix()
    smsim.compute_singularities()
    smsim.generate_SM_sim()