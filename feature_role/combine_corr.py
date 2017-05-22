from reading.dataset import Dataset
from reading.advertisement import Advertisement
from reading.user import User
from reading.app import App
from conf.configure import Configure
import numpy as np
import math


class Combine_Corr:
    flag = False
    fea_names = list()

    def __init__(self, data_set, user, ad, app):
        self.data_set = data_set  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.user = user # type: User
        self.app = app # type: App
        self.app_baby_corr = self.read_app_baby_corr()
        self.cate_baby_corr = self.read_cate_baby_corr()
        self.cate_time_corr = self.read_cate_time_corr()
        self.fea_set = dict()

    def read_app_baby_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            userID = d['userID']
            clickTime = d['clickTime']
            baby = self.user.get_value(userID)['haveBaby']
            creativeID = d['creativeID']
            appID = self.ad.get_value(creativeID)['appID']
            label = d['label']
            if label < 0:
                continue
            if appID not in result:
                result[appID] = np.zeros([7, 31, 2])
            result[appID][baby][clickTime // 10000][label] += 1
        return result

    def read_cate_baby_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            userID = d['userID']
            clickTime = d['clickTime']
            baby = self.user.get_value(userID)['haveBaby']
            creativeID = d['creativeID']
            appID = self.ad.get_value(creativeID)['appID']
            appCategory = self.app.get_value(appID)['appCategory']
            label = d['label']
            if label < 0:
                continue
            if appCategory not in result:
                result[appCategory] = np.zeros([7, 31, 2])
            result[appCategory][baby][clickTime // 10000][label] += 1
        return result

    def read_cate_time_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            creativeID = d['creativeID']
            appID = self.ad.get_value(creativeID)['appID']
            appCategory = self.app.get_value(appID)['appCategory']
            hour = d['clickTime'] // 100 % 100
            day = d['clickTime'] // 10000
            label = d['label']
            if label < 0:
                continue
            if appCategory not in result:
                result[appCategory] = np.zeros([24, 31, 2])
            result[appCategory][hour][day][label] += 1
        return result

    def corr_to_vec(self, dlist, cond, clickDay, tw):
        result = list()
        _clickDay = clickDay - tw
        if _clickDay < 0:
            _clickDay = 0
        _clickDay = _clickDay // 10000
        clickDay = clickDay // 10000
        _sum = np.sum(dlist[cond, _clickDay:clickDay])
        _sum_1 = np.sum(dlist[cond, _clickDay:clickDay, 1])
        _sum_all_cond = np.sum(dlist[:, _clickDay:clickDay])
        _sum_one_cond = np.sum(dlist[cond, _clickDay:clickDay])
        result.append(_sum_1 / _sum if _sum_1 > 0 else 0)
        result.append(_sum_one_cond / _sum_all_cond if _sum_one_cond > 0 else 0)
        return result

    def app_baby_to_vec(self, appID, baby, clickDay, tw):
        return self.corr_to_vec(self.app_baby_corr[appID], baby, clickDay, tw)

    def cate_baby_to_vec(self, appCategory, baby, clickDay, tw):
        return self.corr_to_vec(self.cate_baby_corr[appCategory], baby, clickDay, tw)

    def cate_time_to_vec(self, appCategory, hour, clickDay, tw):
        return self.corr_to_vec(self.cate_time_corr[appCategory], hour, clickDay, tw)

    def cos_similarity(self, a, b):
        len_a = math.sqrt(sum(a ** 2))
        len_b = math.sqrt(sum(b ** 2))
        return sum(a * b) / (len_a * len_b) if len_a * len_b > 0 else -1e-5

    def cate_hour_user_similarity(self, appCategory, user_id, clickDay, tw):
        _day = clickDay // 10000
        _last_day = (clickDay - tw) // 10000
        cate = self.cate_time_corr[appCategory][:, _last_day : _day, :]
        cate = np.sum(cate, axis=2)
        cate = np.sum(cate, axis=1)
        cate = cate.reshape([-1])
        user_click = np.zeros([24])
        for d in self.data_set.get_value_by_user_id(user_id):
            if d['clickTime'] < clickDay - tw or d['clickTime'] >= clickDay:
                continue
            user_click[d['clickTime'] // 100 % 100] += 1
        return [self.cos_similarity(cate, user_click)]


    def get_fea_names(self):
        return Combine_Corr.fea_names

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not Combine_Corr.flag:
            for index in range(len(fea)):
                Combine_Corr.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        tw = [10000, 30000, 100000, 150000]
        appID = param['appID']
        userID = param['userID']
        haveBaby = param['haveBaby']
        clickDay = param['clickDay']
        clickTime = param['clickTime']
        appCategory = param['appCategory']
        for _tw in tw:
            result.extend(self.generate(self.app_baby_to_vec, 'app_baby_corr_{}'.format(_tw), True,
                                        appID, haveBaby, clickDay, _tw))
            result.extend(self.generate(self.cate_baby_to_vec, 'cate_baby_corr_{}'.format(_tw), True,
                                        appCategory, haveBaby, clickDay, _tw))
            result.extend(self.generate(self.cate_time_to_vec, 'cate_hour_corr_{}'.format(_tw), True,
                                        appCategory, clickTime // 100 % 100, clickDay, _tw))
            result.extend(self.generate(self.cate_hour_user_similarity, 'cate_hour_user_similarity_{}'.format(_tw), True,
                                        appCategory, userID, clickDay, _tw))

        Combine_Corr.flag = True
        return result
