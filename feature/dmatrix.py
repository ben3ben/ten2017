import numpy as np
from reading.dataset import Dataset
from reading.advertisement import Advertisement
from reading.app import App
from reading.user import User
from feature_role.user_role import User_Role
from feature_role.dataset_role import Dataset_Role
from feature_role.position_role import Position_Role
from feature_role.advertisement_role import Advertisement_Role
from feature_role.app_role import App_Role
from feature_role.app_actions_role import App_Actions_Role
from feature_role.combine_corr import Combine_Corr

class DMatrix:
    def __init__(self, user, train, position, ad, app, acc_actions):
        self.user = user
        self.train = train  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.app = app # type: App
        self.user = user # type: User
        self.roles = [User_Role(user), Dataset_Role(train, ad), Position_Role(train, position),
                      Advertisement_Role(train, ad), App_Role(app), App_Actions_Role(acc_actions),
                      Combine_Corr(train, user, ad)]

    def run(self, begin_t, end_t, mode):
        train_list = self.train.get_data_list()
        instanceIDs = list()
        labels = list()
        features = list()
        for index, record in enumerate(train_list):
            if record['clickTime'] < begin_t or record['clickTime'] >= end_t:
                continue
            _ad = self.ad.get_value(record['creativeID'])
            _app = self.app.get_value(_ad['appID'])
            _user = self.user.get_value(record['userID'])
            param = {'userID': record['userID'],
                     'positionID': record['positionID'],
                     'creativeID': record['creativeID'],
                     'adID': _ad['adID'],
                     'camgaignID': _ad['camgaignID'],
                     'advertiserID': _ad['advertiserID'],
                     'appPlatform': _ad['appPlatform'],
                     'appID': _ad['appID'],
                     'appCategory': _app['appCategory'],
                     'clickTime': record['clickTime'],
                     'connectionType': record['connectionType'],
                     'telecomsOperator': record['telecomsOperator'],
                     'haveBaby': _user['haveBaby'],
                     'clickDay': record['clickTime'] // 10000 * 10000,
                     'userid_dlist': self.train.get_value_by_user_id(record['userID']),
                     'mode': mode}
            feas = [role.run(param) for role in self.roles]
            labels.append(record['label'])
            if 'instanceID' in record:
                instanceIDs.append(record['instanceID'])
            else:
                instanceIDs.append(index)
            features.append(np.concatenate(feas))
        result = {'instanceIDs': np.array(instanceIDs),
                  'labels': np.array(labels),
                  'features': np.array(features),
                  'feature_names': np.concatenate([role.get_fea_names() for role in self.roles])}
        return result
