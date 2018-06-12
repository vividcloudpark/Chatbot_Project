from sqlalchemy import Column, String, Float, Integer, Boolean, Date, Table, ForeignKey, Sequence, DateTime, Text, UniqueConstraint,ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql
import datetime
import connections as cnnt

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


user, password, host, port, DB = cnnt.aws_basic_info()

target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'

app.config['SQLALCHEMY_DATABASE_URI'] = target
db = SQLAlchemy(app)

Base = declarative_base()


class BaseMovieInfo(Base):
    __tablename__ = 'BaseMovieInfo'
    movie_code = Column(String(10), primary_key = True,  nullable=False)
    movie_name_kor = Column(String(50), nullable=False)

    UniqueConstraint('movie_code', name='code_should_unique')

    def __init__(self, movie_code, movie_name_kor ):
        self.movie_code =movie_code
        self.movie_name_kor =movie_name_kor


class DetailedBaseMovieInfo(Base):
    __tablename__ = 'DetailedBaseMovieInfo'
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"),primary_key = True)
    opendate = Column(Date, nullable=True)
    movie_name_eng = Column(String(100), nullable=True)
    produce_year = Column(String(5), nullable=True)
    flim_class = Column(String(100), nullable=True)
    story = Column(Text, nullable=True)
    story_detail = Column(Text,  nullable=True)
    def __init__(self,  movie_code, opendate, movie_name_eng, produce_year, flim_class, story, story_detail):
        self.movie_code = movie_code
        self.opendate =opendate
        self.movie_name_eng = movie_name_eng
        self.produce_year = produce_year
        self.flim_class = flim_class
        self.story = story
        self.story_detail = story_detail


class MovieScore(Base):
    __tablename__ = 'MovieScore'
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"), primary_key = True)
    viewer_score = Column(Float, nullable=True)
    giza_score = Column(Float, nullable=True)
    ntz_score = Column(Float, nullable=True)

    def __init__(self, movie_code, viewer_score, giza_score, ntz_score):
        self.movie_code = movie_code
        self.viewer_score = viewer_score
        self.giza_score = giza_score
        self.ntz_score = ntz_score

class GenreOfMovie(Base):
    __tablename__ = 'GenreOfMovie'
    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"))
    movie_genre = Column(String(20), ForeignKey('Genre.genre', onupdate="CASCADE", ondelete="CASCADE"))
    def __init__(self, movie_code, movie_genre):
        self.movie_code = movie_code
        self.movie_genre = movie_genre

class Genre(Base):
    __tablename__ = 'Genre'
    genre = Column(String(20), primary_key = True, unique=True)
    def __init__(self, genre):
        self.genre = genre

class NationOfMovie(Base):
    __tablename__ = 'NationOfMovie'
    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"))
    movie_nation = Column(String(20), ForeignKey('Nations.nations', onupdate="CASCADE", ondelete="CASCADE"))
    def __init__(self, movie_code, movie_genre):
        self.movie_code = movie_code
        self.movie_genre = movie_genre

class Nations(Base):
    __tablename__ = 'Nations'
    nations = Column(String(20), primary_key = True, unique=True)
    def __init__(self, nations):
        self.nations = nations


class DirectorOfMovie(Base):
    __tablename__ = 'DirectorOfMovie'
    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"))
    movie_director_code = Column(String(10), ForeignKey('Director.director_code', onupdate="CASCADE", ondelete="CASCADE"))

    def __init__(self, movie_code, movie_director_code):
        self.movie_code = movie_code
        self.movie_director_code = movie_director_code


class Director(Base):
    __tablename__ = 'Director'
    director_code = Column(String(10), nullable=False, primary_key=True)
    director_name_kor = Column(String(50), nullable=False)

    def __init__(self, director_code, director_name_kor):
        self.director_code = director_code
        self.director_name_kor = director_name_kor

class ActorsOfMovie(Base):
    __tablename__ = 'ActorsOfMovie'
    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"))
    movie_actor_code = Column(String(50), ForeignKey('Actors.actor_code', onupdate="CASCADE", ondelete="CASCADE"))

    def __init__(self, movie_code, movie_actor_code):
        self.movie_code = movie_code
        self.movie_actor_code = movie_actor_code

class Actors(Base):
    __tablename__ = 'Actors'
    actor_code = Column(String(10), nullable=False, primary_key=True)
    actor_name_kor = Column(String(50), nullable=False)

    def __init__(self, actor_code, actor_name_kor):
        self.actor_code = actor_code
        self.actor_name_kor = actor_name_kor


class KobisMovieInfo(Base):
    __tablename__ = 'KobisMovieInfo'
    index = Column(Integer, primary_key = True, autoincrement=True)
    movie_name = Column(String(50), primary_key = True)
    search_date = Column(Date)
    today_audi = Column(Integer)

    def __init__(self,movie_name,search_date,today_audi):
        self.movie_name =movie_name
        self.search_date =search_date
        self.today_audi =today_audi

class KakaoMessage(Base):
    __tablename__ = 'KakaoMessage'
    index = Column(Integer, primary_key = True, autoincrement=True)
    user_key = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    message = Column(Text)

    def __init__(self, user_key, message):
        self.user_key = user_key
        self.message = message
