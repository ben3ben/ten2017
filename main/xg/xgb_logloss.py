import pandas as pd
from conf.configure import Configure
from model.func import logloss


if __name__ == '__main__':
    train = pd.read_csv(Configure.xgb_model_file['train'])
    test = pd.read_csv(Configure.xgb_model_file['test'])
    print(logloss(train['label'], train['prob']))
    print(logloss(test['label'], test['prob']))
