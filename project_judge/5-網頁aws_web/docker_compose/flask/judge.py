import uuid
from datetime import datetime
from pathlib import Path

from flask_moment import Moment

import crime_elements as ce
import model.load_model as model
from flask import Flask, render_template, request, url_for

app = Flask(__name__)


# ----------practice start------------
@app.route('/')
def index():
    return render_template("master.html")


@app.route('/information')
def information():
    return render_template("information.html")


@app.route('/member')
def member():
    return render_template("member.html")


@app.route('/dashboard')
def dashboard():
    return render_template("index.html")


@app.route('/chart')
def chart():
    return render_template("charts.html")


@app.route('/table')
def table():
    return render_template("tables.html")


# @app.route('/predict')
# def predict():
#     return render_template("predict.html")


@app.route('/predict', methods=['GET', 'POST'])
def get_para1():
    if request.method == "GET":
        return render_template('predict.html')
    elif request.method == "POST":

        select1 = request.form.get('傷害意圖')
        select2 = request.form.get('造成被害人受傷程度')
        select3 = request.form.get('傷害對象')
        cd = ce.element2Crime(select1, select2, select3)

        crimePredCategory = cd[0]  # 哪一個罪
        F_03 = request.form.get('傷害方式')
        F_04 = request.form.get('下手力道')
        F_06 = request.form.get('傷害結果')
        F_01 = request.form.get('教育程度')
        F_11 = request.form.get('被告身心狀況')
        F_14 = request.form.get('與被害人關係')
        F_02 = request.form.get('影響判決因素')
        F_13 = request.form.get('和解狀況')
        F_08 = request.form.get('坦承情況')
        F_07 = request.form.get('犯後態度')
        # return render_template('predict.html', predict = cd[1])

        crimeName, crimeTime = model.pred_crime(
            F_01, F_02, F_03, F_04, F_06, F_07, F_08, F_11, F_13, F_14, crimePredCategory)

        if crimeName == 0 or crimeTime == 0:
            crimeName = 0
            crimeTime = 6

        name = {
            0: '無罪',
            1: '過失傷害',
            2: '過失傷害致重傷',
            3: '傷害',
            4: '傷害致重傷',
            5: '傷害致死',
            6: '重傷害',
            7: '重傷害未遂',
            8: '重傷致死',
            9: '傷害直系血親尊親屬',
            10: '傷害直系血親尊親屬致死',
            11: '其他',
        }

        time = {
            0: '無罪',
            1: '拘役1-60天',
            2: '有期徒刑2-6個月',
            3: '有期徒刑半年-2年',
            4: '有期徒刑2-5年',
            5: '有期徒刑5年以上',
            6: ''
        }
        # time[crimeTime]

        # lawTime = {
        #     0: '',
        #     1: '../static/assets/img/過失傷害.png',
        #     2: '../static/assets/img/過失傷害.png',
        #     3: '../static/assets/img/傷害致重傷或死.png',
        #     4: '../static/assets/img/傷害致重傷或死.png',
        #     5: '../static/assets/img/傷害致重傷或死.png',
        #     6: '../static/assets/img/重傷害致重傷或死.png',
        #     7: '../static/assets/img/重傷害致重傷或死.png',
        #     8: '../static/assets/img/重傷害致重傷或死.png',
        #     9: '../static/assets/img/直系血親尊親屬.png',
        #     10: '../static/assets/img/直系血親尊親屬.png',
        #     11: '',
        # }

        lawTime = {
            0: 'T000.html',  # 無
            1: 'T284.html',  # 過失傷害
            2: 'T284.html',  # 過失傷害
            3: 'T277.html',  # 傷害
            4: 'T277.html',  # 傷害
            5: 'T277.html',  # 傷害
            6: 'T278.html',  # 重傷害
            7: 'T278.html',  # 重傷害
            8: 'T278.html',  # 重傷害
            9: 'T280.html',  # 傷直血
            10: 'T280.html',  # 傷直血
            11: 'T000.html'  # 無
        }

        return render_template('predict_result.html', predict1=name[int(crimeName)], predict2=time[int(crimeTime)], predict3=lawTime[int(crimeName)])


# @app.route('/')
# def block():
#     return render_template("navbar.html")
# #----------practice end--------------


if __name__ == "__main__":
    app.run(debug=True)
