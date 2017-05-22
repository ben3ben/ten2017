import sys

sys.path.append('../..')
import lda
import numpy as np
import pandas as pd
from conf.configure import Configure
from model.func import logloss
from scipy import sparse
from sklearn.metrics import roc_auc_score


def generate_matrix(row, column):
    row_index = list(set(row))
    column_index = list(set(column))
    matrix = sparse.lil_matrix((len(row_index), len(column_index)), dtype=np.int)
    row_dict = dict(zip(row_index, range(len(row_index))))
    column_dict = dict(zip(column_index, range(len(column_index))))
    # print(len(row),len(column),len(row_index),len(column_index))
    for i in range(len(row)):
        matrix[row_dict[row[i]], column_dict[column[i]]] += 1
    return (row_index, column_index, matrix)


def output_result(filepath, idx, ndz):
    f = open(filepath, 'w')
    for i in range(len(idx)):
        f.write(str(idx[i]))
        f.write(',')
        for j in range(len(ndz[i])):
            if j > 0:
                f.write(',')
            f.write(str(ndz[i][j]))
        f.write('\n')
    f.close()


def cos(vector1, vector2):
    dot_product = 0.0;
    normA = 0.0;
    normB = 0.0;
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


def normalization(array):
    result = [[(x / row.sum()) for x in row] for row in array]
    return np.array(result)


def generate_lda_input(train_ad, actions_data, installed_data, time):
    train_ad = train_ad[(train_ad['label'] == 1) & (train_ad['clickTime'] < time)]
    user_list = train_ad['userID'].tolist()
    appID_list = train_ad['appID'].tolist()
    actions_data = actions_data[actions_data['installTime'] < time]
    user_list.extend(actions_data['userID'].tolist())
    appID_list.extend(actions_data['appID'].tolist())
    user_list.extend(installed_data['userID'].tolist())
    appID_list.extend(installed_data['appID'].tolist())
    result = generate_matrix(user_list, appID_list)
    return result


def output_lda_distribute(input, n_topics, filepath1, filepath2):
    model = lda.LDA(n_topics=n_topics, n_iter=500, random_state=1)
    model.fit(input[2])
    doc_topic = model.doc_topic_.round(decimals=4)
    word_topic = model.topic_word_.T
    word_topic_normalized = normalization(word_topic).round(decimals=4)
    output_result(filepath1, input[0], doc_topic)
    output_result(filepath2, input[1], word_topic_normalized)


def output_cos(data, distribute, filepath, time):
    data = data[(data['clickTime'] >= time) & (data['userID'].isin(list(distribute[0].keys()))) & (
        data['appID'].isin(list(distribute[1].keys())))]
    f = open(filepath, 'w')
    for i in range(2):
        sum = 0
        num = 0
        for index, row in data[data['label'] == i].iterrows():
            sum += cos(distribute[0][row['userID']], distribute[1][row['appID']])
            num += 1
        f.write('label:' + str(i) + '\t' + str(round((sum / num), 4)) + '\n')
    f.close()


def loss(data, distribute, filepath, time):
    f = open(filepath, 'w')
    data = data[(data['clickTime'] >= time) & (data['userID'].isin(list(distribute[0].keys()))) & (
        data['appID'].isin(list(distribute[1].keys())))]
    labels = data['label'].tolist()
    pred = [cos(distribute[0][row['userID']], distribute[1][row['appID']]) for index, row in data.iterrows()]
    f.write('logloss: ' + str(round(logloss(labels, pred), 4)))
    f.close()


def auc(data, distribute, filepath, time):
    f = open(filepath, 'w')
    data = data[(data['clickTime'] >= time) & (data['userID'].isin(list(distribute[0].keys()))) & (
        data['appID'].isin(list(distribute[1].keys())))]
    labels = data['label'].tolist()
    pred = [cos(distribute[0][row['userID']], distribute[1][row['appID']]) for index, row in data.iterrows()]
    f.write('auc: ' + str(round(roc_auc_score(labels, pred), 4)))
    f.close()


def output_list(data, distribute, filepath, time):
    f = open(filepath, 'w')
    data = data[(data['clickTime'] >= time) & (data['userID'].isin(list(distribute[0].keys()))) & (
        data['appID'].isin(list(distribute[1].keys())))]
    labels = data['label'].tolist()
    pred = [cos(distribute[0][row['userID']], distribute[1][row['appID']]) for index, row in data.iterrows()]
    for i in range(len(labels)):
        f.write(str(labels[i]))
        f.write(',')
        f.write(str(pred[i]))
        f.write('\n')
    f.close()


def read_distribute(filepath1, filepath2):
    user = pd.read_csv(filepath1, header=None)
    app = pd.read_csv(filepath2, header=None)
    user_index = user.iloc[:, 0].tolist()
    app_index = app.iloc[:, 0].tolist()
    doc_topic = user.iloc[:, 1:].as_matrix()
    word_topic = app.iloc[:, 1:].as_matrix()
    return (dict(zip(user_index, doc_topic)), dict(zip(app_index, word_topic)))


def run(time):
    print('start reading')
    train_data = pd.read_csv(Configure.train_path)
    ad_data = pd.read_csv(Configure.ad_path)
    actions_data = pd.read_csv(Configure.user_app_actions_path)
    installed_data = pd.read_csv(Configure.user_installedapps_path)
    train_ad = pd.merge(train_data, ad_data, on='creativeID')
    filepath1 = 'user_topic_action_' + str(time) + '.csv'
    filepath2 = 'appID_topic_action_' + str(time) + '.csv'
    print('start generating input')
    input_matrix = generate_lda_input(train_ad, actions_data, installed_data,time * 10000)
    print('start lda')
    output_lda_distribute(input_matrix, 30, filepath1, filepath2)
    distribute = read_distribute(filepath1, filepath2)
    print('start cos')
    output_cos(train_ad, distribute, 'cos_action_' + str(time) + '.txt', time * 10000)
    print('start loss')
    loss(train_ad, distribute, 'log_loss_action_' + str(time) + '.txt', time * 10000)
    print('start auc')
    auc(train_ad, distribute, 'auc_action_' + str(time) + '.txt', time * 10000)
    print('label-pred list')
    output_list(train_ad, distribute, 'labelPred_list_' + str(time) + '.csv', time * 10000)


if __name__ == '__main__':
    run(28)
