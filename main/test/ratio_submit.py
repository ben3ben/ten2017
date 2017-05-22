import pandas as pd
from conf.configure import Configure

if __name__ == '__main__':
    data = pd.read_csv('../../file/submit/submission_0.09883.csv')
    data['prob'] *= 0.98
    data['instanceID'] = data['instanceID'].astype(int)
    data.to_csv('../../file/submit/submission_ratio.csv', float_format='%.6f', index=False)