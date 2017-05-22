import numpy as np

class Position:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()
        self.dataset_pos = dict()
        self.position_count = dict()
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            positionID, sitesetID, positionType = tmp
            self.data[positionID] = {'positionID': positionID,
                                     'sitesetID': sitesetID,
                                     'positionType': positionType}
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record):
        positionID = record['positionID']
        _day = record['clickTime'] // 10000
        label = record['label']
        label = max(0, label)
        if positionID not in self.dataset_pos:
            self.dataset_pos[positionID] = list()
            self.position_count[positionID] = np.zeros([2, 32])
        self.dataset_pos[positionID].append(record)
        self.position_count[positionID][label][_day] += 1

    def fresh(self):
        def push(f):
            for i in range(len(f)):
                for j in range(1, len(f[i])):
                    f[i][j] += f[i][j-1]

        for k in self.position_count:
            push(self.position_count[k])

    def get_dataset(self, positionID):
        return self.dataset_pos[positionID]

    def get_position_count(self, positionID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.position_count[positionID][:, end_t - 1] - self.position_count[positionID][:, from_t - 1])
        return self.position_count[positionID][label, end_t - 1] - self.position_count[positionID][label, from_t - 1]
