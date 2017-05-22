from reading.user_app_actions import User_App_Actions
from reading.dataset import Dataset
from reading.advertisement import Advertisement
from reading.app import App
from conf.configure import Configure


class App_Actions_Role:
    flag = False
    fea_names = list()

    def __init__(self, app_actions : User_App_Actions, data_set : Dataset, ad : Advertisement, app : App):
        self.app_actions = app_actions
        self.data_set = data_set
        self.ad = ad
        self.app = app
        self.fea_set = dict()

    def get_fea_names(self):
        return App_Actions_Role.fea_names

    def install_count(self, userID, _time, tw):
        dlist = self.app_actions.get_value(userID)
        r = len(dlist)
        while r > 0 and dlist[r - 1]['installTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['installTime']
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                result[index] += 1
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def install_in_days(self, userID, _time):
        dlist = self.app_actions.get_value(userID)
        install_total = 0
        days = 0
        _install = 0
        max_install_oneday = 0
        near_times = 31
        for index, d in enumerate(dlist):
            if d['installTime'] >= _time:
                break
            install_total += 1
            if index == 0 or d['installTime'] // 10000 > dlist[index-1]['installTime'] // 10000:
                days += 1
                _install = 0
                near_times = _time - d['installTime']
            _install += 1
            if _install > max_install_oneday:
                max_install_oneday = _install
        avg_install = install_total / days if days > 0 else 0
        last_times = _time - dlist[0]['installTime'] if len(dlist) > 0 and dlist[0]['installTime'] < _time else 30
        return [days, install_total, avg_install, max_install_oneday, last_times, near_times]

    def appid_install_early(self, userID, appID, clickDay):
        _install_count = 0
        _install_time = 31
        for d in self.app_actions.get_value(userID):
            if d['installTime'] >= clickDay:
                break
            if d['appID'] == appID:
                _install_count += 1
                _install_time = clickDay - d['installTime']
        for d in self.data_set.get_value_by_user_id(userID):
            if d['clickTime'] >= clickDay:
                break
            creativeID = d['creativeID']
            _appID = self.ad.get_value(creativeID)['appID']
            if _appID == appID:
                _install_count += 1
                _install_time = min(_install_time, clickDay - d['clickTime'])
        return [_install_count, _install_time]

    def cate_install_early(self, userID, cate, clickDay):
        _install_count = 0
        _install_time = 31
        for d in self.app_actions.get_value(userID):
            if d['installTime'] >= clickDay:
                break
            _cate = self.app.get_value(d['appID'])['appCategory']
            if _cate == cate:
                _install_count += 1
                _install_time = clickDay - d['installTime']
        for d in self.data_set.get_value_by_user_id(userID):
            if d['clickTime'] >= clickDay:
                break
            creativeID = d['creativeID']
            _appID = self.ad.get_value(creativeID)['appID']
            _cate = self.app.get_value(_appID)['appCategory']
            if _cate == cate:
                _install_count += 1
                _install_time = min(_install_time, clickDay - d['clickTime'])
        return [_install_count, _install_time]

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not App_Actions_Role.flag:
            for index in range(len(fea)):
                App_Actions_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        userID = param['userID']
        appID = param['appID']
        clickDay = param['clickDay']
        appCategory = param['appCategory']
        result.extend(self.generate(self.install_count, 'app_actions_install_count', True,
                                    userID, param['clickDay'], [50000, 100000, 150000, 200000]))
        result.extend(self.generate(self.install_in_days, 'app_actions_install_in_days', True,
                                    userID, param['clickDay']))
        result.extend(self.generate(self.appid_install_early, 'app_actions_appID_install_early', True,
                                    userID, appID, clickDay))
        result.extend(self.generate(self.cate_install_early, 'app_actions_cate_install_early', True,
                                    userID, appCategory, clickDay))
        App_Actions_Role.flag = True
        return result
