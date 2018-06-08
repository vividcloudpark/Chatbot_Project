from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql
import pprint

def cursor():
    data=open("config.json").read()
    json_data = json.loads(data)

    user = json_data["users"][0]["user"]
    password = json_data["users"][0]["password"]
    host = json_data["users"][0]["host"]
    port = json_data["users"][0]["port"]
    DB = json_data["users"][0]["DB"]

    target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'

    engine = create_engine(target, encoding = "utf-8")
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = pymysql.connect(host=host, user=user, password=password,  charset='utf8')
    curs = conn.cursor()
    curs.execute('USE %s' %DB)

    return curs, engine, session


def initialize():
    curs = cursor()[0]
    curs.execute("SET FOREIGN_KEY_CHECKS = 0;")
    curs.close()
    curs = cursor()[0]
    # delete = '''TRUNCATE TABLE BaseMovieInfo'''
    delete = '''DELETE FROM BaseMovieInfo'''
    curs.execute(delete)
    curs.close()
    curs = cursor()[0]
    curs.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("초기화완료!")
