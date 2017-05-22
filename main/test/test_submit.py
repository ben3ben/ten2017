import pandas as pd
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.dataset import Dataset
from reading.user import User
from reading.app import App
import numpy as np


if __name__ == '__main__':
    submit = pd.read_csv(Configure.submission)
    test = pd.read_csv(Configure.test_path)
    ad = pd.read_csv(Configure.ad_path)
    app = pd.read_csv(Configure.app_categories_path)

    data = submit.merge(test, how='left', on='instanceID')
    data = data.merge(ad, how='left', on='creativeID')
    data = data[data['appID'] == 389]
    print(data['prob'])
    print(np.average(data['prob']))
    # for (appCategoru, hour, label), df in g:
    #     print(appCategoru, hour, label, df)