import xgboost as xgb
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed
from feature.dmatrix import DMatrix
from model.xgb_func import *
from handle.handle import *


if __name__ == '__main__':
    debug = False
    print('reading data...')
    user_app_actions = User_App_Actions(Configure.user_app_actions_path, debug=debug)

    result = [0] * 31
    for userid in user_app_actions.get_keys():
        dlist = user_app_actions.get_value(userid)
        for d in dlist:
            result[d['installTime'] // 10000] += 1
    for i in range(len(result)):
        print(i, result[i])
