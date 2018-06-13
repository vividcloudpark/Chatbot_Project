from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import json
import connections as cnnt
from flask_models import *
import datetime


def get_source(url):
    html = urlopen(url)
    source = html.read()
    html.close()
    return source

def score(soup,i):
    res = soup.find_all('div', 'star_score')[i].find_all("em")
    viewer_score = []
    for i in res:
        viewer_score.append(i.get_text())
    a = "".join(viewer_score)
    if len(a) != 0:
        return a
    else:
        return None

def get_code(link):
    a = link.split("=")
    code = a[-1]
    return code

def delete_exceptioanl_text(content):
    getout = ['\r','\n','\t']
    result=[]
    content = list(content)
    for i in content:
        if i not in getout:
            result.append(i)
    result = "".join(result)
    return result

def replace_detail(content):
    content=list(content)
    result=[]
    getout = ['\r', '\xa0']
    for i in content:
        if i not in getout:
            result.append(i)
        else:
            result.append("\n")
    result = "".join(result)
    return result


def make_craw_list(selector):
    if selector == "op":
        link = "https://movie.naver.com/movie/running/current.nhn?view=list&tab=normal&order=open"
    elif selector == "pre":
        link = "https://movie.naver.com/movie/running/premovie.nhn"
    soup = BeautifulSoup(get_source(link), "lxml")
    res = soup.find_all('dl', 'lst_dsc')
    to_craw_list = []
    for i in range(len(res)):
        moviename = res[i].a.string
        movielink = res[i].a.get('href')
        moviecode = get_code(movielink)
        temp_opendate = delete_exceptioanl_text(res[i].find("dl", "info_txt1").find("dd").get_text()).split("|")[-1]
        opendate = temp_opendate.replace(" 개봉", "")
        to_craw_list.append(moviecode)
    return to_craw_list


def make_list(soup, number):
    base = soup.find("dl", "info_spec").find_all("dd")[0].find_all('span')[number].find_all('a')
    textlist = []
    for i in range(len(base)):
        text = base[i].get_text()
        textlist.append(text)
    return textlist


def get_by_moviecode(moviecode):
    movieurl = f"https://movie.naver.com/movie/bi/mi/basic.nhn?code={moviecode}"
    soup = BeautifulSoup(get_source(movieurl), "lxml")
    a = get_movie_info(moviecode, soup)
    return a

def get_movie_info(moviecode, soup):
    #이름
    kor_nm = soup.find('h3', 'h_movie').find("a").get_text()
    tempengname = soup.find_all('strong', 'h_movie2')[1].get_text()
    if len(tempengname)>45:
        eng_nm = tempengname[:45]
        produce_year = 9999
    else:
        eng_nm = tempengname[:-6]
        produce_year = tempengname[-4:]


    #평점
    try:
        giza = len(soup.find(class_="main_score").find_all('div', 'star_score'))
        if giza == 4: #기레기없을때
            viewer_score = score(soup, 0)
            ntz_score = score(soup, 1)
            giza_score = None

        elif giza == 5:
            viewer_score = score(soup, 0)
            giza_score = score(soup, 1)
            ntz_score = score(soup, 2)
    except:
        viewer_score = None
        giza_score = None
        ntz_score = None

    #영화 줄거리
    try:
        story = soup.find('h5', 'h_tx_story').get_text()
    except:
        story = None

    #영화 detail
    try:
        story_detail = soup.find('p', 'con_tx').get_text()
        story_detail = replace_detail(story_detail)
    except:
        story_detail = None



    #장르리스트
    try:
        genre_list = make_list(soup, 0)
    except:
        genre_list = ["장르정보없음"]

    try:
        nation_list = make_list(soup, 1)
    except:
        nation_list = ["국가정보없음"]

    #개봉일
    try:
        open_date = "".join(make_list(soup, 3)).strip()
        print(len(open_date))
        status = 1
        if len(open_date)>10:
            open_date = open_date.split(" ")[1]
            open_date = datetime.datetime.strptime(open_date, '%Y.%m.%d').date()
        elif len(open_date)<10:
            status = "nonpass"
    except:
        status = "nonpass"

    #감독
    try:
        director = soup.find("dl", "info_spec").find_all("dd")[1].get_text()
        directorcode = get_code(soup.find("dl", "info_spec").find_all("dd")[1].a.get('href'))
    except:
        directorcode = -9999
        director = "감독정보가 없습니다"

    #배우 그리고 배우코드
    actordict={}
    try:
        base = soup.find("dl", "info_spec").find_all("dd")[2].find_all('a')

        for i in range(len(base)-1):
            actor = soup.find("dl", "info_spec").find_all("dd")[2].find_all('a')[i].get_text()
            actor_code = get_code(soup.find("dl", "info_spec").find_all("dd")[2].find_all('a')[i].get('href'))
            actordict.update({actor_code : actor})
    except:
        actordict.update({-9999 : "None"})


    #관람등급
    try:
        flim_class = soup.find("dl", "info_spec").find_all("dd")[3].find('a').get_text()
    except:
        flim_class = None
    # session = cnnt.mk_session()
    # curs = cnnt.mk_cursor()

    # pk들 넣기
    if status != "nonpass":
        codeofmovie = BaseMovieInfo(moviecode, kor_nm)
        db.session.merge(codeofmovie)
        codeofdirector = Director(directorcode, director)
        db.session.merge(codeofdirector)
        for actorcode in actordict:
            c = Actors(actorcode, actordict[actorcode])
            db.session.merge(c)
        for genre in genre_list:
            genrecode = Genre(genre)
            db.session.merge(genrecode)
        for nation in nation_list:
            nations = Nations(nation)
            db.session.merge(nations)
        db.session.commit()
        db.session.close()


        for actorcode in actordict:
            movieandactor = ActorsOfMovie(moviecode, actorcode)
            db.session.merge(movieandactor)
        for genre in genre_list:
            movieandgenre = GenreOfMovie(moviecode, genre)
            db.session.merge(movieandgenre)
        for nation in nation_list:
            movieandnation = NationOfMovie(moviecode, nation)
            db.session.merge(movieandnation)
        db.session.commit()
        db.session.close()
        moviescore = MovieScore(moviecode, viewer_score, giza_score, ntz_score)
        directorandmovie = DirectorOfMovie(moviecode, directorcode)
        detail = DetailedBaseMovieInfo(moviecode, open_date, eng_nm, produce_year, flim_class, story, story_detail)

        db.session.merge(moviescore)
        db.session.merge(directorandmovie)
        db.session.merge(detail)
        db.session.commit()
        db.session.close()
        print(moviecode, open_date, "데이터베이스에 저장 완료!")
# 추가될정보
# 1.장르정보
# 2.국가정보
# 3.등급정보
# 4.누적관객수 << 현아가 가져온 정보에서 더하는게 나을지.. 흠...
# 5.영화 줄거리
# 6.영화 줄거리 (디테일)

# 인물테이블
# 1.인물 id(숫자)
# 인물 특성 (배우/감독)

# 영화 수상테이블
# 1.영화id (fk)
# 2.수상명

def get_by_peoplecode(peoplecode):
    peopleurl = f"https://movie.naver.com/movie/bi/pi/basic.nhn?code={peoplecode}"
    soup = BeautifulSoup(get_source(peopleurl), "lxml") # 파싱할 문서를 BeautifulSoup 클래스의 생성자에 넘겨주어 문서 개체를 생성, 관습적으로 soup 이라 부름
    a = get_people_info(peoplecode, soup)
    return soup

def get_people_info(peoplecode, soup):
    infobox = soup.find(class_="mv_info character")
    people_name = infobox.a.get_text()
    people_link = get_code(infobox.a.get('href'))
    print(people_name, people_link)
    pilmobox = soup.find(class_="lst_pilmo")
    pilmos = pilmobox.find_all(class_="pilmo_info")


    for i in pilmos:
        kor_nm = delete_exceptioanl_text(i.find(class_="pilmo_tit").a.get_text())

        movie_code = get_code(i.find(class_="pilmo_tit").a.get('href'))
        year = i.find("p", "pilmo_genre").a.get_text()

        if int(year) < 2019:
            ntz_score = i.find(class_="star_score").get_text()
            ntz_score = delete_exceptioanl_text(ntz_score)
        else:
            ntz_score = None

        print(movie_code, kor_nm, ntz_score)

# try:
#     addtional = soup.find(class_="awarded")
#     print(addtional.find_all("td"))
# #     print(addtional.find_all(class_="award_wrap"))
# except:
#     print("수상 데이터가없습니다")
