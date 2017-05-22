from reading.dataset import Dataset


class Dataset_Diff_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set):
        self.data_set = data_set  # type: Dataset

    def get_fea_names(self):
        return Dataset_Diff_Role.fea_names

    def click_operator(self, userID, day, tw):
        _sum = [0, 0]
        for d in self.data_set.get_value_by_user_id(userID):
            _day = d['clickTime'] // 10000
            if _day >= day:
                break
            if day - 2 * tw <= _day < day - tw:
                _sum[0] += 1
            if day - tw <= _day < day:
                _sum[1] += 1
        s = _sum[0] + _sum[1]
        result = [_sum[1] / s if s > 0 else 0]
        return result

    def convert_operator(self, userID, day, tw):
        _sum = [[0, 0], [0, 0]]
        for d in self.data_set.get_value_by_user_id(userID):
            _day = d['clickTime'] // 10000
            if _day >= day:
                break
            label = d['label']
            if day - 2 * tw <= _day < day - tw:
                _sum[label][0] += 1
            if day - tw <= _day < day:
                _sum[label][1] += 1
        s1 = _sum[1][0] + _sum[1][1]
        s_1 = _sum[0][1] + _sum[1][1]
        s_0 = _sum[0][0] + _sum[1][0]
        r1 = _sum[1][1] / s_1 if s_1 > 0 else 0
        r0 = _sum[0][1] / s_0 if s_0 > 0 else 0
        result = [_sum[1][1] / s1 if s1 > 0 else 0, r1 - r0]
        return result

    def generate(self, func, scope, *args):
        fea = func(*args)
        if not Dataset_Diff_Role.flag:
            for index in range(len(fea)):
                Dataset_Diff_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        userID = param['userID']
        clickDay = param['clickDay']
        day = clickDay // 10000
        result = list()
        for tw in [1, 2, 3]:
            result.extend(self.generate(self.click_operator, 'user_click_diff_{}'.format(tw), userID, day + 1, tw))
            result.extend(self.generate(self.convert_operator, 'user_convert_diff_{}'.format(tw), userID, day, tw))
        Dataset_Diff_Role.flag = True
        return result
