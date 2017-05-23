import numpy as np
from reading.user_item import User_Item
from reading.dataset_item import Dataset_Item
from typing import Dict


class User:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()  # type: Dict[Int, User_Item]
        self.dataset_by_hometown = dict()
        self.dataset_by_residence = dict()

        self.hometown_count = dict()
        self.residence_count = dict()
        self.user_count = dict()
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            userID, age, gender, education, marriageStatus, haveBaby, hometown, residence = tmp
            self.data[userID] = User_Item(userID, age, gender, education, marriageStatus, haveBaby, hometown, residence)
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record : Dataset_Item):
        userID = record.userID
        hometown = self.data[userID].hometown // 100
        residence = self.data[userID].residence // 100
        _day = record.clickTime // 10000
        label = record.label
        label = max(0, label)
        if hometown not in self.dataset_by_hometown:
            self.dataset_by_hometown[hometown] = list()
            self.hometown_count[hometown] = np.zeros([2, 32])
        if residence not in self.dataset_by_residence:
            self.dataset_by_residence[residence] = list()
            self.residence_count[residence] = np.zeros([2, 32])
        if userID not in self.user_count:
            self.user_count[userID] = np.zeros([2, 32])
        self.dataset_by_hometown[hometown].append(record)
        self.dataset_by_residence[residence].append(record)

        self.hometown_count[hometown][label][_day] += 1
        self.residence_count[residence][label][_day] += 1
        self.user_count[userID][label][_day] += 1

    def fresh(self):
        def push(f):
            for i in range(len(f)):
                for j in range(1, len(f[i])):
                    f[i][j] += f[i][j-1]

        for k in self.hometown_count:
            push(self.hometown_count[k])
        for k in self.residence_count:
            push(self.residence_count[k])
        for k in self.user_count:
            push(self.user_count[k])

    def get_dataset_by_hometown(self, hometown):
        return self.dataset_by_hometown[hometown // 100]

    def get_dataset_by_residence(self, residence):
        return self.dataset_by_residence[residence // 100]

    def get_user_count(self, userID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.user_count[userID][:, end_t - 1] - self.user_count[userID][:, from_t - 1])
        return self.user_count[userID][label, end_t - 1] - self.user_count[userID][label, from_t - 1]

    def get_hometown_count(self, hometown, label, from_t, end_t):
        hometown = hometown // 100
        if label == -1:
            return np.sum(self.hometown_count[hometown][:, end_t - 1] - self.hometown_count[hometown][:, from_t - 1])
        return self.hometown_count[hometown][label, end_t - 1] - self.hometown_count[hometown][label, from_t - 1]

    def get_residence_count(self, residence, label, from_t, end_t):
        residence = residence // 100
        if label == -1:
            return np.sum(self.residence_count[residence][:, end_t - 1] - self.residence_count[residence][:, from_t - 1])
        return self.residence_count[residence][label, end_t - 1] - self.residence_count[residence][label, from_t - 1]
