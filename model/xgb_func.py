import numpy as np
from model.func import *


def evalerror(preds, dtrain):
    labels = dtrain.get_label()
    # preds = 1.0 / (1.0 + np.exp(-preds))
    return 'logerror', logloss(labels, preds)


def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0 - preds)
    return grad, hess


def xgb_feature_importance(bst, feature_names):
    fi_gain = bst.get_score(importance_type='gain')
    fi_weight = bst.get_score(importance_type='weight')
    fi_cover = bst.get_score(importance_type='cover')
    feature_importance = dict()
    for key in feature_names:
        if key not in feature_importance:
            feature_importance[key] = dict()
        feature_importance[key]['gain'] = fi_gain[key] if key in fi_gain else 0
        feature_importance[key]['weight'] = fi_weight[key] if key in fi_weight else 0
        feature_importance[key]['cover'] = fi_cover[key] if key in fi_cover else 0
    return feature_importance
