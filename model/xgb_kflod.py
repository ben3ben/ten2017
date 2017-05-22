import xgboost as xgb
from sklearn.model_selection import KFold
from model.xgb_func import *

class Xgb_Kflod:
    def __init__(self, K):
        self.K = K
        self.models = list()

    def fit(self, param, train):
        kf = KFold(n_splits=self.K, shuffle=True)
        for train_index, test_index in kf.split(train['features']):
            dtrain = xgb.DMatrix(train['features'][train_index], train['labels'][train_index],
                                 feature_names=train['feature_names'])
            dtrain_eval = xgb.DMatrix(train['features'][test_index], train['labels'][test_index],
                                feature_names=train['feature_names'])
            evallist = [(dtrain_eval, 'eval'), (dtrain, 'train')]
            num_round = 300
            # xgb.cv(param, dtrain, num_round, nfold=10, verbose_eval=True, show_stdv=False, shuffle=True)
            # # exit()
            bst = xgb.train(param, dtrain, num_round, evallist, feval=evalerror, early_stopping_rounds=100)
            self.models.append(bst)
            del dtrain
            del dtrain_eval

    def predict(self, train):
        dtrain = xgb.DMatrix(train['features'], train['labels'],
                             feature_names=train['feature_names'])
        result = None
        for bst in self.models:
            pred = bst.predict(dtrain)
            if result is None:
                result = pred
            else:
                result += pred / self.K
        del dtrain
        return result
