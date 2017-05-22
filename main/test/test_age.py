import pandas as pd
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.dataset import Dataset
from reading.user import User
from reading.app import App


if __name__ == '__main__':
    ad = Advertisement(Configure.ad_path)
    app = App(Configure.app_categories_path)
    data_set = Dataset(Configure.train_path, Configure.test_path)
    user = User(Configure.user_path)

    result0 = [0] * 100
    result1 = [0] * 100
    for d in data_set.get_data_list():
        userID = d['userID']
        age = user.get_value(userID)['age']
        label = d['label']
        if label < 0:
            continue
        if label == 0:
            result0[age] += 1
        else:
            result1[age] += 1
    for i in range(len(result0)):
        print(i, result0[i] + result1[i], result0[i], result1[i])


