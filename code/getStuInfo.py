import os
import pandas as pd
import numpy as np
import json

data = pd.read_csv('../education_data/2_student_info.csv', index_col='bf_StudentID')
data2 = pd.read_csv('../education_data/1_teacher.csv', index_col='cla_id')

ids = np.unique(data.index)

for _id in ids:
	stu_data = data.loc[_id].fillna('empty')
	stu_info = dict(zip(stu_data.index, stu_data.values))
	for key, value in stu_info.items():
		if key == 'bf_zhusu':
			if value == 'empty':
				stu_info[key] = '不住校'
			elif value == 1.0:
				stu_info[key] = '住校'
		else:
			if value == 'empty':
				stu_info[key] = '无'
	cls_id = stu_info['cla_id']
	stu_info['cla_id'] = str(cls_id)
	if not cls_id in data2.index:
		print('>>>>>>>开始写入{}的学生信息...'.format(_id))
		with open('../files/stuinfo/{}.json'.format(_id), 'w') as fp:
			json.dump(stu_info, fp)
		print('>>>>>>>{}的学生信息已写入...'.format(_id))
	else:
		cla_data = data2.loc[cls_id]
		if str(type(cla_data)) == "<class 'pandas.core.series.Series'>":
			stu_info['cla_Name'] = cla_data.cla_Name
			stu_info['teacher'] = cla_data.sub_Name + cla_data.bas_Name
		else:
			stu_info['cla_Name'] = cla_data.cla_Name.values[0]
			sub = cla_data.sub_Name.values
			teacher = cla_data.bas_Name.values
			word = ''
			for i in range(len(cla_data)):
				word = word + sub[i] + teacher[i] + ' '
			stu_info['teacher'] = word
		print('>>>>>>>开始写入{}的学生信息...'.format(_id))
		with open('../files/stuinfo/{}.json'.format(_id), 'w') as fp:
			json.dump(stu_info, fp)
		print('>>>>>>>{}的学生信息已写入...'.format(_id))
	# exit(0)
	








