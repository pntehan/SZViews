from word_cloud import drawCloud
from drawScaPic import drawScatter
import pandas as pd
import numpy as np
from datetime import datetime
import os


def getInfo():
    '''按学号获取一卡通数据'''
    data = pd.read_csv('../education_data/7_consumption.csv',
                       index_col='bf_StudentID')
    all_id = np.unique(data.index)
    for _id in all_id:
        pay_info = data.ix[_id]
        yield (pay_info, _id)


def drawPay(data, output, _id):
    '''消费画像'''
    if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
        money = ''
        for i in data['MonDeal'].values:
            money += '消费' + str(int(abs(i))) + '元'
            money += ' '
        ID = ''
        for i in data.index:
            ID += '学号' + str(i)
            ID += ' '
        Name = ''
        for i in data['AccName'].values:
            Name += i
            Name += ' '
        Sex = ''
        for i in data['PerSex'].values:
            Sex += i
            Sex += ' '
        info = money + ID + Name + Sex
    else:
        money = '消费' + str(int(abs(data['MonDeal']))) + '元'
        ID = '学号' + str(_id)
        name = data['AccName']
        sex = data['PerSex']
        info = money + ' ' + ID + ' ' + name + ' ' + sex
    drawCloud(word=info, img='../wordCloud/Pay.jpg', output=output)


def drawPayBar(data, _id):
    '''绘制消费散点图'''
    if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
        data = data.set_index('DealTime')
        days = np.unique([x.split(' ')[0] for x in data.index])
        result = []
        for day in days:
            aim_index = dayPaydata(data, day)
            money = [abs(data.ix[i]['MonDeal']) for i in aim_index]
            result.append({'time': aim_index, 'data': money})
    else:
        money = [abs(data['MonDeal'])]
        time = [data['DealTime']]
        day = data['DealTime'].split(' ')[0].replace('/', '-')
    drawScatter(result, output='')


def dayPaydata(data, day):
    '''返回一天消费记录的数组'''
    aim_index = []
    for i in data.index:
        if i.split(' ')[0] == day:
            aim_index.append(i)
    return aim_index


if __name__ == '__main__':
    f = getInfo()
    # while True:
    #     try:
    #         info = next(f)
    #     except:
    #         break
    #     print('正在绘制{}的消费画像...'.format(info[1]))
    #     drawPay(
    #         info[0], output='../image/studentPay/{}.jpg'.format(info[1]), _id=info[1])
    #     print('{}的消费画像绘制完毕...'.format(info[1]))
    while True:
        try:
            info = next(f)
        except:
            break
        print('正在绘制{}的消费散点图...'.format(info[1]))
        if not os.path.exists('../image/studentPayInfo/{}'.format(info[1])):
            os.makedirs('../image/studentPayInfo/{}'.format(info[1]))
        drawPayBar(data=info[0], _id=info[1])
        print('{}的消费散点图绘制完毕...'.format(info[1]))
        exit(0)
