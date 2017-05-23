from reading.dataset import Dataset
from reading.advertisement import Advertisement
from reading.user import User
from reading.app import App
from reading.position import Position
from reading.user_app_actions import User_App_Actions
from conf.configure import Configure
import numpy as np
import math


class Combine_Corr:
    flag = False
    fea_names = list()

    def __init__(self, data_set, user, ad, app, position, app_actions):
        self.data_set = data_set  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.user = user # type: User
        self.app = app # type: App
        self.position = position # type: Position
        self.app_actions = app_actions # type: User_App_Actions
        self.app_baby_corr = self.read_app_baby_corr()
        self.cate_baby_corr = self.read_cate_baby_corr()
        self.cate_time_corr = self.read_cate_time_corr()
        self.cate_edu_corr, self.app_edu_corr, self.position_edu_corr = self.read_edu_corr()
        self.cate_edu_action, self.app_edu_action = self.read_edu_action_corr()
        self.cate_gender_corr, self.app_gender_corr, self.position_gender_corr = self.read_gender_corr()
        self.fea_set = dict()

    def read_gender_corr(self):
        cate_gender = dict()
        app_gender = dict()
        position_gender = dict()
        for d in self.data_set.get_data_list():
            if d.label < 0:
                continue
            day = d.clickTime // 10000
            userID = d.userID
            gender = self.user.get_value(userID).gender
            appID = self.ad.get_value(d.creativeID).appID
            cate = self.app.get_value(appID).appCategory
            positionID = d.positionID
            if cate not in cate_gender:
                cate_gender[cate] = np.zeros([3, 31, 2])
            if appID not in app_gender:
                app_gender[appID] = np.zeros([3, 31, 2])
            if positionID not in position_gender:
                position_gender[positionID] = np.zeros([3, 31, 2])
            cate_gender[cate][gender][day][d.label] += 1
            app_gender[appID][gender][day][d.label] += 1
            position_gender[positionID][gender][day][d.label] += 1
        return cate_gender, app_gender, position_gender

    def read_edu_corr(self):
        cate_edu = dict()
        app_edu = dict()
        position_edu = dict()
        for d in self.data_set.get_data_list():
            if d.label < 0:
                continue
            day = d.clickTime // 10000
            userID = d.userID
            education = self.user.get_value(userID).education
            appID = self.ad.get_value(d.creativeID).appID
            cate = self.app.get_value(appID).appCategory
            positionID = d.positionID
            if cate not in cate_edu:
                cate_edu[cate] = np.zeros([8, 31, 2])
            if appID not in app_edu:
                app_edu[appID] = np.zeros([8, 31, 2])
            if positionID not in position_edu:
                position_edu[positionID] = np.zeros([8, 31, 2])
            cate_edu[cate][education][day][d.label] += 1
            app_edu[appID][education][day][d.label] += 1
            position_edu[positionID][education][day][d.label] += 1
        return cate_edu, app_edu, position_edu

    def read_edu_action_corr(self):
        cate_edu_action = dict()
        app_edu_action = dict()
        for d in self.data_set.get_data_list():
            if d.label != 1:
                continue
            day = d.clickTime // 10000
            userID = d.userID
            education = self.user.get_value(userID).education
            appID = self.ad.get_value(d.creativeID).appID
            cate = self.app.get_value(appID).appCategory
            if cate not in cate_edu_action:
                cate_edu_action[cate] = np.zeros([8, 31])
            if appID not in app_edu_action:
                app_edu_action[appID] = np.zeros([8, 31])
            cate_edu_action[cate][education][day] += 1
            app_edu_action[appID][education][day] += 1
        for key in self.app_actions.get_keys():
            for d in self.app_actions.get_value(key):
                installTime = d.installTime
                day = installTime // 10000
                appID = d.appID
                userID = d.userID
                education = self.user.get_value(userID).education
                cate = self.app.get_value(appID).appCategory
                if cate not in cate_edu_action:
                    cate_edu_action[cate] = np.zeros([8, 31])
                if appID not in app_edu_action:
                    app_edu_action[appID] = np.zeros([8, 31])
                cate_edu_action[cate][education][day] += 1
                app_edu_action[appID][education][day] += 1
        return cate_edu_action, app_edu_action

    def read_app_baby_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            userID = d.userID
            clickTime = d.clickTime
            baby = self.user.get_value(userID).haveBabys
            creativeID = d.creativeID
            appID = self.ad.get_value(creativeID).appID
            label = d.label
            if label < 0:
                continue
            if appID not in result:
                result[appID] = np.zeros([7, 31, 2])
            result[appID][baby][clickTime // 10000][label] += 1
        return result

    def read_cate_baby_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            userID = d.userID
            clickTime = d.clickTime
            baby = self.user.get_value(userID).haveBabys
            creativeID = d.creativeID
            appID = self.ad.get_value(creativeID).appID
            appCategory = self.app.get_value(appID).appCategory
            label = d.label
            if label < 0:
                continue
            if appCategory not in result:
                result[appCategory] = np.zeros([7, 31, 2])
            result[appCategory][baby][clickTime // 10000][label] += 1
        return result

    def read_cate_time_corr(self):
        result = dict()
        for d in self.data_set.get_data_list():
            creativeID = d.creativeID
            appID = self.ad.get_value(creativeID).appID
            appCategory = self.app.get_value(appID).appCategory
            hour = d.clickTime // 100 % 100
            day = d.clickTime // 10000
            label = d.label
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
            if d.clickTime < clickDay - tw or d.clickTime >= clickDay:
                continue
            user_click[d.clickTime // 100 % 100] += 1
        return [self.cos_similarity(cate, user_click)]

    def cate_edu_convert_ratio(self, cate, edu, day):
        if cate not in self.cate_edu_corr:
            return [0]
        a = np.sum(self.cate_edu_corr[cate][edu, : day, 1])
        b = np.sum(self.cate_edu_corr[cate][edu, :day, :])
        return [a / b if b > 0 else 0]

    def cate_edu_convert_sr(self, cate, edu, day):
        if cate not in self.cate_edu_corr:
            return [0]
        a = np.sum(self.cate_edu_corr[cate][edu, : day, 1])
        b = np.sum(self.cate_edu_corr[cate][:, :day, 1])
        return [a / b if b > 0 else 0]

    def app_edu_convert_ratio(self, appID, edu, day):
        if appID not in self.app_edu_corr:
            return [0]
        a = np.sum(self.app_edu_corr[appID][edu, : day, 1])
        b = np.sum(self.app_edu_corr[appID][edu, :day, :])
        return [a / b if b > 0 else 0]

    def app_edu_convert_sr(self, appID, edu, day):
        if appID not in self.app_edu_corr:
            return [0]
        a = np.sum(self.app_edu_corr[appID][edu, : day, 1])
        b = np.sum(self.app_edu_corr[appID][:, :day, 1])
        return [a / b if b > 0 else 0]

    def position_edu_convert_ratio(self, positionID, edu, day):
        if positionID not in self.position_edu_corr:
            return [0]
        a = np.sum(self.position_edu_corr[positionID][edu, : day, 1])
        b = np.sum(self.position_edu_corr[positionID][edu, :day, :])
        return [a / b if b > 0 else 0]

    def position_edu_convert_sr(self, positionID, edu, day):
        if positionID not in self.position_edu_corr:
            return [0]
        a = np.sum(self.position_edu_corr[positionID][edu, : day, 1])
        b = np.sum(self.position_edu_corr[positionID][:, :day, 1])
        return [a / b if b > 0 else 0]

    def cate_edu_action_convert_sr(self, cate, edu, day):
        if cate not in self.cate_edu_action:
            return [0]
        a = np.sum(self.cate_edu_action[cate][edu, : day])
        b = np.sum(self.cate_edu_action[cate][:, :day])
        return [a / b if b > 0 else 0]

    def app_edu_action_convert_sr(self, appID, edu, day):
        if appID not in self.app_edu_action:
            return [0]
        a = np.sum(self.app_edu_action[appID][edu, : day])
        b = np.sum(self.app_edu_action[appID][:, :day])
        return [a / b if b > 0 else 0]

    def cate_gender_convert_ratio(self, cate, gender, day):
        if cate not in self.cate_gender_corr:
            return [0]
        a = np.sum(self.cate_gender_corr[cate][gender, : day, 1])
        b = np.sum(self.cate_gender_corr[cate][gender, : day, :])
        return [a / b if b > 0 else 0]

    def cate_gender_convert_sr(self, cate, gender, day):
        if cate not in self.cate_gender_corr:
            return [0]
        a = np.sum(self.cate_gender_corr[cate][gender, : day, 1])
        b = np.sum(self.cate_gender_corr[cate][:, : day, 1])
        return [a / b if b > 0 else 0]

    def app_gender_convert_ratio(self, appID, gender, day):
        if appID not in self.app_gender_corr:
            return [0]
        a = np.sum(self.app_gender_corr[appID][gender, : day, 1])
        b = np.sum(self.app_gender_corr[appID][gender, : day, :])
        return [a / b if b > 0 else 0]

    def app_gender_convert_sr(self, appID, gender, day):
        if appID not in self.app_gender_corr:
            return [0]
        a = np.sum(self.app_gender_corr[appID][gender, : day, 1])
        b = np.sum(self.app_gender_corr[appID][:, : day, 1])
        return [a / b if b > 0 else 0]

    def position_gender_convert_ratio(self, positionID, gender, day):
        if positionID not in self.position_gender_corr:
            return [0]
        a = np.sum(self.position_gender_corr[positionID][gender, : day, 1])
        b = np.sum(self.position_gender_corr[positionID][gender, : day, :])
        return [a / b if b > 0 else 0]

    def position_gender_convert_sr(self, positionID, gender, day):
        if positionID not in self.position_gender_corr:
            return [0]
        a = np.sum(self.position_gender_corr[positionID][gender, : day, 1])
        b = np.sum(self.position_gender_corr[positionID][:, : day, 1])
        return [a / b if b > 0 else 0]

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
        education = param['education']
        positionID = param['positionID']
        gender = param['gender']
        day = param['clickDay'] // 10000
        for _tw in tw:
            result.extend(self.generate(self.app_baby_to_vec, 'app_baby_corr_{}'.format(_tw), True,
                                        appID, haveBaby, clickDay, _tw))
            result.extend(self.generate(self.cate_baby_to_vec, 'cate_baby_corr_{}'.format(_tw), True,
                                        appCategory, haveBaby, clickDay, _tw))
            result.extend(self.generate(self.cate_time_to_vec, 'cate_hour_corr_{}'.format(_tw), True,
                                        appCategory, clickTime // 100 % 100, clickDay, _tw))
            result.extend(self.generate(self.cate_hour_user_similarity, 'cate_hour_user_similarity_{}'.format(_tw), True,
                                        appCategory, userID, clickDay, _tw))
        result.extend(self.generate(self.cate_edu_convert_ratio, 'cate_edu_convert_ratio', True,
                                    appCategory, education, day))
        result.extend(self.generate(self.cate_edu_convert_sr, 'cate_edu_convert_sr', True,
                                    appCategory, education, day))
        result.extend(self.generate(self.app_edu_convert_ratio, 'app_edu_convert_ratio', True,
                                    appID, education, day))
        result.extend(self.generate(self.app_edu_convert_sr, 'app_edu_convert_sr', True,
                                    appID, education, day))
        result.extend(self.generate(self.position_edu_convert_ratio, 'position_edu_convert_ratio', True,
                                    positionID, education, day))
        result.extend(self.generate(self.position_edu_convert_sr, 'position_edu_convert_sr', True,
                                    positionID, education, day))
        result.extend(self.generate(self.cate_edu_action_convert_sr, 'cate_edu_action_convert_sr', True,
                                    appCategory, education, day))
        result.extend(self.generate(self.app_edu_action_convert_sr, 'app_edu_action_convert_sr', True,
                                    appID, education, day))
        result.extend(self.generate(self.cate_gender_convert_ratio, 'cate_gender_convert_ratio', True,
                                    appCategory, gender, day))
        result.extend(self.generate(self.cate_gender_convert_sr, 'cate_gender_convert_sr', True,
                                    appCategory, gender, day))
        result.extend(self.generate(self.app_gender_convert_ratio, 'app_gender_convert_ratio', True,
                                    appID, gender, day))
        result.extend(self.generate(self.app_gender_convert_sr, 'app_gender_convert_sr', True,
                                    appID, gender, day))
        result.extend(self.generate(self.position_gender_convert_ratio, 'position_gender_convert_ratio', True,
                                    positionID, gender, day))
        result.extend(self.generate(self.position_gender_convert_sr, 'position_gender_convert_sr', True,
                                    positionID, gender, day))
        Combine_Corr.flag = True
        return result
