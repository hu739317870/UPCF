# -*- coding: utf-8 -*-

import sys
import csv
import os


class GenerateNewUserInfo(object):

    def __init__(self):
        self.user_info = []

    def generate_new_user_info(self, filename):

        for line in self.loadfile(filename):
            uid, gender, age, occupation, _ = line.split('::')
            if age in ['1', '18']:
                self.age = 'Tee'
            elif age in ['25', '35']:
                self.age = 'Adu'
            elif age in ['45', '50']:
                self.age = 'Mat'
            else:
                self.age = 'Old'

            if occupation in ['6', '11', '12', '17']:
                self.occupation = 'Tec'
            elif occupation in ['1', '2', '4', '15', '20']:
                self.occupation = 'Rec'
            elif occupation in ['3', '7', '16']:
                self.occupation = 'Ope'
            elif occupation in ['5', '8', '14', '18']:
                self.occupation = 'Obj'
            else:
                self.occupation = 'Else'

            user_info = '%s::%s::%s::%s' % (uid, gender, self.age, self.occupation)

            self.user_info.append(user_info)

        self.export_file('ml-1m/new_users.csv', self.user_info)

        print >> sys.stderr, '生成新用户信息表成功'

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
    user_file = os.path.join('ml-1m', 'users.dat')
    user = GenerateNewUserInfo()
    user.generate_new_user_info(user_file)