# -*- coding: utf-8 -*-

import sys
import csv
import os
from MovieLabelIndex import GenerateMovieLabelIndex

class GenerateUserProfile(object):

    def __init__(self):
        self.rate_matrix = {}
        self.user_profile = {}
        self.user_info_matrix = {}
        self.label = ['M', 'F', 'Tee', 'Adu', 'Mat', 'Old', 'Tec', 'Rec', 'Ope', 'Obj', 'Else']
        self.movie_label_index_matrix = {}

    def generate_user_info_matrix(self, new_user_info_file):
        for line in self.loadfile(new_user_info_file):
            uid, gender, age, occupation = line.split('::')
            self.user_info_matrix.setdefault(uid, {})
            self.user_info_matrix[uid] = [gender, age, occupation]
        print >> sys.stderr, '生成用户信息矩阵成功'

    def generate_data_matrix(self, rate_file, movie_label_index_file):
        for line in self.loadfile(rate_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(user, {})
            self.rate_matrix[user][movie] = float(rate)

        for line in self.loadfile(movie_label_index_file):
            movie, label, index = line.split('::')
            self.movie_label_index_matrix.setdefault(movie, {})
            self.movie_label_index_matrix[movie][label] = float(index)

    def generate_one_user_profile(self, user):
        for movie in self.rate_matrix[user]:
            for label in self.label:
                self.user_profile.setdefault(user, {})
                self.user_profile[user].setdefault(label, 0)
                self.user_profile[user][label] += (self.rate_matrix[user][movie] * self.movie_label_index_matrix[movie][label]) / len(self.rate_matrix[user])

    def generate_user_profile(self):
        for user in self.rate_matrix:
            if int(user) in range(100, 200):
                for label in self.label:
                    if label in self.user_info_matrix[user]:
                        self.user_profile.setdefault(user, {})
                        self.user_profile[user].setdefault(label, 0)
                        self.user_profile[user][label] = 1
                    else:
                        self.user_profile.setdefault(user, {})
                        self.user_profile[user].setdefault(label, 0)
                        self.user_profile[user][label] = 0
            else:
                self.generate_one_user_profile(user)

        print >> sys.stderr, '计算每位用户的特征画像完成'

        self.export_file('ml-1m/coldstart_user_profile', self.user_profile)
        print >> sys.stderr, '导出用户的特征画像完成'

    def export_user_profile(self):
        a = GenerateMovieLabelIndex()
        user_profile = a.transform_data_structure(self.user_profile)
        GenerateMovieLabelIndex.export_file('ml-1m/coldstart_user_profile.csv', user_profile)
        print >> sys.stderr, '导出每部电影的标签指数成功'

    @staticmethod
    def loadfile(filename):
        fp = open(filename, 'r')
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
            if i % 100000 == 0:
                print >> sys.stderr, '加载 %s(%s)' % (filename, i)
        fp.close()
        print >> sys.stderr, '加载 %s 成功' % filename

    @staticmethod
    def export_file(filename, data):
        with open(filename, "wb") as csvFile:
            csv_writer = csv.writer(csvFile)
            for line in data:
                csv_writer.writerow([line])
        csvFile.close()

if __name__ == '__main__':
    user_info_file = os.path.join('ml-1m', 'new_users.csv')
    rate_file = os.path.join('ml-1m', 'train_set.csv')
    movie_label_index_file = os.path.join('ml-1m', 'movie_label_index.csv')
    user = GenerateUserProfile()
    user.generate_user_info_matrix(user_info_file)
    user.generate_data_matrix(rate_file, movie_label_index_file)
    user.generate_user_profile()
    user.export_user_profile()