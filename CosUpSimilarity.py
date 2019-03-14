# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GenerateCOSUPsim(object):

    def __init__(self):
        self.user_profile = {}
        self.COS_UPsim = {}

    def generate_user_profile(self, user_profile_file):
        for line in DivideData.loadfile(user_profile_file):
            user, label, feature_value = line.split('::')
            self.user_profile.setdefault(user, {})
            self.user_profile[user][label] = float(feature_value)

    def compute_one_user_COS_UPsim(self, one_user):
        for user in self.user_profile:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for label in self.user_profile[user]:
                    fen_zi += self.user_profile[one_user][label] * self.user_profile[user][label]
                    fen_mu1 += math.pow(self.user_profile[one_user][label], 2)
                    fen_mu2 += math.pow(self.user_profile[user][label], 2)
            else:
                continue
            self.COS_UPsim.setdefault(one_user, {})
            self.COS_UPsim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))

    def generate_COS_UPsim(self):
        for user in self.user_profile:
            self.compute_one_user_COS_UPsim(user)
        print >> sys.stderr, '计算 COS_UPsim 成功'

        COS_UPsim_matrix = DivideData.transform_data_structure(self.COS_UPsim)
        DivideData.export_file('ml-1m/COS_UPsim.csv', COS_UPsim_matrix)
        print >> sys.stderr, '导出 COS_UPsim 成功'

if __name__ == '__main__':
    user_profile_file = os.path.join('ml-1m', 'user_profile.csv')
    cosupsim = GenerateCOSUPsim()
    cosupsim.generate_user_profile(user_profile_file)
    cosupsim.generate_COS_UPsim()