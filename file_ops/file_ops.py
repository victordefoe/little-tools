# encoding: utf-8
'''
@Author: 刘琛
@Time: 2018/10/23 2:13
@Contact: victordefoe88@gmail.com

@File: file_ops.py
@Statement:

'''

import os
import shutil
from pprint import pprint
from sklearn.svm import SVC

def create_list(dir, set=None):
    if set == None:
        set = 'train'
    allfiles = os.listdir(dir)
    with open('./%slist.txt' % set, 'w') as f:
        for file in allfiles:
            path = os.path.join(dir, file)
            label = file.split('_')[0]
            f.write('%s %s \n' % (path, label))




if __name__ == '__main__':
    # create_list('D:/destbin/help/Everyone_data/deal/data_all/format/all/train/')
    path = 'D:/work-201810-28/faster_rcnn_pytorch-master/faster_rcnn_pytorch-master/data/text2018/TEXT2018/raw/ann/'
    error = 'D:/work-201810-28/faster_rcnn_pytorch-master/faster_rcnn_pytorch-master/data/text2018/TEXT2018/raw/error/'
    all = os.listdir(path)

    errorlist = []
    emptylist = []
    for each in all:
        with open(os.path.join(path, each), 'r') as f:
            cont = f.readlines()

            try:
                for ix, obj in enumerate(cont):
                    bbox = [float(x) for x in obj.strip().split(',')[:8]]

            except Exception as e:
                # print('error:', e, each)
                for every in cont:
                    if every.strip() == '':
                        cont.remove(every)
                errorlist.append(each)
                with open(os.path.join(error, each), 'w') as fid:
                    fid.writelines(cont)












