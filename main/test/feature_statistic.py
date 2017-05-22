import xgboost as xgb
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed
from feature.dmatrix import DMatrix
import pandas as pd
import numpy as np
from handle.handle import *

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
    # train = dmatrix.run(Configure.train_begin_t, Configure.train_end_t, 'train')
    train = dmatrix.run(Configure.train_begin_t, Configure.train_end_t, 'train', ratio=1)
    train = select_columns(train, Configure.features_erase)
    p_train = pd.DataFrame(data=train['features'], columns=train['feature_names'])
    # p_train.to_csv(Configure.feature_files['train'], index=False)
    des_train = p_train.describe()
    des_train.T.to_csv(Configure.feature_files['train_describe'])
    del train
    del p_train
    print('generate test...')
    test = dmatrix.run(Configure.test_begin_t, Configure.test_end_t, 'train', ratio=1)
    test = select_columns(test, Configure.features_erase)
    p_test = pd.DataFrame(data=test['features'], columns=test['feature_names'])
    # p_test.to_csv(Configure.feature_files['test'], index=False)
    des_test = p_test.describe()
    des_test.T.to_csv(Configure.feature_files['test_describe'])
    del test
    del p_test
    print('generate submit...')
    submit = dmatrix.run(Configure.submit_begin_t, Configure.submit_end_t, 'train', ratio=1)
    submit = select_columns(submit, Configure.features_erase)
    p_submit = pd.DataFrame(data=submit['features'], columns=submit['feature_names'])
    # p_submit.to_csv(Configure.feature_files['submit'], index=False)
    des_submit = p_submit.describe()
    des_submit.T.to_csv(Configure.feature_files['submit_describe'])

    des_submit = des_submit.T
    des_test = des_test.T
    des_train = des_train.T
    des_submit['feature'] = des_submit.index
    des_test['feature'] = des_test.index
    des_train['feature'] = des_train.index
    des_submit = des_submit[['feature', 'count', 'mean', 'std']]
    des_test = des_test[['feature', 'count', 'mean', 'std']]
    des_train = des_train[['feature', 'count', 'mean', 'std']]
    des_submit = des_submit.rename(index=str, columns={"count": "count_submit", "mean": "mean_submit", "std": "std_submit"})
    des_test = des_test.rename(index=str, columns={"count": "count_test", "mean": "mean_test", "std": "std_test"})
    des_train = des_train.rename(index=str, columns={"count": "count_train", "mean": "mean_train", "std": "std_train"})

    description = des_submit.merge(des_test, how='left', on='feature')
    description = description.merge(des_train, how='left', on='feature')
    print(description)
    description['ratio_test_submit'] = (description['mean_test'] - description['mean_submit']) / description[
        'mean_submit']
    description['ratio_train_submit'] = (description['mean_train'] - description['mean_submit']) / description[
        'mean_submit']
    description['ratio_train_test'] = (description['mean_train'] - description['mean_test']) / description[
        'mean_test']
    description.to_csv('../../file/feature/description_feature.csv', index=False)
