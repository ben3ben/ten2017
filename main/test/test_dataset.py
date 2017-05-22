import pandas as pd
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.dataset import Dataset
from reading.user import User
from reading.app import App

if __name__ == '__main__':
    data_set = pd.read_csv(Configure.train_path)
    test = pd.read_csv(Configure.test_path)
    data_set = data_set.append(test)

    data = data_set
    data['label'] = data['label'].replace(-1, 0)
    print(data)
    data['day'] = data['clickTime'] // 10000
    data['label_0'] = data['label'] == 0
    data['label_1'] = data['label'] == 1
    data = data[['day', 'label_0', 'label_1']]
    g = data.groupby(['day']).sum().reset_index()
    # for (appCategoru, hour, label), df in g:
    #     print(appCategoru, hour, label, df)
    print(g)