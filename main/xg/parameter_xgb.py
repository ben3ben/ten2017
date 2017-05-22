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
from feature.dmatrix import DMatrix
from model.xgb_func import *
from handle.handle import *


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
    data_set.add_to_user(user)

    dmatrix = DMatrix(user, data_set, position, ad, app, user_app_actions)

    print('generate train...')
    train = dmatrix.run(Configure.train_begin_t, Configure.train_end_t, 'train')
    # train = dmatrix.run(280000, 300000, 'train')
    print('generate test...')
    test = dmatrix.run(Configure.test_begin_t, Configure.test_end_t, 'train')


    # print('feature names :', train['feature_names'])
    print('train positive labels : {}\t total labels : {}'.format(sum(train['labels']), len(train['labels'])))
    print('test positive labels : {}\t total labels : {}'.format(sum(test['labels']), len(test['labels'])))

    print('feature names len:', len(train['feature_names']))
    print('train x columns len:', len(train['features'][0]))
    '''xgboost'''
    dtrain = xgb.DMatrix(train['features'], train['labels'], feature_names=train['feature_names'])
    dtest = xgb.DMatrix(test['features'], test['labels'], feature_names=train['feature_names'])

    fout = open('parameter.txt', 'w')
    # for eta in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
    # for gamma in [i * 0.05 for i in range(41)]:
    # for min_child_weight in range(1, 100, 2):
    for _lambda in range(1, 100, 2):
        param = {'booster': 'gbtree',
                 'max_depth': 6,
                 'min_child_weight': 10,
                 'learning_rate': 0.03,
                 'subsample': 0.9,
                 'gamma': 0.15,
                 'lambda': _lambda,
                 'colsample_bytree': 0.9,
                 'objective': 'reg:logistic',
                 'silent': 1,
                 'sample_type': 'uniform',
                 'normalize_type': 'tree',
                 'eval_metric': 'auc'}
        evallist = [(dtest, 'eval'), (dtrain, 'train')]
        num_round = 300
        # xgb.cv(param, dtrain, num_round, nfold=10, verbose_eval=True, show_stdv=False, shuffle=True)
        # # exit()
        bst = xgb.train(param, dtrain, num_round, evallist, feval=evalerror, early_stopping_rounds=100)
        test_prediction = bst.predict(dtest)
        train_prediction = bst.predict(dtrain)
        print('_lambda :', _lambda, '\ttest logloss :', logloss(test['labels'], test_prediction), '\ttrain logloss:',
              logloss(train['labels'], train_prediction), file=fout)
        fout.flush()
    fout.close()
