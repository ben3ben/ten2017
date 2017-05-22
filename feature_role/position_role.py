from reading.dataset import Dataset
from reading.position import Position
from conf.configure import Configure
from handle.handle import handle_correlate_to_vec
import scipy


class Position_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set, position):
        self.data_set = data_set  # type: Dataset
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

    def click_count_operator(self, positionID, _day, tw):
        return [self.position.get_position_count(positionID, 0, _day - tw, _day)]

    def convert_count_operator(self, positionID, _day, tw):
        return [self.position.get_position_count(positionID, 1, _day - tw, _day)]

    def convert_ratio(self, positionID, _day, tw):
        convert = self.position.get_position_count(positionID, 1, _day - tw, _day)
        _sum = self.position.get_position_count(positionID, -1, _day - tw, _day)
        return [convert / (_sum + 1)]

    def position_convert_ratio_median(self, positionID, _day, tw):
        cr = list()
        for i in range(tw):
            convert = self.position.get_position_count(positionID, 1, _day - i - 1, _day - i)
            click = self.position.get_position_count(positionID, 0, _day - i - 1, _day - i)
            cr.append(convert / (click + convert + 1))
        return [scipy.median(cr)]

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
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
        _day = param['clickDay'] // 10000
        pos = self.position.get_value(positionID)
        result.extend(self.generate(self.sitesetID_to_vec, 'position_sitesetID', False, pos['sitesetID']))
        result.extend(self.generate(self.positionType_to_vec, 'position_positionType', False, pos['positionType']))
        for tw in Configure.days_windows:
            _tw = tw // 10000
            result.extend(self.generate(self.click_count_operator, 'position_click_count_{}'.format(_tw), True,
                                        positionID, _day, _tw))
            result.extend(self.generate(self.convert_count_operator, 'position_convert_count_{}'.format(_tw), True,
                                        positionID, _day, _tw))
            result.extend(self.generate(self.convert_ratio, 'position_convert_ratio_{}'.format(_tw), True,
                                        positionID, _day, _tw))
        result.extend(self.generate(self.position_convert_ratio_median, 'position_cr_median_{}'.format(_tw), True,
                                    positionID, _day, _tw))
        Position_Role.flag = True
        return result
