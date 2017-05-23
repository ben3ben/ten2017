# coding: utf-8
from sklearn.model_selection import train_test_split
from sklearn import metrics
from xgboost.sklearn import XGBClassifier, XGBRegressor
import numpy as np

class XgboostFeature():
      ##可以传入xgboost的参数
      ##常用传入特征的个数 即树的个数 默认30
      def __init__(self,n_estimators=30,learning_rate =0.3,max_depth=3,min_child_weight=1,gamma=0.3,subsample=0.8,colsample_bytree=0.8,objective= 'binary:logistic',nthread=4,scale_pos_weight=1,reg_alpha=1e-05,reg_lambda=1,seed=27):
          self.n_estimators=n_estimators
          self.learning_rate=learning_rate
          self.max_depth=max_depth
          self.min_child_weight=min_child_weight
          self.gamma=gamma
          self.subsample=subsample
          self.colsample_bytree=colsample_bytree
          self.objective=objective
          self.nthread=nthread
          self.scale_pos_weight=scale_pos_weight
          self.reg_alpha=reg_alpha
          self.reg_lambda=reg_lambda
          self.seed=seed

      def mergeToOne(self,X,X2):
          X3=[]
          for i in range(X.shape[0] - 1, -1, -1):
              tmp=np.array([list(X[i]),list(X2[i])])
              X3.append(list(np.hstack(tmp)))
          X3=np.array(X3)
          return X3
      ##切割训练
      def fit_model_split(self,X_train,y_train,X_test,y_test):
          ##X_train_1用于生成模型  X_train_2用于和新特征组成新训练集合
          X_train_1, X_train_2, y_train_1, y_train_2 = train_test_split(X_train, y_train, test_size=0.6, random_state=0)
          clf = XGBRegressor(
                 learning_rate =self.learning_rate,
                 n_estimators=self.n_estimators,
                 max_depth=self.max_depth,
                 min_child_weight=self.min_child_weight,
                 gamma=self.gamma,
                 subsample=self.subsample,
                 colsample_bytree=self.colsample_bytree,
                 objective= self.objective,
                 nthread=self.nthread,
                 scale_pos_weight=self.scale_pos_weight,
                 reg_alpha=self.reg_alpha,
                 reg_lambda=self.reg_lambda,
                 seed=self.seed)
          clf.fit(X_train_1, y_train_1)
          new_feature= clf.apply(X_train_2)
          X_train_new2=self.mergeToOne(X_train_2,new_feature)
          new_feature_test= clf.apply(X_test)
          X_test_new=self.mergeToOne(X_test,new_feature_test)
          return X_train_new2,y_train_2,X_test_new,y_test

if __name__ = '__main__':
    pass