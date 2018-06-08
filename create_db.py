from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql
from models import *



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


try:
    sql ="create database if not exists DBtoday;"
    curs.execute(sql)
    use_DB = "USE DBtoday"
    curs.execute(use_DB)
    change_charset = "ALTER SCHEMA DEFAULT CHARACTER SET 'utf8'"
    curs.execute(change_charset)
    Base.metadata.create_all(engine)

    session.commit()
    session.close()

except:
    print("에러, DB를 삭제하고 다시 시도해주세요!")
