import xgboost as xgb
import sys
sys.path.append('../..')
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed
from feature.dmatrix_diff import DMatrix_Diff
from feature.dmatrix import DMatrix
from model.xgb_func import *
from handle.handle import *

def predict(dmatrix, model_path):
    result = dict()
    bst = xgb.Booster({'nthread': 4})  # init model
    bst.load_model(model_path)  # load data
    result['train'] = dict()
    result['test'] = dict()
    result['submit'] = dict()
    train = dmatrix.run(train_from_t, train_end_t)
    dtrain = xgb.DMatrix(train['features'], train['labels'], feature_names=train['feature_names'])
    pred_train = bst.predict(dtrain)
    result['train']['label'] = train['labels']
    result['train']['predict'] = pred_train
    del train
    del dtrain
    test = dmatrix.run(test_from_t, test_end_t)
    dtest = xgb.DMatrix(test['features'], test['labels'], feature_names=test['feature_names'])
    pred_test = bst.predict(dtest)
    result['test']['label'] = test['labels']
    result['test']['predict'] = pred_test
    del test
    del dtest
    # submit = dmatrix.run(submit_from_t, submit_end_t)
    # dsubmit = xgb.DMatrix(submit['features'], submit['labels'], feature_names=submit['feature_names'])
    # pred_submit = bst.predict(dsubmit)
    # result['submit']['label'] = submit['labels']
    # result['submit']['predict'] = pred_submit
    return result

train_from_t = 290000
train_end_t = 300000
test_from_t = Configure.test_begin_t
test_end_t = Configure.test_end_t
submit_from_t = Configure.submit_begin_t
submit_end_t = Configure.submit_end_t

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
    print('reading finish...')
    data_set.add_to_position(position)
    data_set.add_to_advertisement(ad)
    data_set.add_to_app_cat(ad, app)
    data_set.add_to_user(user)

    dmatrix_diff = DMatrix_Diff(user, data_set, position, ad, app, user_app_actions)
    dmatrix_major = DMatrix(user, data_set, position, ad, app, user_app_actions)

    print('predict dmatrix major...')
    re_major = predict(dmatrix_major, Configure.xgb_model_file)
    print('predict dmatrix diff...')
    re_diff = predict(dmatrix_diff, Configure.xgb_diff_model_file)

    fout = open('fusion_result.txt', 'w')
    fout.write('r1,r2,train_loss,test_loss\n')
    for ratio in range(101):
        ratio1 = ratio / 100
        ratio2 = 1 - ratio1
        pred_train = ratio1 * re_major['train']['predict'] + ratio2 * re_diff['train']['predict']
        pred_test = ratio1 * re_major['test']['predict'] + ratio2 * re_diff['test']['predict']
        train_logloss = logloss(re_major['train']['label'], pred_train)
        test_logloss = logloss(re_major['test']['label'], pred_test)
        print('{0:0.2f},{1:0.2f},{2:},{3:}'.format(ratio1, ratio2, train_logloss, test_logloss))
        print('{0:0.2f},{1:0.2f},{2:},{3:}'.format(ratio1, ratio2, train_logloss, test_logloss), file=fout)
    fout.close()


