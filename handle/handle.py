def delta_time(ta, tb):
    if ta < tb:
        print('may be error in func delta_time')
        exit()
    _min = ta % 100 - tb % 100
    _hour = ta // 100 % 100 - tb // 100 % 100
    _day = ta // 10000 - tb // 10000
    return  _day * 24 * 60 + _hour * 60 + _min

def submit_file(instanceIDs, prediction, path):
    instanceIDs, prediction = (list(t) for t in zip(*sorted(zip(instanceIDs, prediction))))
    fout = open(path, 'w')
    fout.write('instanceID,prob\n')
    for id, pred in zip(instanceIDs, prediction):
        fout.write('{0:},{1:0.6f}\n'.format(id, pred))
    fout.close()

def output_instanceID(ids, path):
    fout = open(path, 'w')
    for v in ids:
        print(v, file=fout)
    fout.close()

def output_feature_names(fea_names, path):
    fout = open(path, 'w')
    for v in fea_names:
        print(v, file=fout)
    fout.close()

def read_feature_names(path):
    fin = open(path)
    result = list()
    for line in fin:
        result.append(line.strip())
    fin.close()
    return result

def read_instanceID(path):
    fin = open(path)
    result = list()
    for line in fin:
        result.append(int(line))
    fin.close()
    return result

def prediction_to_file(instanceIDs, labels, prediction, path):
    instanceIDs, labels, prediction = (list(t) for t in zip(*sorted(zip(instanceIDs, labels, prediction))))
    fout = open(path, 'w')
    fout.write('instanceID,label,prob\n')
    for id, label, pred in zip(instanceIDs, labels, prediction):
        fout.write('{0:},{1:0.1f},{2:0.6f}\n'.format(id, label, pred))
    fout.close()

def handle_correlate_to_vec(correlate, dlist, cond_name, cond, clickDay):
    _k2 = -1
    _pro = -1
    max_pro = -1
    avg_pro = 0
    weight_pro = -1
    c_pro = 0
    pro_list = []
    n_list = []
    '''abcd limit'''
    low_limit = [100, 500, 1000, 5000, 10000, 20000]
    prod_limit = [-1] * len(low_limit)
    for record in dlist:
        if record['clickTime'] >= clickDay:
            break
        da = cond
        db = record[cond_name]
        if da not in correlate or db not in correlate[da]:
            continue
        d, c, b, a = correlate[da][db]
        n = a + b + c + d
        m = (a + b) * (c + d) * (a + c) * (b + d)
        k2 = n * (a * d - b * c) ** 2 / m if m > 0 else 0.0
        pro = (b / (b + d) if b > 0 else 0) if record['label'] == 0 else (a / (a + c) if a > 0 else 0)
        max_pro = max(max_pro, pro)
        avg_pro += pro
        pro_list.append(pro)
        n_list.append(b + d if record['label'] == 0 else a + c)
        c_pro += 1
        if k2 > _k2:
            _k2 = k2
            _pro = pro
        '''limit a+b+c+d'''
        for i in range(len(low_limit)):
            if low_limit[i] <= n and pro > prod_limit[i]:
                prod_limit[i] = pro
    avg_pro = avg_pro / c_pro if c_pro > 0 else -1
    if len(pro_list) > 0:
        _sum = sum(n_list)
        n_list = [v / _sum if _sum > 0 else 0 for v in n_list]
        weight_pro = 0
        for a, b in zip(pro_list, n_list):
            weight_pro += a * b
    result = [_k2, _pro, _k2 * _pro, max_pro, avg_pro, weight_pro]
    result.extend(prod_limit)
    return result


def select_columns(data, erase):
    result = data
    fea_names = list()
    columns_index = list()
    for index, fea in enumerate(data['feature_names']):
        if fea not in erase:
            fea_names.append(fea)
            columns_index.append(index)
    result['features'] = data['features'][:, columns_index]
    result['feature_names'] = fea_names
    return result
