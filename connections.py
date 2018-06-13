from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql

def local_baic_info():
    data=open("config.json").read()
    json_data = json.loads(data)

    user = json_data["users"][0]["user"]
    password = json_data["users"][0]["password"]
    host = json_data["users"][0]["host"]
    port = json_data["users"][0]["port"]
    DB = json_data["users"][0]["DB"]
    return user, password, host, port, DB

def aws_basic_info():
    data=open("config.json").read()
    json_data = json.loads(data)

    user = json_data["aws"]["user"]
    port = json_data["users"][0]["port"]
    DB = json_data["users"][0]["DB"]
    aws_password=json_data["aws"]["awspassword"]
    aws_host=json_data["aws"]["awshost"]
    return user, aws_password, aws_host, port, DB


def mk_engine():
    user, password, host, port, DB = aws_basic_info()
    # user, password, host, port, DB = aws_basic_info()

    target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'
    engine = create_engine(target, encoding = "utf-8")
    return engine


def mk_session():
    engine = mk_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def mk_cursor():
    user, password, host, port, DB = aws_basic_info()
    # user, password, host, port, DB = aws_basic_info()
    session = mk_session()
    conn = pymysql.connect(host=host, user=user, password=password,  charset='utf8')
    curs = conn.cursor()
    curs.execute('USE %s' %DB)
    return curs


def initialize():
    curs = mk_cursor()
    curs.execute("SET FOREIGN_KEY_CHECKS = 0;")
    curs.close()
    curs = mk_cursor()
    # delete = '''TRUNCATE TABLE BaseMovieInfo'''
    delete = '''DELETE FROM BaseMovieInfo'''
    curs.execute(delete)
    curs.close()
    curs = mk_cursor()
    curs.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("초기화완료!")
