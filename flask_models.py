import pymysql
import datetime
import connections as cnnt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


user, password, host, port, DB = cnnt.aws_basic_info()

target = f'mysql+pymysql://{user}:{password}@{host}:{port}/{DB}?charset=utf8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = target
db = SQLAlchemy(app)

class BaseMovieInfo(db.Model):
    __tablename__ = 'BaseMovieInfo'
    movie_code = db.Column(db.String(10), primary_key = True,  nullable=False)
    movie_name_kor = db.Column(db.String(50), nullable=False)

    db.UniqueConstraint('movie_code', name='code_should_unique')

    def __init__(self, movie_code, movie_name_kor ):
        self.movie_code =movie_code
        self.movie_name_kor =movie_name_kor


class DetailedBaseMovieInfo(db.Model):
    __tablename__ = 'DetailedBaseMovieInfo'
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"),primary_key = True)
    opendate = db.Column(db.Date, nullable=True)
    movie_name_eng = db.Column(db.String(100), nullable=True)
    produce_year = db.Column(db.String(5), nullable=True)
    flim_class = db.Column(db.String(100), nullable=True)
    story = db.Column(db.Text, nullable=True)
    story_detail = db.Column(db.Text,  nullable=True)

    detail_with_movie = db.relationship('BaseMovieInfo', backref=db.backref('DetailedBaseMovieInfo', lazy=True))

    def __init__(self,  movie_code, opendate, movie_name_eng, produce_year, flim_class, story, story_detail):
        self.movie_code = movie_code
        self.opendate =opendate
        self.movie_name_eng = movie_name_eng
        self.produce_year = produce_year
        self.flim_class = flim_class
        self.story = story
        self.story_detail = story_detail


class MovieScore(db.Model):
    __tablename__ = 'MovieScore'
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"), primary_key = True)
    viewer_score = db.Column(db.Float, nullable=True)
    giza_score = db.Column(db.Float, nullable=True)
    ntz_score = db.Column(db.Float, nullable=True)

    score_with_movie = db.relationship('BaseMovieInfo', backref=db.backref('MovieScore', lazy=True))


    def __init__(self, movie_code, viewer_score, giza_score, ntz_score):
        self.movie_code = movie_code
        self.viewer_score = viewer_score
        self.giza_score = giza_score
        self.ntz_score = ntz_score

class GenreOfMovie(db.Model):
    __tablename__ = 'GenreOfMovie'
    index = db.Column(db.Integer, primary_key = True)
    # movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code', onupdate="CASCADE", ondelete="CASCADE"))
    # movie_genre = db.Column(db.String(20), db.ForeignKey('Genre.genre', onupdate="CASCADE", ondelete="CASCADE"))
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code'))
    movie_genre = db.Column(db.String(20), db.ForeignKey('Genre.genre'))

    moviecode_of_genre_with_movie = db.relationship('BaseMovieInfo', backref=db.backref('GenreOfMovie', cascade="all, delete-orphan"))
    genrecode_of_genre_with_moive = db.relationship('Genre', backref=db.backref('GenreOfMovie', cascade="all, delete-orphan"))

    def __init__(self, movie_code, movie_genre):
        self.movie_code = movie_code
        self.movie_genre = movie_genre

class Genre(db.Model):
    __tablename__ = 'Genre'
    genre = db.Column(db.String(20), primary_key = True, unique=True)
    def __init__(self, genre):
        self.genre = genre

class NationOfMovie(db.Model):
    __tablename__ = 'NationOfMovie'
    index = db.Column(db.Integer, primary_key = True)
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code'))
    movie_nation = db.Column(db.String(20), db.ForeignKey('Nations.nations'))

    moviecode_of_nation = db.relationship('BaseMovieInfo', backref=db.backref('NationOfMovie', cascade="all, delete-orphan"))
    nationcode_of_nation = db.relationship('Nations', backref=db.backref('NationOfMovie', cascade="all, delete-orphan"))


    def __init__(self, movie_code, movie_genre):
        self.movie_code = movie_code
        self.movie_genre = movie_genre

class Nations(db.Model):
    __tablename__ = 'Nations'
    nations = db.Column(db.String(20), primary_key = True, unique=True)
    def __init__(self, nations):
        self.nations = nations


class DirectorOfMovie(db.Model):
    __tablename__ = 'DirectorOfMovie'
    index = db.Column(db.Integer, primary_key = True)
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code'))
    movie_director_code = db.Column(db.String(10), db.ForeignKey('Director.director_code'))
    moviecode_of_director = db.relationship('BaseMovieInfo', backref=db.backref('DirectorOfMovie', cascade="all, delete-orphan"))
    directorcode_of_director = db.relationship('Director', backref=db.backref('DirectorOfMovie', cascade="all, delete-orphan"))


    def __init__(self, movie_code, movie_director_code):
        self.movie_code = movie_code
        self.movie_director_code = movie_director_code


class Director(db.Model):
    __tablename__ = 'Director'
    director_code = db.Column(db.String(10), nullable=False, primary_key=True)
    director_name_kor = db.Column(db.String(50), nullable=False)

    def __init__(self, director_code, director_name_kor):
        self.director_code = director_code
        self.director_name_kor = director_name_kor

class ActorsOfMovie(db.Model):
    __tablename__ = 'ActorsOfMovie'
    index = db.Column(db.Integer, primary_key = True)
    movie_code = db.Column(db.String(10), db.ForeignKey('BaseMovieInfo.movie_code'))
    movie_actor_code = db.Column(db.String(50), db.ForeignKey('Actors.actor_code'))

    moviecode_of_actor = db.relationship('BaseMovieInfo', backref=db.backref('ActorsOfMovie', cascade="all, delete-orphan"))
    actorcode_of_actor = db.relationship('Actors', backref=db.backref('ActorsOfMovie', cascade="all, delete-orphan"))


    def __init__(self, movie_code, movie_actor_code):
        self.movie_code = movie_code
        self.movie_actor_code = movie_actor_code

class Actors(db.Model):
    __tablename__ = 'Actors'
    actor_code = db.Column(db.String(10), nullable=False, primary_key=True)
    actor_name_kor = db.Column(db.String(50), nullable=False)

    def __init__(self, actor_code, actor_name_kor):
        self.actor_code = actor_code
        self.actor_name_kor = actor_name_kor


class KobisMovieInfo(db.Model):
    __tablename__ = 'KobisMovieInfo'
    index = db.Column(db.Integer, primary_key = True, autoincrement=True)
    movie_name = db.Column(db.String(50), primary_key = True)
    search_date = db.Column(db.Date)
    today_audi = db.Column(db.Integer)

    def __init__(self,movie_name,search_date,today_audi):
        self.movie_name =movie_name
        self.search_date =search_date
        self.today_audi =today_audi

class KakaoMessage(db.Model):
    __tablename__ = 'KakaoMessage'
    index = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_key = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.now())
    message = db.Column(db.Text)

    def __init__(self, user_key, message):
        self.user_key = user_key
        self.message = message
