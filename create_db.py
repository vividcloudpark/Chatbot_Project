from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql
from models import *
import connections as cnnt




user, password, host, port, DB = cnnt.local_baic_info()
# user, password, host, port, DB = aws_basic_info()
engine = cnnt.mk_engine()
session = cnnt.mk_session()
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
