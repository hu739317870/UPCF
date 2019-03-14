# -*- coding: utf-8 -*-

import sys
import math
import os
from DivideData import DivideData

class GenerateADCOSUPsim(object):

    def __init__(self):
        self.user_profile = {}
        self.ADCOS_UPsim = {}
        self.average_label = {}

    def generate_user_profile(self, user_profile_file):
        for line in DivideData.loadfile(user_profile_file):
            user, label, feature_value = line.split('::')
            self.user_profile.setdefault(user, {})
            self.user_profile[user][label] = float(feature_value)

    def compute_average_label(self):
        for user in self.user_profile:
            for label in self.user_profile[user]:
                self.average_label.setdefault(label, 0)
                self.average_label[label] += float(self.user_profile[user][label]) / len(self.user_profile)

    def compute_one_user_ADCOS_UPsim(self, one_user):
        for user in self.user_profile:
            fen_zi, fen_mu1, fen_mu2 = 0, 0, 0
            if user != one_user:
                for label in self.user_profile[user]:
                    fen_zi += (self.user_profile[one_user][label] - self.average_label[label]) * \
                              (self.user_profile[user][label] - self.average_label[label])
                    fen_mu1 += math.pow(self.user_profile[one_user][label] - self.average_label[label], 2)
                    fen_mu2 += math.pow(self.user_profile[user][label] - self.average_label[label], 2)
            else:
                continue
            self.ADCOS_UPsim.setdefault(one_user, {})
            self.ADCOS_UPsim[one_user][user] = fen_zi / (math.sqrt(fen_mu1) * math.sqrt(fen_mu2))

    def generate_ADCOS_UPsim(self):
        for user in self.user_profile:
            self.compute_one_user_ADCOS_UPsim(user)
        print >> sys.stderr, '计算 ADCOS_UPsim 成功'

        ADCOS_UPsim_matrix = DivideData.transform_data_structure(self.ADCOS_UPsim)
        DivideData.export_file('ml-1m/ADCOS_UPsim.csv', ADCOS_UPsim_matrix)
        print >> sys.stderr, '导出 ADCOS_UPsim 成功'

if __name__ == '__main__':
    user_profile_file = os.path.join('ml-1m', 'user_profile.csv')
    adcosupsim = GenerateADCOSUPsim()
    adcosupsim.generate_user_profile(user_profile_file)
    adcosupsim.compute_average_label()
    adcosupsim.generate_ADCOS_UPsim()