from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed
import pandas as pd
import numpy as np


if __name__ == '__main__':
    a = 1
    b = 0
    raise a > b
    exit()
    ad = pd.read_csv(Configure.ad_path)
    data_set = pd.read_csv(Configure.train_path)
    user = pd.read_csv(Configure.user_path)
    app = pd.read_csv(Configure.app_categories_path)
    user_app_actions = pd.read_csv(Configure.user_app_actions_path)


    data_train = data_set[data_set['clickTime'] < 290000]
    data_test = data_set[data_set['clickTime'] >= 290000]
    user_train = data_train['userID'].drop_duplicates().tolist()
    user_test = data_test['userID'].drop_duplicates().tolist()
    print(len(set(user_test) - set(user_train)))
    # data = data_set.merge(ad, how='inner', on='creativeID')
    # data = data.merge(user_app_actions, how='inner', on=['userID', 'appID'])
    # print(data.shape)