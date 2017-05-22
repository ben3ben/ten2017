import pandas as pd
from conf.configure import Configure
from model.func import logloss


if __name__ == '__main__':
    major = dict()
    major['train'] = pd.read_csv(Configure.xgb_model_file['train'])
    major['test'] = pd.read_csv(Configure.xgb_model_file['test'])
    diff = dict()
    diff['train'] = pd.read_csv(Configure.xgb_diff_model_file['train'])
    diff['test'] = pd.read_csv(Configure.xgb_diff_model_file['test'])

    diff_index = diff['train']['instanceID'].isin(major['train']['instanceID'])
    diff['train'] = diff['train'][diff_index]

    fout = open('fusion_result.txt', 'w')
    fout.write('r1,r2,train_loss,test_loss\n')
    for r in range(0, 101):
        ratio1 = r / 100
        ratio2 = 1 - ratio1
        pred_train = ratio1 * major['train']['prob'].as_matrix() + ratio2 * diff['train']['prob'].as_matrix()
        pred_test = ratio1 * major['test']['prob'].as_matrix() + ratio2 * diff['test']['prob'].as_matrix()
        # print('pred_train :', len(pred_train), '\tmajor :', len(major['train']['label']))
        train_logloss = logloss(major['train']['label'], pred_train)
        test_logloss = logloss(diff['test']['label'], pred_test)
        print('{0:0.2f},{1:0.2f},{2:},{3:}'.format(ratio1, ratio2, train_logloss, test_logloss))
        print('{0:0.2f},{1:0.2f},{2:},{3:}'.format(ratio1, ratio2, train_logloss, test_logloss), file=fout)
    fout.close()



