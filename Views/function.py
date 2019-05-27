from flask import request
from glob import glob
import json
import os
import pandas as pd
import time
import numpy as np

np.random.seed(1)

Class = ['1B模块总分', '体育', '美术', '音乐', '通用技术', np.nan]

def searchStu():
    '''根据学号返回所有相关数据信息'''
    _id = request.form.get('searchStu')
    if not os.path.exists('./static/image/studentPic/{}.jpg'.format(_id)):
        stuPic = '不存在'
    else:
        stuPic = '/static/image/studentPic/{}.jpg'.format(_id)
    if not os.path.exists('./static/image/studentPay/{}.jpg'.format(_id)):
        stuPayPic = '不存在'
    else:
        stuPayPic = '/static/image/studentPay/{}.jpg'.format(_id)
    if not os.path.exists('./static/image/studentAttence/{}.jpg'.format(_id)):
        stuAttencePic = '不存在'
    else:
        stuAttencePic = '/static/image/studentAttence/{}.jpg'.format(_id)
    info = {'stuID':_id,
            'stuPic': stuPic,
            'stuPayPic': stuPayPic,
            'stuAttencePic': stuAttencePic}
    # print(info)
    return info

def get_stuInfo(stuID):
    '''根据学号返回学生个人信息'''
    with open("./data/stuinfo/{}.json".format(stuID), 'r') as load_f:
        load_dict = json.load(load_f)
    if load_dict['bf_qinshihao'] == '无':
        pass
    else:
        load_dict['bf_qinshihao'] = int(load_dict['bf_qinshihao'])
    info = {'stuID': stuID,
            'stuinfo': load_dict,
            'stuPic': '/static/image/studentPic/{}.jpg'.format(stuID)}
    return info

def get_stuKaoqin(stuID):
    '''根据学号返回考勤信息'''
    with open("./data/stukaoqin/{}.json".format(stuID), 'r') as load_f:
        load_dict = json.load(load_f)
    info = {'data': load_dict, 'pic': '/static/image/studentAttence/{}.jpg'.format(stuID)}
    return info

def get_stuPay(stuID):
    '''根据学号返回消费信息'''
    dirs = glob('./data/stupay/{}/*.csv'.format(stuID))
    info = {}
    for path in dirs:
        data = pd.read_csv(path, index_col='Unnamed: 0')
        day = path.split('/')[-1].split('.')[0]
        info[day] = {'data':[]}
        for i in range(len(data)):
            time = data.index[i].replace(':', '')[:-2]
            info[day]['data'].append([int(time), data.money[i]])
        info[day]['color'] = 'rgba({}, {}, {}, 0.5)'.format(np.random.randint(255), np.random.randint(255), np.random.randint(255))
    image_url = '/static/image/studentPay/{}.jpg'.format(stuID)
    # print(info)
    return info, image_url


def get_stuScore(stuID, subject):
    '''根据学号返回学生成绩'''
    dirs = glob('./data/stuScore/{}/*.csv'.format(stuID))
    all_score = {'exam':[], 'grade':[]}
    for path in dirs:
        score = pd.read_csv(path, index_col='Unnamed: 0')
        exam = list(score)[0]
        data = score[exam]
        for sub in data.index:
            if sub == subject:
                if data.loc[sub] < 0:
                    all_score['grade'].append(0)
                else:
                    all_score['grade'].append(data.loc[sub])
                all_score['exam'].append(exam)
    return all_score

def get_sub(stuID):
    '''获取学生的考试'''
    dirs = glob('./data/stuScore/{}/*.csv'.format(stuID))
    subs = []
    for path in dirs:
        score = pd.read_csv(path, index_col='Unnamed: 0')
        exam = list(score)[0]
        data = score[exam]
        for sub in data.index:
            if sub in Class:
                pass
            else:
                if not sub in subs:
                    subs.append(sub)
    return subs