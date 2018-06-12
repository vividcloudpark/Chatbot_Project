import os
from flask import Flask, request, jsonify
import pymysql
import connections as cnnt
from models import *
import datetime

app = Flask(__name__)

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
    session = cnnt.cursor()[2]
    user_key = dataReceive['user_key']
    content = dataReceive['content']
    save_message = KakaoMessage(user_key,message)
    session.add(save_message)
    session.commit()
    session.close()


    if content == u"관객수 그래프 보기":
        dataSend = {
            "message": {
                "text": f"{user}님, 행복하세요."
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
