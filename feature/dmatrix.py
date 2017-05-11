import numpy as np
from reading.dataset import Dataset
from feature_role.user_role import User_Role
from feature_role.dataset_role import Dataset_Role
from feature_role.position_role import Position_Role

class DMatrix:
    def __init__(self, user, train, position):
        self.user = user
        self.train = train  # type: Dataset
        self.roles = [User_Role(user), Dataset_Role(train), Position_Role(position)]

    def run(self, begin_t, end_t):
        train_list = self.train.get_data_list()
        instanceIDs = list()
        labels = list()
        features = list()
        for index, record in enumerate(train_list):
            if record['clickTime'] < begin_t or record['clickTime'] >= end_t:
                continue
            param = {'userID': record['userID'],
                     'positionID': record['positionID'],
                     'clickTime': record['clickTime'],
                     'connectionType': record['connectionType'],
                     'telecomsOperator': record['telecomsOperator'],
                     'clickDay': record['clickTime'] // 10000 * 10000,
                     'userid_dlist': self.train.get_value_by_user_id(record['userID'])}
            feas = [role.run(param) for role in self.roles]
            labels.append(record['label'])
            if 'instanceID' in record:
                instanceIDs.append(record['instanceID'])
            features.append(np.concatenate(feas))
        result = {'instanceIDs': np.array(instanceIDs),
                  'labels': np.array(labels),
                  'features': np.array(features),
                  'feature_names': np.concatenate([role.get_fea_names() for role in self.roles])}
        return result

