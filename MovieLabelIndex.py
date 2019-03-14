# -*- coding: utf-8 -*-

import sys
import csv
import os

class GenerateMovieLabelIndex(object):

    def __init__(self):
        self.movie_label_number_matrix = {}
        self.user_info_matrix = {}
        self.rate_matrix = {}
        self.movie_label_index_matrix = {}
        self.label = ['M', 'F', 'Tee', 'Adu', 'Mat', 'Old', 'Tec', 'Rec', 'Ope', 'Obj', 'Else']

    def generate_user_info_matrix(self, new_user_info_file):
        for line in self.loadfile(new_user_info_file):
            uid, gender, age, occupation = line.split('::')
            self.user_info_matrix.setdefault(uid, {})
            self.user_info_matrix[uid] = [gender, age, occupation]
        print >> sys.stderr, '生成用户信息矩阵成功'

    def generate_rate_matrix(self, rating_file):
        for line in self.loadfile(rating_file):
            user, movie, rate, _ = line.split('::')
            self.rate_matrix.setdefault(movie, {})
            self.rate_matrix[movie][user] = float(rate)
        print >> sys.stderr, '生成评分矩阵成功'

    def count_up_one_label_number(self, label):
        for movie in self.rate_matrix:
            self.movie_label_number_matrix.setdefault(movie, {})
            for user in self.rate_matrix[movie]:
                if label in self.user_info_matrix[user]:
                    self.movie_label_number_matrix[movie].setdefault(label, 0)
                    self.movie_label_number_matrix[movie][label] += 1

    def generate_movie_label_number(self):
        for label in self.label:
            self.count_up_one_label_number(label)
        print >> sys.stderr, '统计每部电影各标签数成功'

        movie_label_number = self.transform_data_structure(self.movie_label_number_matrix)
        self.export_file('ml-1m/movie_label_number.csv', movie_label_number)
        print >> sys.stderr, '导出每部电影的标签数成功'

    def compute_one_movie_label_index(self, movie):
        gender, age, occupation = float(0), float(0), float(0)
        for label in self.movie_label_number_matrix[movie]:
            if label in ['F', 'M']:
                gender += self.movie_label_number_matrix[movie][label]
            elif label in ['Tee', 'Adu', 'Mat', 'Old']:
                age += self.movie_label_number_matrix[movie][label]
            else:
                occupation += self.movie_label_number_matrix[movie][label]

        self.movie_label_index_matrix.setdefault(movie, {})
        for label in self.label:
            if label in self.movie_label_number_matrix[movie] and label in ['F', 'M']:
                self.movie_label_index_matrix[movie][label] = self.movie_label_number_matrix[movie][label] / gender
            elif label in self.movie_label_number_matrix[movie] and label in ['Tee', 'Adu', 'Mat', 'Old']:
                self.movie_label_index_matrix[movie][label] = self.movie_label_number_matrix[movie][label] / age
            elif label in self.movie_label_number_matrix[movie] and label in ['Tec', 'Rec', 'Ope', 'Obj', 'Else']:
                self.movie_label_index_matrix[movie][label] = self.movie_label_number_matrix[movie][label] / occupation
            else:
                self.movie_label_index_matrix[movie][label] = 0

    def generate_movie_label_index(self):
        '''
        :return: 电影-标签 指数矩阵
        '''
        for movie in self.movie_label_number_matrix:
            self.compute_one_movie_label_index(movie)
        print >> sys.stderr, '计算每部电影的标签指数完成'
        return self.movie_label_index_matrix

    def export_movie_label_index_matrix(self):
        movie_label_index = self.transform_data_structure(self.movie_label_index_matrix)
        self.export_file('ml-1m/movie_label_index.csv', movie_label_index)
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

    def transform_data_structure(self, data):
        data_set = []
        for movie in data:
            for label in data[movie]:
                line = '%s::%s::%s' % (movie, label, data[movie][label])
                data_set.append(line)
        return data_set

if __name__ == '__main__':
    user_info_file = os.path.join('ml-1m', 'new_users.csv')
    rate_file = os.path.join('ml-1m', 'train_set.csv')
    user_profile = GenerateMovieLabelIndex()
    user_profile.generate_user_info_matrix(user_info_file)
    user_profile.generate_rate_matrix(rate_file)
    user_profile.generate_movie_label_number()
    user_profile.generate_movie_label_index()
    user_profile.export_movie_label_index_matrix()