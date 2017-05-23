import xgboost as xgb
import sys
sys.path.append('../..')
from conf.configure import Configure
from handle.handle import *
from model.xgb_kflod_dmatrix import Xgb_Kflod_DMatrix

if __name__ == '__main__':
    dtrain = xgb.DMatrix(Configure.xgb_feature['xgb_train'])
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
    bst = Xgb_Kflod_DMatrix(10)
    bst.fit(param, dtrain)
    '''save train and test result'''
    pred_train = bst.predict(dtrain)
    prediction_to_file(read_instanceID(Configure.xgb_feature['train_instanceID']), dtrain.get_label(), pred_train,
                       Configure.xgb_kflod_model_file['train'])
    dtest = xgb.DMatrix(Configure.xgb_feature['xgb_test'])
    pred_test = bst.predict(dtest)
    prediction_to_file(read_instanceID(Configure.xgb_feature['test_instanceID']), dtest.get_label(), pred_test,
                       Configure.xgb_kflod_model_file['test'])
    print('generate submit...')
    dsubmit = xgb.DMatrix(Configure.xgb_feature['xgb_submit'])
    submission = bst.predict(dsubmit)
    submit_file(read_instanceID(Configure.xgb_feature['submit_instanceID']), submission, Configure.submission)
    prediction_to_file(read_instanceID(Configure.xgb_feature['submit_instanceID']), dsubmit.get_label(), submission,
                       Configure.xgb_kflod_model_file['submit'])
