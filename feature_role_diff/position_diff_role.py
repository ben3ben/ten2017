from reading.position import Position


class Position_Diff_Role:
    flag = False
    fea_names = list()

    def __init__(self, position):
        self.position = position # type: Postion
        self.fea_set = dict()

    def get_fea_names(self):
        return Position_Diff_Role.fea_names

    def position_click_op(self, positionID, day, tw):
        s0 = self.position.get_position_count(positionID, 0, day - 2 * tw, day - tw)
        s1 = self.position.get_position_count(positionID, 0, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def position_convert_op(self, positionID, day, tw):
        s0 = self.position.get_position_count(positionID, 1, day - 2 * tw, day - tw)
        s1 = self.position.get_position_count(positionID, 1, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def position_convert_ratio(self, positionID, day, tw):
        s00 = self.position.get_position_count(positionID, 0, day - 2 * tw, day - tw)
        s01 = self.position.get_position_count(positionID, 0, day - tw, day)
        s10 = self.position.get_position_count(positionID, 1, day - 2 * tw, day - tw)
        s11 = self.position.get_position_count(positionID, 1, day - tw, day)
        r0 = s10 / (s00 + s10) if s00 + s10 > 0 else 0
        r1 = s11 / (s01 + s11) if s01 + s11 > 0 else 0
        return [r1, r1 - r0]

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not Position_Diff_Role.flag:
            for index in range(len(fea)):
                Position_Diff_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        positionID = param['positionID']
        clickDay = param['clickDay']
        _day = clickDay // 10000
        for tw in [1, 2, 3]:
            result.extend(self.generate(self.position_click_op, 'position_click_op_{}'.format(tw), True,
                                        positionID, _day + 1, tw))
            result.extend(self.generate(self.position_convert_op, 'position_convert_op_{}'.format(tw), True,
                                        positionID, _day, tw))
            result.extend(self.generate(self.position_convert_ratio, 'position_convert_ratio_{}'.format(tw), True,
                                        positionID, _day, tw))
        Position_Diff_Role.flag = True
        return result
