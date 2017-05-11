class User_Role:
    flag = False
    fea_names = list()

    def __init__(self, user):
        self.user = user

    def get_fea_names(self):
        return User_Role.fea_names

    def age_to_vec(self, param):
        return [param['age']]

    def gender_to_vec(self, param):
        res = [0] * 3
        res[param['gender']] = 1
        return res

    def edu_to_vec(self, param):
        res = [0] * 8
        res[param['education']] = 1
        return res

    def marriage_to_vec(self, param):
        res = [0] * 4
        res[param['marriageStatus']] = 1
        return res

    def baby_to_vec(self, param):
        res = [0] * 7
        res[param['haveBaby']] = 1
        return res

    def generate(self, func, param, scope):
        fea = func(param)
        if not User_Role.flag:
            for index in range(len(fea)):
                User_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        u = self.user.get_value(param['userID'])
        result.extend(self.generate(self.age_to_vec, {'age': u['age']}, 'user_age'))
        result.extend(self.generate(self.gender_to_vec, {'gender': u['gender']}, 'user_gender'))
        result.extend(self.generate(self.edu_to_vec, {'education': u['education']}, 'user_edu'))
        result.extend(self.generate(self.marriage_to_vec, {'marriageStatus': u['marriageStatus']}, 'user_marriage'))
        result.extend(self.generate(self.baby_to_vec, {'haveBaby': u['haveBaby']}, 'user_havebaby'))
        User_Role.flag = True
        return result
