def submit_file(instanceIDs, prediction, path):
    instanceIDs, prediction = (list(t) for t in zip(*sorted(zip(instanceIDs, prediction))))
    fout = open(path, 'w')
    fout.write('instanceID,prob\n')
    for id, pred in zip(instanceIDs, prediction):
        fout.write('{0:},{1:0.6f}\n'.format(id, pred))
    fout.close()
