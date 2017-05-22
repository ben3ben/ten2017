import numpy as np
from reading.app import App
from conf.configure import Configure


class App_Role:
    flag = False
    fea_names = list()

    def __init__(self, app):
        self.app = app  # type: App
        self.fea_set = dict()

    def get_fea_names(self):
        return App_Role.fea_names

    def category_to_vec(self, appCategory):
        bai = appCategory // 100
        result = [0] * 6
        result[bai] = 1
        result.append(1 if 0 < appCategory < 100 else 0)
        return result

    def click_count_operator(self, appCategory, _time, tw):
        dlist = self.app.get_dataset(appCategory)
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
                result[index] += 1
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def convert_count_operator(self, appCategory, _time, tw):
        dlist = self.app.get_dataset(appCategory)
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
                result[index] += d['label']
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def convert_ratio(self, appCategory, _time, tw):
        convert = self.convert_count_operator(appCategory, _time, tw)
        click = self.click_count_operator(appCategory, _time, tw)
        result = [a / (b + a + 1) for a, b in zip(convert, click)]
        return result

    def split_in_hours(self, appCategory, clickDay, tw):
        count = np.zeros([2, 24])
        for d in self.app.get_dataset(appCategory):
            clickTime = d['clickTime']
            if clickTime < clickDay - tw or clickTime >= clickDay:
                continue
            hour = clickTime // 100 % 100
            label = d['label']
            count[label][hour] += 1
        _sum = np.sum(count, axis=1)
        count /= _sum.reshape([2, 1])
        result = list()
        for i in range(0, 24, 8):
            result.append(np.sum(count[0][i:i+8]))
            result.append(np.sum(count[1][i:i+8]))
        # for i in range(8, 24, 3):
        #     result.append(np.sum(count[0][i:i+3]) - np.sum(count[0][i+3:i+6]))
        return result

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(func.__name__, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not App_Role.flag:
            for index in range(len(fea)):
                App_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        appID = param['appID']
        clickDay = param['clickDay']
        app = self.app.get_value(appID)
        appCategory = app['appCategory']
        # result.extend(self.generate(self.category_to_vec, 'app_cate_to_vec', True,
        #                             appCategory))
        result.extend(self.generate(self.click_count_operator, 'app_cate_dataset_click_count', True,
                                    appCategory, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_count_operator, 'app_cate_dataset_convert_count', True,
                                    appCategory, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_ratio, 'app_cate_dataset_convert_ratio', True,
                                    appCategory, param['clickDay'], Configure.days_windows))
        for _tw in [30000]:
            result.extend(self.generate(self.split_in_hours, 'app_cate_split_in_hours_{}'.format(_tw), True,
                                        appCategory, clickDay, _tw))
        App_Role.flag = True
        return result
