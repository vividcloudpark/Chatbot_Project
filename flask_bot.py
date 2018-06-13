import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import connections as cnnt
from flask_models import *
import datetime

user, password, host, port, DB = cnnt.aws_basic_info()

target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = target
db = SQLAlchemy(app)
default_button_list = ["관객수 그래프 보기", "현재상영작 보기", "개봉예정작 보기", "장르별 현재상영작", "평점순 현재상영작"]


@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type" : "buttons",
        "buttons" : default_button_list
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    user_key = dataReceive['user_key']
    content = dataReceive['content']
    save_message = KakaoMessage(user_key,content)
    db.session.add(save_message)
    db.session.commit()

    if content == u"관객수 그래프 보기":
        dataSend = {
            "message": {
                "text": f"{user_key}님, 행복하세요."
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":default_button_list
            }

        }
    elif content == u"현재상영작 보기":
        dataSend = {
            "message": {
                "text": "현재상영작 보기"
            }
        }

    elif content == u"개봉예정작 보기":
        dataSend = {
            "message": {
                "text": "개봉예정작 보기"
            }
        }

    elif content == u"장르별 현재상영작":
        dataSend = {
            "message": {
                "text": "장르별 현재상영작"
            }
        }

    elif content == u"평점순 현재상영작":
        dataSend = {
            "message": {
                "text": "장르별 현재상영작"
            }
        }


    elif u"누구냐" in content:
        dataSend = {
            "message": {
                "text": "뭠마"
            }
        }
    else:
        dataSend = {
            "message": {
                "text": "죄송합니다ㅠ 문송해서 인식할수가 없습니다 ㅋㅋㅋ"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":default_button_list
            }
        }

    return jsonify(dataSend)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
