from reading.advertisement import Advertisement


class Advertisement_Diff_Role:
    flag = False
    fea_names = list()

    def __init__(self, ad):
        self.ad = ad  # type: Advertisement
        self.fea_set = dict()

    def get_fea_names(self):
        return Advertisement_Diff_Role.fea_names

    def create_click_op(self, creativeID, day, tw):
        s0 = self.ad.get_create_count(creativeID, 0, day - 2 * tw, day - tw)
        s1 = self.ad.get_create_count(creativeID, 0, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def create_convert_op(self, creativeID, day, tw):
        s0 = self.ad.get_create_count(creativeID, 1, day - 2 * tw, day - tw)
        s1 = self.ad.get_create_count(creativeID, 1, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def create_convert_ratio(self, creativeID, day, tw):
        s00 = self.ad.get_create_count(creativeID, 0, day - 2 * tw, day - tw)
        s01 = self.ad.get_create_count(creativeID, 0, day - tw, day)
        s10 = self.ad.get_create_count(creativeID, 1, day - 2 * tw, day - tw)
        s11 = self.ad.get_create_count(creativeID, 1, day - tw, day)
        r0 = s10 / (s00 + s10) if s00 + s10 > 0 else 0
        r1 = s11 / (s01 + s11) if s01 + s11 > 0 else 0
        return [r1, r1 - r0]

    def app_click_op(self, appID, day, tw):
        s0 = self.ad.get_app_count(appID, 0, day - 2 * tw, day - tw)
        s1 = self.ad.get_app_count(appID, 0, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def app_convert_op(self, appID, day, tw):
        s0 = self.ad.get_app_count(appID, 1, day - 2 * tw, day - tw)
        s1 = self.ad.get_app_count(appID, 1, day - tw, day)
        return [s1 / (s1 + s0) if s1 + s0 > 0 else 0]

    def app_convert_ratio(self, appID, day, tw):
        s00 = self.ad.get_app_count(appID, 0, day - 2 * tw, day - tw)
        s01 = self.ad.get_app_count(appID, 0, day - tw, day)
        s10 = self.ad.get_app_count(appID, 1, day - 2 * tw, day - tw)
        s11 = self.ad.get_app_count(appID, 1, day - tw, day)
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
        if not Advertisement_Diff_Role.flag:
            for index in range(len(fea)):
                Advertisement_Diff_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        creativeID = param['creativeID']
        appID = param['appID']
        clickDay = param['clickDay']
        _day = clickDay // 10000
        for tw in [1, 2, 3]:
            result.extend(self.generate(self.create_click_op, 'create_click_op_{}'.format(tw), True,
                                        creativeID, _day + 1, tw))
            result.extend(self.generate(self.create_convert_op, 'create_convert_op_{}'.format(tw), True,
                                        creativeID, _day, tw))
            result.extend(self.generate(self.create_convert_ratio, 'create_convert_ratio_{}'.format(tw), True,
                                        creativeID, _day, tw))
            result.extend(self.generate(self.app_click_op, 'app_click_op_{}'.format(tw), True,
                                        appID, _day + 1, tw))
            result.extend(self.generate(self.app_convert_op, 'app_convert_op_{}'.format(tw), True,
                                        appID, _day, tw))
            result.extend(self.generate(self.app_convert_ratio, 'app_convert_ratio_{}'.format(tw), True,
                                        appID, _day, tw))
        Advertisement_Diff_Role.flag = True
        return result
