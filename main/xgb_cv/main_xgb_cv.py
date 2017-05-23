import xgboost as xgb
import sys

sys.path.append('../..')
from conf.configure import Configure
from model.xgb_func import *
from handle.handle import *

if __name__ == '__main__':
    feature_names = read_feature_names(Configure.xgb_feature['feature_names'])
    dtrain = xgb.DMatrix(Configure.xgb_feature['xgb_train'], feature_names=feature_names)
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
    num_round = 300
    # xgb.cv(param, dtrain, num_round, nfold=10, verbose_eval=True, show_stdv=False, shuffle=True)
    # # exit()
    history = xgb.cv(param, dtrain, num_round, 5, feval=evalerror, shuffle=True, verbose_eval=True)
    # print(history)

