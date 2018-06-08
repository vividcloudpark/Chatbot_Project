from sqlalchemy import Column, String, Float, Integer, Boolean, Date, Table, ForeignKey, Sequence, Text, UniqueConstraint,ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pymysql

Base = declarative_base()
#
# DirectorOfMovie = Table('DirectorOfMovie', Base.metadata,
# Column('movie_director_code', String(10), ForeignKey("Director.director_code")),
# Column('movie_code', String(10), ForeignKey('BaseMovieInfo.movie_code')))
#
#
# ActorsOfMovie = Table('ActorsOfMovie', Base.metadata, Column('movie_code', String(10), ForeignKey("BaseMovieInfo.movie_code")),
# Column('movie_actor_code', String(10), ForeignKey('Actors.actor_code')))


class BaseMovieInfo(Base):
    __tablename__ = 'BaseMovieInfo'
    movie_code = Column(String(10), primary_key = True,  nullable=False)
    movie_name_kor = Column(String(50), nullable=False)
    UniqueConstraint('movie_code', name='code_should_unique')

    def __init__(self, movie_code, movie_name_kor):
        self.movie_code =movie_code
        self.movie_name_kor =movie_name_kor

class DetailedBaseMovieInfo(Base):
    __tablename__ = 'DetailedBaseMovieInfo'
    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code'))
    movie_name_eng = Column(String(100), nullable=True)
    produce_year = Column(String(5), nullable=True)
    genre_list = Column(String(255))
    nation_list = Column(String(100))
    flim_class = Column(String(100), nullable=True)
    story = Column(Text)
    story_detail = Column(Text)

    movieanddetail = relationship("BaseMovieInfo", backref = "DetailedBaseMovieInfo")

    __table_args__ =(
    ForeignKeyConstraint(
    ['movie_code'],
    ['BaseMovieInfo.movie_code'],
    onupdate="CASCADE", ondelete="CASCADE"),
    )


    def __init__(self, movie_code, movie_name_eng, produce_year, genre_list, nation_list, flim_class, story, story_detail):
        self.movie_code = movie_code
        self.movie_name_eng = movie_name_eng
        self.produce_year = produce_year
        self.genre_list = genre_list
        self.nation_list = nation_list
        self.flim_class = flim_class
        self.story = story
        self.story_detail = story_detail


class MovieScore(Base):
    __tablename__ = 'MovieScore'

    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code'))
    viewer_score = Column(Float, nullable=True)
    giza_score = Column(Float, nullable=True)
    ntz_score = Column(Float, nullable=True)

    movie_and_score = relationship("BaseMovieInfo", backref = "MovieScore")

    __table_args__ =(
    ForeignKeyConstraint(
    ['movie_code'],
    ['BaseMovieInfo.movie_code'],
    onupdate="CASCADE", ondelete="CASCADE"),)

    def __init__(self, movie_code, viewer_score, giza_score, ntz_score):
        self.movie_code = movie_code
        self.viewer_score = viewer_score
        self.giza_score = giza_score
        self.ntz_score = ntz_score


class DirectorOfMovie(Base):
    __tablename__ = 'DirectorOfMovie'

    index = Column(Integer, primary_key = True)
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code'))
    movie_director_code = Column(String(10), ForeignKey('Director.director_code'))


    director_moviecode_connetion = relationship("BaseMovieInfo", backref = "DirectorOfMovie")
    directorcode_connection = relationship("Director", backref = "DirectorOfMovie")


    # __table_args__ =(
    # ForeignKeyConstraint(
    # ['movie_code', 'movie_director_code'],
    # ['BaseMovieInfo.movie_code', 'Director.director_code'],
    # onupdate="CASCADE", ondelete="CASCADE"),)

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
    movie_code = Column(String(10), ForeignKey('BaseMovieInfo.movie_code'))
    movie_actor_code = Column(String(50), ForeignKey('Actors.actor_code'))


    actor_moviecode_connetion = relationship("BaseMovieInfo", backref = "ActorsOfMovie")
    actorcode_connection = relationship("Actors", backref = "ActorsOfMovie")

    # __table_args__ =(
    # ForeignKeyConstraint(
    # ['movie_code', 'movie_actor_code'],
    # ['BaseMovieInfo.movie_code', 'Actors.actor_code'],
    # onupdate="CASCADE", ondelete="CASCADE"),)

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
    index = Column(Integer, primary_key = True)
    movie_name = Column(String(50), primary_key = True)
    search_date = Column(Date)
    today_audi = Column(Integer)
    def __init__(self,movie_name,search_date,today_audi):
        self.movie_name =movie_name
        self.search_date =search_date
        self.today_audi =today_audi
