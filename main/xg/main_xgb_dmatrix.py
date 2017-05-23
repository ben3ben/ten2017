import xgboost as xgb
import sys

sys.path.append('../..')
from conf.configure import Configure
from model.xgb_func import *
from handle.handle import *

if __name__ == '__main__':
    feature_names = read_feature_names(Configure.xgb_feature['feature_names'])
    dtrain = xgb.DMatrix(Configure.xgb_feature['xgb_train'], feature_names=feature_names)
    dtest = xgb.DMatrix(Configure.xgb_feature['xgb_test'], feature_names=feature_names)
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
    bst.apply()
    bst.save_model(Configure.xgb_model_file['model'])

    feature_importance = xgb_feature_importance(bst, dtrain.feature_names)
    fout = open(Configure.xgb_feature_importance, 'w')
    fout.write('feature,gain,weight,cover\n')
    for key in feature_importance:
        s = feature_importance[key]
        fout.write('{},{},{},{}\n'.format(key, s['gain'], s['weight'], s['cover']))
    fout.close()

    '''save train and test result'''
    pred_train = bst.predict(dtrain)
    prediction_to_file(read_instanceID(Configure.xgb_feature['train_instanceID']), dtrain.get_label(), pred_train,
                       Configure.xgb_model_file['train'])
    pred_test = bst.predict(dtest)
    prediction_to_file(read_instanceID(Configure.xgb_feature['test_instanceID']), dtest.get_label(), pred_test,
                       Configure.xgb_model_file['test'])
    del dtrain
    del dtest
    dsubmit = xgb.DMatrix(Configure.xgb_feature['xgb_submit'], feature_names=feature_names)
    submission = bst.predict(dsubmit)
    submit_file(read_instanceID(Configure.xgb_feature['submit_instanceID']), submission, Configure.submission)
    prediction_to_file(read_instanceID(Configure.xgb_feature['submit_instanceID']), dsubmit.get_label(), submission,
                       Configure.xgb_model_file['submit'])
