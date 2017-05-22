from feature_role.lda_role import Lda_Role
from reading.dataset import Dataset
from conf.configure import Configure
from reading.advertisement import Advertisement
import numpy as np


if __name__ == '__main__':
    data_set = Dataset(Configure.train_path, Configure.test_path)
    ad = Advertisement(Configure.ad_path)
    param = {'userID': 311729, 'appID': 420}
    role = Lda_Role()
    result = dict()
    for d in data_set.get_data_list():
        param = {'userID': d['userID'], 'appID': ad.get_value(d['creativeID'])['appID']}
        vec = role.run(param)
        clickDay = d['clickTime'] // 10000
        label = d['label']
        if label < 0:
            label = 0
        if clickDay not in result:
            result[clickDay] = dict()
            result[clickDay][0] = dict()
            result[clickDay][1] = dict()
            result[clickDay][0]['vec'] = np.zeros([len(vec)])
            result[clickDay][0]['include_c'] = 0
            result[clickDay][0]['exclude_c'] = 0
            result[clickDay][1]['vec'] = np.zeros([len(vec)])
            result[clickDay][1]['include_c'] = 0
            result[clickDay][1]['exclude_c'] = 0
        if param['userID'] not in role.user_appid_topic_for_user or param['appID'] not in role.user_appid_topic_for_appid:
            result[clickDay][label]['exclude_c'] += 1
        else:
            result[clickDay][label]['include_c'] += 1
            result[clickDay][label]['vec'] += vec
    fout = open('../../file/lda_test.csv', 'w')
    for day in result:
        for label in result[day]:
            d = result[day][label]
            fout.write('{},{},{},{}'.format(day, label, d['exclude_c'], d['include_c']))
            for x in d['vec'] / d['include_c']:
                fout.write(',{}'.format(x))
            fout.write('\n')
    fout.close()