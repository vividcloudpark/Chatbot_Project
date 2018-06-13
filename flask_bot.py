import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import connections as cnnt
from flask_models import *
import datetime
import show_movie_trend as smt

user, password, host, port, DB = cnnt.aws_basic_info()

target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'


def make_movie_list():
    curs = cnnt.mk_cursor()
    sql = """SELECT movie_name_kor FROM DBtoday.BaseMovieInfo"""
    a = curs.execute(sql)
    sqlresult = curs.fetchall()
    curs.close()
    temp_list = []
    for i in sqlresult:
        temp_list.append(i[0])
    return temp_list


movie_list = make_movie_list()

def make_last_msg(user_key):
    curs = cnnt.mk_cursor()
    try:
        sql =f'''SELECT * FROM DBtoday.KakaoMessage as KM Where user_key = '{user_key}' order by KM.timestamp desc, KM.index desc limit 1;'''
        a = curs.execute(sql)
        sqlresult = curs.fetchone()
        curs.close()
        print(sqlresult[3])
        return sqlresult[3]
    except:
        return None



def movie_detail_info(user_movie_name):
    curs = cnnt.mk_cursor()
    sql=f'''
    SELECT bmi.movie_code, bmi.movie_name_kor as '제목',dir.director_name_kor as '감독',dbmi.opendate as '개봉일',dbmi.flim_class as '관람가',dbmi.story as '개요'
    FROM BaseMovieInfo as bmi
    left join DetailedBaseMovieInfo as dbmi
    on bmi.movie_code=dbmi.movie_code
    left join DirectorOfMovie as dof
    on dof.movie_code=bmi.movie_code
    left join Director as dir
    on dof.movie_director_code=dir.director_code
    where movie_name_kor="{user_movie_name}"'''
    a = curs.execute(sql)
    sqlresult=curs.fetchone()
    curs.close()
    moviecode,title,director,opendate,viewer,story = sqlresult


    sql2=f'''SELECT bmi.movie_name_kor as '제목',act.actor_name_kor as '출연자'
    from BaseMovieInfo as bmi
    inner join ActorsOfMovie as aom
    on aom.movie_code=bmi.movie_code
    inner join Actors as act
    on aom.movie_actor_code=act.actor_code
    where movie_name_kor="{user_movie_name}"'''

    curs = cnnt.mk_cursor()
    b = curs.execute(sql2)
    sql2result=curs.fetchall()
    curs.close()

    actorlist = []
    for i in range(len(sql2result)):
        actorlist.append(sql2result[i][1])
    finalactor = ", ".join(actorlist)

    curs = cnnt.mk_cursor()
    sql3=f'''
    SELECT bmi.movie_name_kor as '제목', gn.genre as '장르'
    from BaseMovieInfo as bmi
    inner join GenreOfMovie as gom
    on gom.movie_code=bmi.movie_code
    inner join Genre as gn
    on gn.genre=gom.movie_genre
    where movie_name_kor="{user_movie_name}"'''

    c = curs.execute(sql3)
    sql3result=curs.fetchall()
    curs.close()
    genrelist = []
    for i in range(len(sql3result)):
        genrelist.append(sql3result[i][1])
    finalgenre = ",".join(genrelist)

    return moviecode,title,director,opendate,viewer,story,finalactor,finalgenre

def find_by_score():
    curs = cnnt.mk_cursor()
    sql = '''
    SELECT ba.movie_name_kor,
    CASE WHEN viewer_score = 0 THEN round(ntz_score,2)
    ELSE round((ntz_score+viewer_score)/2,2)
    END AS average_score, giza_score
        FROM DBtoday.MovieScore as ms
        INNER JOIN BaseMovieInfo as ba
        ON ms.movie_code = ba.movie_code
        INNER JOIN DetailedBaseMovieInfo as dm
        ON dm.movie_code = ms.movie_code
        WHERE date(dm.opendate) > date_add(date(now()), interval -1 month)
        Order by average_score DESC
        LIMIT 10'''
    a = curs.execute(sql)
    sqlresult = curs.fetchall()
    curs.close()
    stringlist = []
    namelist = []
    for number, i in enumerate(sqlresult):
        name, mean_score, giza = i[0], i[1], i[2]
        namelist.append(name)
        string = f"{number+1}위 : {name} | 평균평점 : {mean_score} | 기자평점 : {giza} \n"
        stringlist.append(string)
    final_string = "".join(stringlist)
    return namelist, final_string

def currently_or_future_showing_movie(parameter):
    if parameter == "curr":
        banghang = "<"
    else:
        banghang = ">"

    curs =cnnt.mk_cursor()
    sql=f'''
    SELECT bmi.movie_code, bmi.movie_name_kor, dbmi.opendate, sc.ntz_score
    FROM BaseMovieInfo as bmi
   inner join DetailedBaseMovieInfo as dbmi
      on bmi.movie_code = dbmi.movie_code
	inner join MovieScore as sc
		on bmi.movie_code = sc.movie_code
   inner join DirectorOfMovie as dom
      on dom.movie_code = bmi.movie_code
      where
      (dbmi.opendate {banghang} date(now())) in (date(dbmi.opendate) > date_add(date(now()), interval -1 month))
order by opendate desc limit 10;
    '''
    a = curs.execute(sql)
    sqlresult = curs.fetchall()
    curs.close()
    contentslist = []
    namelist = []
    if banghang == ">":
        for i in sqlresult:
            name, opendate, score  = i[1], i[2], i[3]
            namelist.append(name)
            contents = f"{name} | 개봉 {opendate} | 평점  {score} \n"
            contentslist.append(contents)
        final_contents = "".join(contentslist)
    else:
        for i in sqlresult:
            name, opendate = i[1], i[2]
            namelist.append(name)
            contents = f"{name} | 개봉예정 {opendate}  \n"
            contentslist.append(contents)
        final_contents = "".join(contentslist)
    return namelist, final_contents

user, password, host, port, DB = cnnt.aws_basic_info()

target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'
movie_list = make_movie_list()

cur = cnnt.mk_cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = target
db = SQLAlchemy(app)
default_button_list = ["관객수 그래프 보기", "현재상영작 보기", "개봉예정작 보기", "평점순 현재상영작"]


@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type" : "buttons",
        "buttons" : default_button_list
    }

    return jsonify(dataSend)



def insert_trend(section):
    today = datetime.datetime.now().date()
    smt.insert_movie_audiance_num_per_date(today,section)
    section = datetime.timedelta(section)

    end_date = today - section 

    return smt.query_and_draw(today, end_date)


def draw_trend(section):
    today = datetime.datetime.now().date()
    section = datetime.timedelta(section)
    end_date = today - section
     
    today = today.strftime("%Y-%m-%d")
    end_date =  end_date.strftime("%Y-%m-%d")
    graph_buttons = ["일주일", "이주일", "한달"]

    return graph_buttons,today, end_date
    




def save_message(user_key, content):
    save_message = KakaoMessage(user_key,content)
    db.session.add(save_message)
    db.session.commit()
    db.session.close()
    return







@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    user_key = dataReceive['user_key']
    content = dataReceive['content']
    save_message(user_key, content)
    last_msg = make_last_msg(user_key)
    img_link = "https://raw.githubusercontent.com/vividcloudpark/Chatbot_Project/master/asset/image/{0}to{1}.png"


    if last_msg in movie_list:
        moviecode,title,director,opendate,viewer,story,finalactor,finalgenre = movie_detail_info(last_msg)
        naverlink = f"https://movie.naver.com/movie/bi/mi/basic.nhn?code={moviecode}"
        dataSend = {
            "message": {
                "text": f"제목 : {title} \n개봉일 : {opendate} \n감독 : {director} \n출연자 : {finalactor}  \n장르 : {finalgenre}\n등급 : {viewer} \n개요 :{story}\n상세링크:{naverlink}"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":default_button_list
            }

        }

    elif content == u"관객수 그래프 보기":
        graph_buttons,_,_ = draw_trend(5)
        dataSend = {
            "message": {
                "text": "며칠간격으로 그래프를 보여드릴까요?"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":graph_buttons
            }

        }
    elif content == u"일주일" :
        _,start_date,end_date = draw_trend(7)
        dataSend = {
                     "message" : {"text" : "일주일간 관객수 추이입니다(10위 이하였던 날짜, 미개봉이었던 날짜에는 데이터가 존재하지 않습니다)",
                     "photo":{"url" : img_link.format(start_date,end_date),
                     "width" : 720,
		      "height" : 630}},
                      "keyboard":{
                         "type": "buttons",
                         "buttons":default_button_list
            }

		   }

    elif content == u"이주일" : 
        _,start_date,end_date = draw_trend(14)
        dataSend = {
                     "message" : {"text" : "이주일간 관객수 추이입니다(10위 이하였던 날짜, 미개봉이었던 날짜에는 데이터가 존재하지 않습니다)",
                     "photo":{"url" : img_link.format(start_date,end_date),
                     "width" : 720,
                      "height" : 630}},
                      "keyboard":{
                         "type": "buttons",
                         "buttons":default_button_list
            }


                   }


    elif content == u"한달":
        _,start_date, end_date = draw_trend(30)
        dataSend = {
                     "message" : {"text" : "한달 간 관객수 추이입니다(10위 이하였던 날짜, 미개봉이었던 날짜에는 데이터가 존재하지 않습니다)",
                     "photo":{"url" : img_link.format(start_date,end_date),
                     "width" : 720,
                      "height" : 630}}, 
                      "keyboard":{
                         "type": "buttons",
                         "buttons":default_button_list
            }


                   }


    
    elif content == u"현재상영작 보기":
        namelist, final_contents = currently_or_future_showing_movie("curr")
        dataSend = {
            "message": {
                "text": f"{final_contents}"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":namelist
        }}

    elif content == u"개봉예정작 보기":
        namelist, final_contents = currently_or_future_showing_movie("future")
        dataSend = {
            "message": {
                "text": f"{final_contents}"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":namelist
        }}


    elif content == u"평점순 현재상영작":
        namelist, final_string = find_by_score()
        dataSend = {
            "message": {
                "text": f"{final_string}"
            },
            "keyboard":{
                "type": "buttons",
                    "buttons":namelist
        }}


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
