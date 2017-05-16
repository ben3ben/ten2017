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
    ad = Advertisement(Configure.ad_path, debug=debug)
    data_set = Dataset(Configure.train_path, Configure.test_path, debug=debug)
    user = User(Configure.user_path, debug=debug)

    from_t = 290000
    end_t = 310000
    result = dict()
    for d in data_set.get_data_list():
        if d['clickTime'] < from_t or d['clickTime'] >= end_t:
            continue
        userID = d['userID']
        baby = user.get_value(userID)['haveBaby']
        creativeID = d['creativeID']
        appID = ad.get_value(creativeID)['appID']
        label = d['label']
        if baby not in result:
            result[baby] = dict()
        if appID not in result[baby]:
            result[baby][appID] = [0, 0]
        result[baby][appID][label] += 1
    fout = open(Configure.baby_app_correlate.format(from_t, end_t), 'w')
    for baby in result:
        for appID in result[baby]:
            s = result[baby][appID]
            r = s[1] / (s[0] + s[1]) if s[1] > 0 else 0
            fout.write('{},{},{},{},{}\n'.format(baby, appID, s[0], s[1], r))
    fout.close()
