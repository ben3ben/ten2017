import xgboost as xgb
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
import matplotlib.pyplot as plt
import numpy as np


def get_index(a, b):
    return a * 2 + b


def run(data: dict, from_t, end_t):
    print('running ...')
    result = dict()
    for userid in data.keys():
        # print(userid)
        dlist = data[userid]
        val_set = dict()
        for d in dlist:
            if d['clickTime'] < from_t or d['clickTime'] >= end_t:
                continue
            da = d['condition']
            label_a = d['label']
            for db in val_set:
                # if da == db:
                #     continue
                label_b = val_set[db]
                if da not in result:
                    result[da] = dict()
                if db not in result[da]:
                    result[da][db] = [0] * 4
                result[da][db][get_index(label_a, label_b)] += 1
            if da not in val_set or label_a == 1:
                val_set[da] = label_a
    return result


def common_part(d):
    result = dict()
    for k in ['label', 'clickTime']:
        result[k] = d[k]
    return result


def creative_dlist(d):
    result = common_part(d)
    result['condition'] = d['creativeID']
    return result


def position_dlist(d):
    result = common_part(d)
    result['condition'] = d['positionID']
    return result


def ad_dlist(d, ad: Advertisement):
    result = common_part(d)
    result['condition'] = ad.get_value(d['creativeID'])['adID']
    return result


def camgaign_dlist(d, ad: Advertisement):
    result = common_part(d)
    result['condition'] = ad.get_value(d['creativeID'])['camgaignID']
    return result


def advertiser_dlist(d, ad: Advertisement):
    result = common_part(d)
    result['condition'] = ad.get_value(d['creativeID'])['advertiserID']
    return result


def app_dlist(d, ad: Advertisement):
    result = common_part(d)
    result['condition'] = ad.get_value(d['creativeID'])['appID']
    return result


if __name__ == '__main__':
    debug = False
    print('reading...')
    ad = Advertisement(Configure.ad_path, debug=debug)
    app = App(Configure.app_categories_path, debug=debug)
    data_set = Dataset(Configure.train_path, Configure.test_path, debug=debug)
    position = Position(Configure.position_path, debug=debug)
    user = User(Configure.user_path, debug=debug)
    user_app_actions = User_App_Actions(Configure.user_app_actions_path)

    func_dict = {'creativeID': creative_dlist,
                 'adID': ad_dlist,
                 'camgaignID': camgaign_dlist,
                 'advertiserID': advertiser_dlist,
                 'appID': app_dlist,
                 'positionID': position_dlist}

    path_dict = {'creativeID': Configure.creative_correlate,
                 'adID': Configure.ad_correlate,
                 'camgaignID': Configure.camgaign_correlate,
                 'advertiserID': Configure.advertiser_correlate,
                 'appID': Configure.app_correlate,
                 'positionID': Configure.position_correlate}

    for cond in ['creativeID', 'positionID', 'adID', 'camgaignID', 'advertiserID', 'appID']:
        for mode in ['train', 'test', 'submit']:
            path = path_dict[cond][mode]
            func = func_dict[cond]
            end_t = Configure.train_begin_t if mode == 'train' else (Configure.test_begin_t if mode == 'test' else Configure.submit_begin_t)
            from_t = end_t - 50000


            data = dict()
            for userid in data_set.get_keys_by_user_id():
                dlist = data_set.get_value_by_user_id(userid)
                data[userid] = list()
                for d in dlist:
                    r = func(d) if cond in ['creativeID', 'positionID'] else func(d, ad)
                    data[userid].append(r)

            result = run(data, from_t, end_t)
            fout = open(path, 'w')
            for k1 in result:
                for k2 in result[k1]:
                    s = result[k1][k2]
                    fout.write('{},{},{},{},{},{}\n'.format(k1, k2, s[0], s[1], s[2], s[3]))
            fout.close()
