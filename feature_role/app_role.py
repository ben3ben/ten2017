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
        app = self.app.get_value(appID)
        appCategory = app['appCategory']
        result.extend(self.generate(self.click_count_operator, 'app_cate_dataset_click_count', True,
                                    appCategory, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_count_operator, 'app_cate_dataset_convert_count', True,
                                    appCategory, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_ratio, 'app_cate_dataset_convert_ratio', True,
                                    appCategory, param['clickDay'], Configure.days_windows[2:]))
        App_Role.flag = True
        return result
