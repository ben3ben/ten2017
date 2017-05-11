class Position:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()
        self.dataset_pos = dict()
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
        if positionID not in self.dataset_pos:
            self.dataset_pos[positionID] = list()
        self.dataset_pos[positionID].append(record)

    def get_dataset(self, positionID):
        return self.dataset_pos[positionID]
