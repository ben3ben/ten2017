from reading.dataset import Dataset
from reading.advertisement import Advertisement
from conf.configure import Configure
from handle.handle import handle_correlate_to_vec

class Dataset_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set, ad):
        self.data_set = data_set  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.creative_corr = {'train': self.read_correlate(Configure.creative_correlate['train']),
                              'test': self.read_correlate(Configure.creative_correlate['test']),
                              'submit': self.read_correlate(Configure.creative_correlate['submit'])}

    def read_correlate(self, path):
        result = dict()
        fin = open(path)
        for line in fin:
            tmp = [int(v) for v in line.strip().split(',')]
            if tmp[0] not in result:
                result[tmp[0]] = dict()
            result[tmp[0]][tmp[1]] = tmp[2:]
        fin.close()
        return result

    def get_fea_names(self):
        return Dataset_Role.fea_names

    def clicktime_to_vec(self, clickTime):
        result = list()
        minute = clickTime % 100
        hour = clickTime // 100 % 100
        result.extend([minute, hour])
        result.append(1 if hour < 10 else 0)
        result.append(1 if 12 < hour < 19 else 0)
        result.append(1 if 18 <= hour <= 21 else 0)
        result.append(1 if 22 <= hour or hour <= 5 else 0)
        result.append(1 if minute == 9 else 0)
        result.append(1 if 29 < minute < 34 else 0)
        result.append(1 if 10 < minute < 20 else 0)
        result.append(1 if 40 <= minute <= 50 else 0)
        result.append(1 if 25 < minute < 35 else 0)
        return result

    def connectionType_to_vec(self, connectionType):
        result = [0] * 6
        result[connectionType] = 1
        result[5] = connectionType
        return result

    def telecomsOperator_to_vec(self, telecomsOperator):
        result = [0] * 4
        result[telecomsOperator] = 1
        return result

    def eauql_creativeID(self, _dlist, val):
        return _dlist['creativeID'] == val

    def equal_adID(self, _dlist, val):
        return self.ad.get_value(_dlist['creativeID'])['adID'] == val

    def equal_camgaignID(self, _dlist, val):
        return self.ad.get_value(_dlist['creativeID'])['camgaignID'] == val

    def equal_advertiserID(self, _dlist, val):
        return self.ad.get_value(_dlist['creativeID'])['advertiserID'] == val

    def equal_appPlatform(self, _dlist, val):
        return self.ad.get_value(_dlist['creativeID'])['appPlatform'] == val

    def equal_appID(self, _dlist, val):
        return self.ad.get_value(_dlist['creativeID'])['appID'] == val

    def click_count_operator(self, dlist, _time, tw, condition_func=None, condition=None):
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['clickTime']
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                if condition_func is None or condition_func(d, condition):
                    result[index] += 1
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def convert_count_operator(self, dlist, _time, tw, condition_func=None, condition=None):
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['clickTime']
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                if condition_func is None or condition_func(d, condition):
                    result[index] += d['label']
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def convert_ratio(self, dlist, _time, tw, condition_func=None, condition=None):
        convert = self.convert_count_operator(dlist, _time, tw, condition_func, condition)
        click = self.click_count_operator(dlist, _time, tw, condition_func, condition)
        result = [a / (b + a + 1) for a, b in zip(convert, click)]
        return result

    def click_one_day(self, dlist, param):
        count = 0
        last = -1
        clickDay = param['clickDay']
        _dataset_keys = ['creativeID',
                        'positionID',
                        'connectionType',
                        'telecomsOperator']
        _ad_keys = ['adID',
                    'camgaignID',
                    'advertiserID',
                    'appPlatform',
                    'appID']
        r_dk = [0] * len(_dataset_keys)
        r_ak = [0] * len(_ad_keys)
        for i in range(len(dlist) - 1, -1, -1):
            day = dlist[i]['clickTime'] // 10000 * 10000
            if day == clickDay:
                count += 1
                for index, key in enumerate(_dataset_keys):
                    if param[key] == dlist[i][key]:
                        r_dk[index] += 1
                for index, key in enumerate(_ad_keys):
                    if param[key] == self.ad.get_value(dlist[i]['creativeID'])[key]:
                        r_ak[index] += 1
            if day < clickDay:
                last = clickDay - dlist[i]['clickTime']
                break
        result = [last, count]
        result.extend(r_dk)
        result.extend(r_ak)
        result.extend([v / count if v > 0 else 0 for v in r_dk])
        result.extend([v / count if v > 0 else 0 for v in r_ak])
        return result

    def click_in_days(self, dlist, clickDay):
        _click = 0
        _convert = 0
        _click_one_day = 0
        _day = 0
        for index, d in enumerate(dlist):
            if d['clickTime'] > clickDay:
                break
            elif d['clickTime'] // 10000 * 10000 == clickDay:
                _click_one_day += 1
            else:
                _click += 1
                _convert += d['label']
                if index == 0 or dlist[index]['clickTime'] // 10000 > dlist[index]['clickTime'] // 10000:
                    _day += 1
        avg_click_day = _click / _day if _click > 0 else 0
        avg_convert_day = _convert / _day if _convert > 0 else 0
        return [_day, avg_click_day, avg_convert_day, _click_one_day - avg_click_day]

    def creative_correlate(self, userID, creativeID, clickDay, mode):
        cond_name = 'creativeID'
        dlist = self.data_set.get_value_by_user_id(userID)
        correlate = self.creative_corr[mode]
        return handle_correlate_to_vec(correlate, dlist, cond_name, creativeID, clickDay)

    def last_appID_operator(self, userID, appID, clickTime):
        dlist = self.data_set.get_value_by_user_id(userID)
        before_total = 0
        before_convert_total = 0
        before_near = -1
        after_total = 0
        after_near = -1
        for d in dlist:
            _creative = d['creativeID']
            _clickTime = d['clickTime']
            _app = self.ad.get_value(_creative)['appID']
            if _clickTime // 10000 > clickTime // 10000:
                break
            if _app == appID:
                if _clickTime // 10000 < clickTime // 10000:
                    before_convert_total += 1
                if _clickTime < clickTime:
                    before_total += 1
                    before_near = clickTime - _clickTime
                if _clickTime > clickTime:
                    after_near = _clickTime - clickTime
                    after_total += 1
        return [before_total, before_near, after_total, after_near, before_convert_total]

    def app_op_set(self, userID, appID, clickTime):
        dlist = self.data_set.get_value_by_user_id(userID)
        app_set_oneday = set()
        app_set_before = set()
        for d in dlist:
            _creative = d['creativeID']
            _clickTime = d['clickTime']
            _app = self.ad.get_value(_creative)['appID']
            if _clickTime // 10000 > clickTime // 10000:
                break
            if _clickTime // 10000 == clickTime // 10000:
                app_set_oneday.add(_app)
            app_set_before.add(_app)
        return [len(app_set_before), len(app_set_oneday)]

    def generate(self, func, scope, *args):
        fea = func(*args)
        if not Dataset_Role.flag:
            for index in range(len(fea)):
                Dataset_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        userID = param['userID']
        clickTime = param['clickTime']
        clickDay = param['clickDay']
        connectionType = param['connectionType']
        telecomsOperator = param['telecomsOperator']
        creativeID = param['creativeID']
        appID = param['appID']
        dlist = self.data_set.get_value_by_user_id(userID)
        result = list()
        result.extend(self.generate(self.clicktime_to_vec, 'dataset_clicktime', clickTime))
        result.extend(self.generate(self.connectionType_to_vec, 'dataset_connectionType', connectionType))
        result.extend(self.generate(self.telecomsOperator_to_vec, 'dataset_telecomsOperator', telecomsOperator))
        result.extend(self.generate(self.click_count_operator, 'user_dataset_clickcount',
                                    dlist, clickTime, Configure.minutes_windows))
        result.extend(self.generate(self.convert_count_operator, 'user_dataset_convert_count',
                                    dlist, clickDay, Configure.days_windows))
        result.extend(self.generate(self.convert_ratio, 'user_dataset_convert_ratio',
                                    dlist, clickDay, Configure.days_windows))
        result.extend(self.generate(self.click_one_day, 'user_dataset_click_one_day',
                                    dlist, param))
        result.extend(self.generate(self.click_in_days, 'user_dataset_click_in_days',
                                    dlist, clickDay))

        result.extend(self.generate(self.click_count_operator, 'user_create_click_count',
                                    dlist, clickDay, Configure.days_windows, self.eauql_creativeID, creativeID))
        # result.extend(self.generate(self.convert_count_operator, 'user_create_convert_count',
        #                             dlist, clickDay, Configure.days_windows, self.eauql_creativeID, creativeID))
        # result.extend(self.generate(self.convert_ratio, 'user_create_convert_ratio',
        #                             dlist, clickDay, Configure.days_windows, self.eauql_creativeID, creativeID))

        result.extend(self.generate(self.click_count_operator, 'user_ad_click_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_adID, param['adID']))
        # result.extend(self.generate(self.convert_count_operator, 'user_ad_convert_count',
        #                             dlist, clickDay, Configure.days_windows, self.equal_adID, param['adID']))
        # result.extend(self.generate(self.convert_ratio, 'user_ad_convert_ratio',
        #                             dlist, clickDay, Configure.days_windows, self.equal_adID, param['adID']))

        result.extend(self.generate(self.click_count_operator, 'user_camgaignID_click_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_camgaignID, param['camgaignID']))
        # result.extend(self.generate(self.convert_count_operator, 'user_camgaignID_convert_count',
        #                             dlist, clickDay, Configure.days_windows, self.equal_camgaignID, param['camgaignID']))
        # result.extend(self.generate(self.convert_ratio, 'user_camgaignID_convert_ratio',
        #                             dlist, clickDay, Configure.days_windows, self.equal_camgaignID, param['camgaignID']))

        result.extend(self.generate(self.click_count_operator, 'user_advertiserID_click_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_advertiserID,
                                    param['advertiserID']))
        # result.extend(self.generate(self.convert_count_operator, 'user_advertiserID_convert_count',
        #                             dlist, clickDay, Configure.days_windows, self.equal_advertiserID,
        #                             param['advertiserID']))
        # result.extend(self.generate(self.convert_ratio, 'user_advertiserID_convert_ratio',
        #                             dlist, clickDay, Configure.days_windows, self.equal_advertiserID,
        #                             param['advertiserID']))

        result.extend(self.generate(self.click_count_operator, 'user_appPlatform_click_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_appPlatform,
                                    param['appPlatform']))
        result.extend(self.generate(self.convert_count_operator, 'user_appPlatform_convert_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_appPlatform,
                                    param['appPlatform']))
        result.extend(self.generate(self.convert_ratio, 'user_appPlatform_convert_ratio',
                                    dlist, clickDay, Configure.days_windows, self.equal_appPlatform,
                                    param['appPlatform']))

        result.extend(self.generate(self.click_count_operator, 'user_appID_click_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_appID,
                                    param['appID']))
        result.extend(self.generate(self.convert_count_operator, 'user_appID_convert_count',
                                    dlist, clickDay, Configure.days_windows, self.equal_appID,
                                    param['appID']))
        result.extend(self.generate(self.convert_ratio, 'user_appID_convert_ratio',
                                    dlist, clickDay, Configure.days_windows, self.equal_appID,
                                    param['appID']))
        # '''correlate features'''
        # result.extend(self.generate(self.creative_correlate, 'creative_correlate',
        #                             userID, creativeID, param['clickTime'], param['mode']))

        result.extend(self.generate(self.last_appID_operator, 'user_appID_last_op',
                                    userID, appID, clickTime))
        result.extend(self.generate(self.app_op_set, 'user_appID_op_set',
                                    userID, appID, clickTime))
        Dataset_Role.flag = True
        return result
