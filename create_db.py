from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql
import connections as cnnt
import warnings


user, password, host, port, DB = cnnt.aws_basic_info()
engine = cnnt.mk_engine()
session = cnnt.mk_session()
conn = pymysql.connect(host=host, user=user, password=password,  charset='utf8')
curs = conn.cursor()


sql ="create database if not exists DBtoday;"
with warnings.catch_warnings():
    warnings.simplefilter("error", category = pymysql.Warning)
    try:
        curs.execute(sql)
    except Exception as e :
        print("에러메시지 : ",e)
    finally:
        conn.commit()
        use_DB = "USE DBtoday"
        curs.execute(use_DB)
        change_charset = "ALTER SCHEMA DEFAULT CHARACTER SET 'utf8'"
        curs.execute(change_charset)
        conn.commit()
        conn.close()
        print("Altered DB")
