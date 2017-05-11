from reading.dataset import Dataset
from conf.configure import Configure


class Dataset_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set):
        self.data_set = data_set  # type: Dataset

    def get_fea_names(self):
        return Dataset_Role.fea_names

    def clicktime_to_vec(self, param):
        clickTime = param['clickTime']
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

    def connectionType_to_vec(self, param):
        result = [0] * 5
        result[param['connectionType']] = 1
        return result

    def telecomsOperator_to_vec(self, param):
        result = [0] * 4
        result[param['telecomsOperator']] = 1
        return result

    def click_count_operator(self, param, dlist, _time, tw):
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

    def convert_count_operator(self, param, dlist, _time, tw):
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        # print('clickDay :', _time, '\tclickTime :', dlist[r-1]['clickTime'] if r > 0 else None)
        result = [0] * len(tw)
        index = 0
        # print('-' * 10, _time, dlist[r-1]['clickTime'] if r > 0 else None)
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['clickTime']
                # print(d['clickTime'])
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                result[index] += d['label']
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    def convert_ratio(self, param, dlist, _time, tw):
        convert = self.convert_count_operator(param, dlist, _time, tw)
        click = self.click_count_operator(param, dlist, _time, tw)
        result = [a / (b + a + 1) for a, b in zip(convert, click)]
        return result

    def generate(self, func, param, scope, *args):
        fea = func(param, *args)
        if not Dataset_Role.flag:
            for index in range(len(fea)):
                Dataset_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        result.extend(self.generate(self.clicktime_to_vec, param, 'dataset_clicktime'))
        result.extend(self.generate(self.connectionType_to_vec, param, 'dataset_connectionType'))
        result.extend(self.generate(self.telecomsOperator_to_vec, param, 'dataset_telecomsOperator'))
        result.extend(self.generate(self.click_count_operator, param, 'dataset_userid_clickcount',
                                    param['userid_dlist'], param['clickTime'], Configure.minutes_windows))
        result.extend(self.generate(self.convert_count_operator, param, 'dataset_userid_convertcount',
                                    param['userid_dlist'], param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_ratio, param, 'dataset_userid_convert_ratio',
                                    param['userid_dlist'], param['clickDay'], Configure.days_windows))
        Dataset_Role.flag = True
        return result
