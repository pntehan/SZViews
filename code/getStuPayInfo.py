import pandas as pd
import numpy as np
import os


def getInfo():
    '''按学号获取一卡通数据'''
    data = pd.read_csv('../education_data/7_consumption.csv',
                       index_col='bf_StudentID')
    all_id = np.unique(data.index)
    for _id in all_id:
        pay_info = data.ix[_id]
        yield (pay_info, _id)


def getDayData(data, stu_id):
    '''获取学生每天数据'''
    if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
        data = data.set_index('DealTime')
        days = np.unique([x.split(' ')[0] for x in data.index])
        for day in days:
            aim_index = get_aimIndex(data, day)
            money = [abs(data.ix[x]['MonDeal']) for x in aim_index]
            time = [x.split(' ')[1] for x in aim_index]
            day_data = pd.DataFrame({'money': money}, index=time)
            day = day.replace('/', '-')
            if not os.path.exists('../files/pay/{}'.format(stu_id)):
                os.makedirs('../files/pay/{}'.format(stu_id))
            day_data.to_csv('../files/pay/{}/{}.csv'.format(stu_id, day))
    else:
        money = [abs(data['MonDeal'])]
        time = [data['DealTime']]
        day = data['DealTime'].split(' ')[0].replace('/', '-')
        day_data = pd.DataFrame({'money': money}, index=time)
        if not os.path.exists('../files/pay/{}'.format(stu_id)):
            os.makedirs('../files/pay/{}'.format(stu_id))
        day_data.to_csv('../files/pay/{}/{}.csv'.format(stu_id, day))


def get_aimIndex(data, day):
    aim_index = []
    for i in data.index:
        if i.split(' ')[0] == day:
            aim_index.append(i)
    return aim_index


if __name__ == '__main__':
    f = getInfo()
    while True:
        try:
            info = next(f)
        except:
            break
        print('>>>>>>正在写入{}的消费记录...'.format(info[1]))
        getDayData(info[0], info[1])
        print('>>>>>>{}的消费记录写入完成!'.format(info[1]))
