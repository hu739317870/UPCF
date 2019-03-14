# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GeneratePCCUPsim(object):

    def __init__(self):
        self.user_profile = {}
        self.PCC_UPsim = {}
        self.average_user = {}

    def generate_user_profile(self, user_profile_file):
        for line in DivideData.loadfile(user_profile_file):
            user, label, feature_value = line.split('::')
            self.user_profile.setdefault(user, {})
            self.user_profile[user][label] = float(feature_value)

    def compute_average_user(self):
        for user in self.user_profile:
            for label in self.user_profile[user]:
                self.average_user.setdefault(user, 0)
                self.average_user[user] += float(self.user_profile[user][label]) / 11

    def compute_one_user_PCC_UPsim(self, one_user):
        for user in self.user_profile:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for label in self.user_profile[user]:
                    fen_zi += (self.user_profile[one_user][label] - self.average_user[one_user]) * \
                              (self.user_profile[user][label] - self.average_user[user])
                    fen_mu1 += math.pow(self.user_profile[one_user][label] - self.average_user[one_user], 2)
                    fen_mu2 += math.pow(self.user_profile[user][label] - self.average_user[user], 2)
            else:
                continue
            self.PCC_UPsim.setdefault(one_user, {})
            self.PCC_UPsim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))

    def generate_PCC_UPsim(self):
        for user in self.user_profile:
            self.compute_one_user_PCC_UPsim(user)
        print >> sys.stderr, '计算 PCC_UPsim 成功'

        PCC_UPsim_matrix = DivideData.transform_data_structure(self.PCC_UPsim)
        DivideData.export_file('ml-1m/PCC_UPsim.csv', PCC_UPsim_matrix)
        print >> sys.stderr, '导出 PCC_UPsim 成功'

if __name__ == '__main__':
    user_profile_file = os.path.join('ml-1m', 'user_profile.csv')
    pccupsim = GeneratePCCUPsim()
    pccupsim.generate_user_profile(user_profile_file)
    pccupsim.compute_average_user()
    pccupsim.generate_PCC_UPsim()