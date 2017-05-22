from reading.user import User
from conf.configure import Configure


class User_Role:
    flag = False
    fea_names = list()

    def __init__(self, user):
        self.user = user    # type: User
        self.fea_set = dict()

    def get_fea_names(self):
        return User_Role.fea_names

    def age_to_vec(self, age):
        v0 = 1 if age == 0 else 0
        v1 = 1 if 0 < age < 11 else 0
        v2 = 1 if 10 < age < 29 else 0
        v3 = 1 if 28 < age < 40 else 0
        v4 = 1 if 39 < age < 51 else 0
        v5 = 1 if 50 < age < 62 else 0
        v6 = 1 if 61 < age else 0
        return [age, v0, v1, v2, v3, v4, v5, v6]

    def gender_to_vec(self, gender):
        res = [0] * 3
        res[gender] = 1
        return res

    def edu_to_vec(self, education):
        res = [0] * 8
        res[education] = 1
        return res

    def marriage_to_vec(self, marriageStatus):
        res = [0] * 4
        res[marriageStatus] = 1
        return res

    def baby_to_vec(self, haveBaby):
        res = [0] * 7
        res[haveBaby] = 1
        return res

    def hometown_equal_residence(self, hometown, residence):
        result = [0] * 2
        if hometown // 100 == residence // 100:
            result[0] = 1
        if hometown == residence:
            result[1] = 1
        return result

    def user_click_count(self, userID, _time, tw):
        return [self.user.get_user_count(userID, 0, _time - tw, _time)]

    def user_convert_count(self, userID, _time, tw):
        return [self.user.get_user_count(userID, 1, _time - tw, _time)]

    def user_convert_ratio(self, userID, _time, tw):
        convert = self.user.get_user_count(userID, 1, _time - tw, _time)
        _sum = self.user.get_user_count(userID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def hometown_click_count(self, hometown, _time, tw):
        return [self.user.get_hometown_count(hometown, 0, _time - tw, _time)]

    def hometown_convert_count(self, hometown, _time, tw):
        return [self.user.get_hometown_count(hometown, 1, _time - tw, _time)]

    def hometown_convert_ratio(self, hometown, _time, tw):
        convert = self.user.get_hometown_count(hometown, 1, _time - tw, _time)
        _sum = self.user.get_hometown_count(hometown, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def residence_click_count(self, residence, _time, tw):
        return [self.user.get_residence_count(residence, 0, _time - tw, _time)]

    def residence_convert_count(self, residence, _time, tw):
        return [self.user.get_residence_count(residence, 1, _time - tw, _time)]

    def residence_convert_ratio(self, residence, _time, tw):
        convert = self.user.get_residence_count(residence, 1, _time - tw, _time)
        _sum = self.user.get_residence_count(residence, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def user_all_diff(self, userID, _time, tw):
        a = self.user.get_user_count(userID, -1, _time - tw, _time)
        b = self.user.get_user_count(userID, -1, _time - 2 * tw, _time)
        return [2 * a - b, a / (b + 1)]

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not User_Role.flag:
            for index in range(len(fea)):
                User_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        u = self.user.get_value(param['userID'])
        userID = param['userID']
        hometown = param['hometown']
        residence = param['residence']
        _day = param['clickDay'] // 10000
        result.extend(self.generate(self.age_to_vec, 'user_age', True, u['age']))
        result.extend(self.generate(self.gender_to_vec, 'user_gender', True, u['gender']))
        result.extend(self.generate(self.edu_to_vec, 'user_edu', True, u['education']))
        result.extend(self.generate(self.marriage_to_vec, 'user_marriage', True, u['marriageStatus']))
        result.extend(self.generate(self.baby_to_vec, 'user_havebaby', True, u['haveBaby']))
        result.extend(self.generate(self.hometown_equal_residence, 'hometown_equal_residence', True, hometown, residence))

        for tw in Configure.days_windows:
            _tw = tw // 10000
            result.extend(self.generate(self.user_click_count, 'user_click_count_{}'.format(tw), True,
                                        userID, _day, _tw))
            result.extend(self.generate(self.user_convert_count, 'user_convert_count_{}'.format(tw), True,
                                        userID, _day, _tw))
            result.extend(self.generate(self.user_convert_ratio, 'user_convert_ratio_{}'.format(tw), True,
                                        userID, _day, _tw))

            result.extend(self.generate(self.hometown_click_count, 'user_hometown_click_count_{}'.format(tw), True,
                                        hometown, _day, _tw))
            result.extend(self.generate(self.hometown_convert_count, 'user_hometown_convert_count_{}'.format(tw), True,
                                        hometown, _day, _tw))
            result.extend(self.generate(self.hometown_convert_ratio, 'user_hometown_convert_ratio_{}'.format(tw), True,
                                        hometown, _day, _tw))

            result.extend(self.generate(self.residence_click_count, 'user_residence_click_count_{}'.format(tw), True,
                                        residence, _day, _tw))
            result.extend(self.generate(self.residence_convert_count, 'user_residence_convert_count_{}'.format(tw), True,
                                        residence, _day, _tw))
            result.extend(self.generate(self.residence_convert_ratio, 'user_residence_convert_ratio_{}'.format(tw), True,
                                        residence, _day, _tw))

        for tw in [1, 3, 5]:
            result.extend(self.generate(self.user_all_diff, 'user_all_diff_{}'.format(tw), True,
                                        userID, _day, tw))

        User_Role.flag = True
        return result
