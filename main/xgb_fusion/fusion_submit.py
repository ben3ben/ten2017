import pandas as pd
from conf.configure import Configure
from model.func import logloss
from handle.handle import submit_file


if __name__ == '__main__':
    major = dict()
    major['submit'] = pd.read_csv(Configure.xgb_model_file['submit'])
    diff = dict()
    diff['submit'] = pd.read_csv(Configure.xgb_diff_model_file['submit'])

    instanceIDs = major['submit']['instanceID']
    prediction = 1.0 * major['submit']['prob'] + 0.00 * diff['submit']['prob']
    submit_file(instanceIDs, prediction, Configure.submission)



