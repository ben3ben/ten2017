import xgboost as xgb
import numpy as np


if __name__ == '__main__':
    X = np.zeros([500000, 200])
    Y = np.zeros([500000])
    a = xgb.DMatrix(X, Y)
    b = a.slice([1,1, 1])
    print(b.num_row())
    print(a, verbose=True)