import pandas as pd
import numpy as np
from word_cloud import drawCloud
import json


def get_StuInfo():
    '''获取单个学生考勤数据'''
    data = pd.read_csv('../education_data/3_kaoqin.csv',
                       index_col='bf_studentID')
    all_id = np.unique(data.index)
    for _id in all_id[:1871]:
        info = data.loc[_id]
        result = analysisInfo(info)
        # word = ''
        # for key, value in result.items():
        #     word = word + (key + ' ') * value
        # yield (word, _id)
        yield (result, _id)
        # exit(0)


def analysisInfo(data):
    '''学生考勤信息分析'''
    result = {}
    data = data.fillna('0')
    label = {
        '迟到': [1001, 100100, 100200, 99001],
        '没穿校服': [200100, 99002],
        '早退': [1002],
        '请假': [200200, 300200],
        '正常考勤': [99004, 99005, 9900500, 9900400, 1003],
        '住宿晨练': [300100]
    }
    if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
        c_id = data['ControllerID'].values
        c_task_order_id = data['control_task_order_id'].values
        all_days = len(np.unique(data['qj_term'].values)) * 130
    else:
        c_id = [data['ControllerID']]
        c_task_order_id = [data['control_task_order_id']]
        all_days = 130
    for i in c_id:
        for key, value in label.items():
            if i in value:
                if not key in result.keys():
                    result[key] = 1
                else:
                    result[key] += 1
        all_days -= 1
    for i in c_task_order_id:
        for key, value in label.items():
            if i in value:
                if not key in result.keys():
                    result[key] = 1
                else:
                    result[key] += 1
        all_days -= 1
    result['到勤'] = all_days
    return result


if __name__ == '__main__':
    f = iter(get_StuInfo())
    while True:
        try:
            info = next(f)
            # print('>>>>>>>>开始绘制{}的考勤画像...'.format(info[1]))
            # drawCloud(word=info[0], img='../wordCloud/day.jpg',
            #           output='../image/studentAttence/{}.jpg'.format(info[1]))
            # print('>>>>>>>>{}的考勤画像绘制完毕...'.format(info[1]))
            print('>>>>>>>开始写入{}的考勤信息...'.format(info[1]))
            with open('../files/kaoqin/{}.json'.format(info[1]), 'w') as fp:
                json.dump(info[0], fp)
                print('>>>>>>>{}的考勤信息已写入...'.format(info[1]))
        except:
            break
