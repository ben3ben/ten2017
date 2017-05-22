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
from model.xgb_kflod import Xgb_Kflod

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
    train = dmatrix.run(Configure.train_begin_t, Configure.train_end_t)
    # train = dmatrix.run(280000, 300000, 'train')
    train = select_columns(train, Configure.features_erase)

    # print('feature names :', train['feature_names'])
    print('train positive labels : {}\t total labels : {}'.format(sum(train['labels']), len(train['labels'])))

    print('feature names len:', len(train['feature_names']))
    print('train x columns len:', len(train['features'][0]))
    '''xgboost'''
    param = {'booster': 'gbtree',
             'max_depth': 6,
             'min_child_weight': 10,
             'learning_rate': 0.03,
             'subsample': 0.9,
             'colsample_bytree': 0.9,
             'gamma': 0.15,
             'objective': 'reg:logistic',
             'silent': 1,
             'sample_type': 'uniform',
             'normalize_type': 'tree',
             'eval_metric': 'auc'}
    bst = Xgb_Kflod(10)
    bst.fit(param, train)
    '''save train and test result'''
    pred_train = bst.predict(train)
    prediction_to_file(train['instanceIDs'], train['labels'], pred_train, Configure.xgb_kflod_model_file['train'])
    del train
    print('generate test...')
    test = dmatrix.run(Configure.test_begin_t, Configure.test_end_t)
    test = select_columns(test, Configure.features_erase)
    pred_test = bst.predict(test)
    prediction_to_file(test['instanceIDs'], test['labels'], pred_test, Configure.xgb_kflod_model_file['test'])
    del test
    print('generate submit...')
    submit = dmatrix.run(Configure.submit_begin_t, Configure.submit_end_t)
    submit = select_columns(submit, Configure.features_erase)
    submission = bst.predict(submit)
    submit_file(submit['instanceIDs'], submission, Configure.submission)
    prediction_to_file(submit['instanceIDs'], submit['labels'], submission, Configure.xgb_kflod_model_file['submit'])
