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
    train = dmatrix.run(Configure.train_begin_t, Configure.train_end_t, ratio=1.)
    # train = dmatrix.run(270000, 290000, ratio=1.)
    # train = dmatrix.run(280000, 300000, 'train')
    train = select_columns(train, Configure.features_erase)
    print('generate test...')
    test = dmatrix.run(Configure.test_begin_t, Configure.test_end_t)
    test = select_columns(test, Configure.features_erase)


    # print('feature names :', train['feature_names'])
    print('train positive labels : {}\t total labels : {}'.format(sum(train['labels']), len(train['labels'])))
    print('test positive labels : {}\t total labels : {}'.format(sum(test['labels']), len(test['labels'])))

    print('feature names len:', len(train['feature_names']))
    print('train x columns len:', len(train['features'][0]))
    '''xgboost'''
    dtrain = xgb.DMatrix(train['features'], train['labels'], feature_names=train['feature_names'])
    dtest = xgb.DMatrix(test['features'], test['labels'], feature_names=test['feature_names'])
    param = {'booster': 'gbtree',
             'max_depth': 6,
             'min_child_weight': 10,
             'learning_rate': 0.03,
             'subsample': 0.9,
             'colsample_bytree': 0.9,
             'gamma': 0.15,
             # 'lambda': 10,
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
    bst.save_model(Configure.xgb_model_file['model'])

    feature_importance = xgb_feature_importance(bst, train['feature_names'])
    fout = open(Configure.xgb_feature_importance, 'w')
    fout.write('feature,gain,weight,cover\n')
    for key in feature_importance:
        s = feature_importance[key]
        fout.write('{},{},{},{}\n'.format(key, s['gain'], s['weight'], s['cover']))
    fout.close()

    '''save train and test result'''
    pred_train = bst.predict(dtrain)
    prediction_to_file(train['instanceIDs'], train['labels'], pred_train, Configure.xgb_model_file['train'])
    pred_test = bst.predict(dtest)
    prediction_to_file(test['instanceIDs'], test['labels'], pred_test, Configure.xgb_model_file['test'])
    # del dtrain
    # del dtest
    # del train
    # del test
    # print('generate submit...')
    # submit = dmatrix.run(Configure.submit_begin_t, Configure.submit_end_t)
    # submit = select_columns(submit, Configure.features_erase)
    # dsubmit = xgb.DMatrix(submit['features'], feature_names=submit['feature_names'])
    # submission = bst.predict(dsubmit)
    # submit_file(submit['instanceIDs'], submission, Configure.submission)
    # prediction_to_file(submit['instanceIDs'], submit['labels'], submission, Configure.xgb_model_file['submit'])
