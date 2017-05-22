import numpy as np
import pandas as pd
import math
from conf.configure import Configure

class Lda_Role:
    flag = False
    fea_names = list()

    def __init__(self):
        self.user_appid_topic_for_user = dict()
        self.user_appid_topic_for_appid = dict()
        self.read_user_appid_topic(Configure.user_appid_topic_for_user, Configure.user_appid_topic_for_appid)
        self.fea_set = dict()

    def get_fea_names(self):
        return Lda_Role.fea_names

    def read_user_appid_topic(self, path_user, path_appid):
        data = pd.read_csv(path_user, header=None)
        data = data.as_matrix()
        for line in data:
            self.user_appid_topic_for_user[int(line[0])] = line[1:]

        data = pd.read_csv(path_appid, header=None)
        data = data.as_matrix()
        for line in data:
            self.user_appid_topic_for_appid[line[0]] = line[1:]

    def get_vec(self, _dict, cond):
        if cond not in _dict:
            for key in _dict:
                _len = len(_dict[key])
                return np.zeros([_len])
        return _dict[cond]

    def cos_similarity(self, a, b):
        len_a = math.sqrt(sum(a ** 2))
        len_b = math.sqrt(sum(b ** 2))
        return sum(a * b) / (len_a * len_b) if len_a * len_b > 0 else -1

    def get_userid_appid_ver_for_user(self, userID):
        if userID not in self.user_appid_topic_for_user:
            for key in self.user_appid_topic_for_user:
                _len = len(self.user_appid_topic_for_user[key])
                return [-1] * _len
        return self.user_appid_topic_for_user[userID]

    def get_userid_appid_vec_for_app(self, appID):
        if appID not in self.user_appid_topic_for_appid:
            for key in self.user_appid_topic_for_appid:
                _len = len(self.user_appid_topic_for_appid[key])
                return [-1] * _len
        return self.user_appid_topic_for_appid[appID]

    def get_userid_appid_similarity(self, userID, appID):
        user_vec = self.get_vec(self.user_appid_topic_for_user, userID)
        app_vec = self.get_vec(self.user_appid_topic_for_appid, appID)
        return [self.cos_similarity(user_vec, app_vec)]

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not Lda_Role.flag:
            for index in range(len(fea)):
                Lda_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        userID = param['userID']
        appID = param['appID']
        result.extend(self.generate(self.get_userid_appid_similarity, 'lda_userid_appid_similarity', True,
                                    userID, appID))
        result.extend(self.generate(self.get_userid_appid_ver_for_user, 'lda_userid_appid_ver_for_user', True,
                                    userID))
        # result.extend(self.generate(self.get_userid_appid_vec_for_app, 'lda_userid_appid_vec_for_app', True,
        #                             appID))
        Lda_Role.flag = True
        return result







