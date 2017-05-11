from reading.position import Position
from conf.configure import Configure


class Position_Role:
    flag = False
    fea_names = list()

    def __init__(self, position):
        self.position = position  # type: Position
        self.fea_set = dict()

    def get_fea_names(self):
        return Position_Role.fea_names

    def sitesetID_to_vec(self, sitesetID):
        result = [0] * 3
        result[sitesetID] = 1
        return result

    def positionType_to_vec(self, positionType):
        result = [0] * 6
        result[positionType] = 1
        return result

    def click_count_operator(self, positionID, _time, tw):
        dlist = self.position.get_dataset(positionID)
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

    def convert_count_operator(self, positionID, _time, tw):
        dlist = self.position.get_dataset(positionID)
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
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

    def convert_ratio(self, positionID, _time, tw):
        convert = self.convert_count_operator(positionID, _time, tw)
        click = self.click_count_operator(positionID, _time, tw)
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
        if not Position_Role.flag:
            for index in range(len(fea)):
                Position_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        positionID = param['positionID']
        pos = self.position.get_value(positionID)
        result.extend(self.generate(self.sitesetID_to_vec, 'position_sitesetID', False, pos['sitesetID']))
        result.extend(self.generate(self.positionType_to_vec, 'position_positionType', False, pos['positionType']))
        result.extend(self.generate(self.click_count_operator, 'position_dataset_click_count', True,
                                    positionID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_count_operator, 'position_dataset_convert_count', True,
                                    positionID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.convert_ratio, 'position_dataset_convert_ratio', True,
                                    positionID, param['clickDay'], Configure.days_windows))
        Position_Role.flag = True
        return result
