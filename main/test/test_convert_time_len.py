import pandas as pd
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.dataset import Dataset
from reading.user import User
from reading.app import App
import numpy as np

if __name__ == '__main__':
    data_set = Dataset(Configure.train_path, Configure.test_path)

    result = np.zeros([32])
    result1 = np.zeros([32, 6])
    for d in data_set.get_data_list():
        clickTime = d['clickTime']
        _day = clickTime // 10000
        label = d['label']
        result[_day] += 1
        if label == 1:
            delta_day = (d['conversionTime'] - clickTime) // 10000
            result1[_day][delta_day] += 1
    result1 /= result1 + result.reshape([32, 1])

    for i in range(17, len(result1)):
        print('{},{}'.format(i, ','.join([str(v) for v in result1[i]])))