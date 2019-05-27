import pandas as pd
import numpy as np
from word_cloud import drawCloud
from tqdm import tqdm


def getImage():
    '''绘制图像'''
    all_informations = pd.read_csv(
        '../education_data/2_student_info.csv', index_col='bf_StudentID')
    for _id in all_informations.index:
        data = all_informations.ix[_id]
        if data['bf_sex'] == '男':
            img_path = '../wordCloud/boy.jpg'
        elif data['bf_sex'] == '女':
            img_path = '../wordCloud/girl.jpg'
        info = doData(data, _id) * 3
        # print(info)
        print('绘制学号为{}的图像...'.format(_id))
        drawCloud(word=info, img=img_path,
                  output='../image/studentPic/{}.jpg'.format(_id))
        print('图片已存在于{}...'.format('../image/studentPic/{}.jpg'.format(_id)))


def doData(data, _id):
    '''处理返回个人数据'''
    data = data.fillna(0)
    if data['bf_zhusu'] == 0:
        data.loc['bf_zhusu'] = '走读'
    else:
        data.loc['bf_zhusu'] = '住宿'
    if data['bf_leaveSchool'] == 0:
        data.loc['bf_leaveSchool'] = '在读'
    else:
        data.loc['bf_leaveSchool'] = '退学'
    if data['bf_qinshihao'] == 0:
        data.loc['bf_qinshihao'] = ''
    info = str(_id)
    for i in data.values:
        aim = (str(i) + ' ') * np.random.randint(10, 20)
        info += aim
    teachers = getTeacher(data['cla_id'])
    return info + ' ' + teachers


def getTeacher(clsID):
    '''获取学生信息'''
    teachers = pd.read_csv(
        '../education_data/1_teacher.csv', index_col='cla_id')
    try:
        aim = teachers.ix[clsID]['bas_Name']
        info = ''
        for i in aim.values:
            info += ' '
            info += ''.join(str(i))
        return info
    except:
        return ''


if __name__ == '__main__':
    getImage()
