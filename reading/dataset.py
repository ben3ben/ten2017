from reading.position import Position


class Dataset:
    def __init__(self, train_path, test_path, debug=False):
        self.debug = debug
        self.data_list = list()
        self.data_by_userid = dict()
        self.read(train_path)
        self.read(test_path)

    '''
        train: label,clickTime,conversionTime,creativeID,userID,positionID,connectionType,telecomsOperator
        test: instanceID,label,clickTime,creativeID,userID,positionID,connectionType,telecomsOperator
    '''

    def read(self, path):
        fin = open(path)
        headers = fin.readline().strip().split(',')
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) if v != '' else -1 for v in line.strip().split(',')]
            d = dict(zip(headers, tmp))
            if len(self.data_list) > 0 and d['clickTime'] < self.data_list[-1]['clickTime']:
                print('dataset not sort at all')
            self.data_list.append(d)
            if d['userID'] not in self.data_by_userid:
                self.data_by_userid[d['userID']] = list()
            self.data_by_userid[d['userID']].append(d)
        fin.close()

    def add_to_position(self, position: Position):
        for record in self.data_list:
            position.add_dataset(record)

    def get_data_list(self):
        return self.data_list

    def get_keys_by_user_id(self):
        return list(self.data_by_userid.keys())

    def get_value_by_user_id(self, key):
        return self.data_by_userid[key]

    def exists_in_user_id(self, key):
        return key in self.data_by_userid
