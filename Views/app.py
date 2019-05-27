from flask import Flask, render_template, request
from function import *

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():
    '''主页'''
    return render_template('home.html')

@app.route('/student', methods={'POST', 'GET'})
def search_stu():
    '''搜索学生信息页面'''
    return render_template('searchStu.html')

@app.route('/studentDo', methods={'POST'})
def studentdo():
    '''从文件中查找学生信息'''
    image_url = searchStu()
    return render_template('student.html', info=image_url)

@app.route('/class', methods={'POST', 'GET'})
def search_cls():
    pass

@app.route('/classDo', methods={'POST', 'GET'})
def classdo():
    pass

@app.route('/student-<int:student_id>', methods={'POST', 'GET'})
def studentinfo(student_id):
    '''学生画像展示'''
    info = get_stuInfo(student_id)
    return render_template('studentInfo.html', info=info)

@app.route('/score-<int:student_id>', methods={'POST', 'GET'})
def studentScore(student_id):
    '''学生成绩分析'''
    scoreInfo = get_sub(student_id)
    return render_template('score.html', scoreInfo=scoreInfo, stuID=student_id)

@app.route('/<int:stu_id>score<string:sub>')
def scoresub(stu_id, sub):
    data = get_stuScore(stu_id, sub)
    return render_template('3Dscore.html', data=data, sub=sub, stuID=stu_id)

@app.route('/kaoqin-<int:stu_id>')
def kaoqin(stu_id):
    '''学生考勤画像展示'''
    info = get_stuKaoqin(stu_id)
    return render_template('kaoqin.html', info=info)

@app.route('/pay-<int:stu_id>')
def pay(stu_id):
    '''学生考勤画像展示'''
    info, image_url = get_stuPay(stu_id)
    return render_template('pay.html', info=info, img=image_url)

@app.route('/subject', methods={'POST', 'GET'})
def sub():
    '''搜索课程信息页面'''
    return render_template('searchSub.html')

@app.route('/Class', methods={'POST', 'GET'})
def banji():
    '''搜索班级信息页面'''
    return render_template('searchCla.html')


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=80)
