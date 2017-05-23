import xgboost as xgb
from sklearn.model_selection import KFold
from model.xgb_func import *
import numpy as np

class Xgb_Kflod_DMatrix:
    def __init__(self, K):
        self.K = K
        self.models = list()

    def fit(self, param, dmatrix : xgb.DMatrix):
        kf = KFold(n_splits=self.K, shuffle=True)
        loss = list()
        n = dmatrix.num_row()
        for train_index, test_index in kf.split([0] * n):
            dtrain = dmatrix.slice(train_index)
            dtrain_eval = dmatrix.slice(test_index)
            evallist = [(dtrain_eval, 'eval'), (dtrain, 'train')]
            num_round = 300
            # xgb.cv(param, dtrain, num_round, nfold=10, verbose_eval=True, show_stdv=False, shuffle=True)
            # # exit()
            bst = xgb.train(param, dtrain, num_round, evallist, feval=evalerror, early_stopping_rounds=100)
            self.models.append(bst)
            loss.append(logloss(dtrain_eval.get_label(), bst.predict(dtrain_eval)))
            del dtrain
            del dtrain_eval
        print('total loss :', loss)
        print('avg loss :', np.average(loss))

    def predict(self, dmatrix):
        result = None
        for bst in self.models:
            pred = bst.predict(dmatrix)
            if result is None:
                result = pred / self.K
            else:
                result += pred / self.K
        return result
