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

len_limit = 20

def get_prod(correlate, da, db, label):
    if da not in correlate:
        return -1
    if db not in correlate[da]:
        return -1
    d, c, b, a = correlate[da][db]
    if a + b + c + d < len_limit:
        return -1
    if label == 0:
        return a / (a + c) if a > 0 else 0
    else:
        return b / (b + d) if b > 0 else 0


def creative_dlist(dlist, creativeID, clickTime, correlate):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = creativeID
        db = d['creativeID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def ad_dlist(dlist, adID, clickTime, correlate, ad : Advertisement):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = adID
        db = ad.get_value(d['creativeID'])['adID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def camgaign_dlist(dlist, camgaignID, clickTime, correlate, ad : Advertisement):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = camgaignID
        db = ad.get_value(d['creativeID'])['camgaignID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def advertiser_dlist(dlist, advertiserID, clickTime, correlate, ad : Advertisement):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = advertiserID
        db = ad.get_value(d['creativeID'])['advertiserID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def app_dlist(dlist, appID, clickTime, correlate, ad : Advertisement):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = appID
        db = ad.get_value(d['creativeID'])['appID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def position_dlist(dlist, positionID, clickTime, correlate):
    result = -1
    for d in dlist:
        if d['clickTime'] >= clickTime:
            break
        da = positionID
        db = d['positionID']
        _prod = get_prod(correlate, da, db, d['label'])
        if _prod > result:
            result = _prod
    return result

def read_correlate(path):
    result = dict()
    fin = open(path)
    for line in fin:
        tmp = [int(v) for v in line.strip().split(',')]
        if tmp[0] not in result:
            result[tmp[0]] = dict()
        result[tmp[0]][tmp[1]] = tmp[2:]
    fin.close()
    return result

def logloss(act, pred):
    epsilon = 1e-15
    pred = sp.maximum(epsilon, pred)
    pred = sp.minimum(1 - epsilon, pred)
    ll = sum(act * sp.log(pred) + sp.subtract(1, act) * sp.log(sp.subtract(1, pred)))
    ll = ll * -1.0 / len(act)
    return ll

if __name__ == '__main__':
    debug = False
    print('reading data...')
    ad = Advertisement(Configure.ad_path, debug=debug)
    app = App(Configure.app_categories_path, debug=debug)
    data_set = Dataset(Configure.train_path, Configure.test_path, debug=debug)
    position = Position(Configure.position_path, debug=debug)
    user = User(Configure.user_path, debug=debug)
    user_app_actions = User_App_Actions(Configure.user_app_actions_path, debug=debug)
    # user_app_installed = User_App_Installed(Configure.user_installedapps_path, debug=debug)
    data_set.add_to_position(position)
    data_set.add_to_advertisement(ad)
    data_set.add_to_app_cat(ad, app)

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


    for length in range(1000, 10000, 1000):
        len_limit = length
        for cond in ['adID', 'camgaignID', 'advertiserID', 'appID', 'positionID', 'creativeID']:
            for mode in ['train', 'test']:
                func = func_dict[cond]
                correlate = read_correlate(path_dict[cond][mode])
                end_t = Configure.train_end_t if mode == 'train' else (
                    Configure.test_end_t if mode == 'test' else Configure.submit_end_t)
                from_t = Configure.train_begin_t if mode == 'train' else (
                    Configure.test_begin_t if mode == 'test' else Configure.submit_begin_t)

                labels = list()
                predtions = list()
                for user_id in data_set.get_keys_by_user_id():
                    dlist = data_set.get_value_by_user_id(user_id)
                    for record in dlist:
                        if record['clickTime'] < from_t or record['clickTime'] >= end_t:
                            continue
                        labels.append(record['label'])
                        predtions.append(func(dlist, record[cond], record['clickTime'], correlate) if cond in ['creativeID', 'positionID']
                                         else func(dlist, ad.get_value(record['creativeID'])[cond], record['clickTime'], correlate, ad))
                _labels = list()
                _predictions = list()
                for a, b in zip(labels, predtions):
                    if b >=0:
                        _labels.append(a)
                        _predictions.append(b)
                print(len_limit, cond, mode, logloss(_labels, _predictions), len(_labels))
