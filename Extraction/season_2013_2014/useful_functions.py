import urllib.request
from bs4 import BeautifulSoup
import re
from selenium import webdriver


championat_statto = {'Астон Вилла': 'Aston Villa',
                     'Манчестер Сити': 'Manchester City',
                     'Тоттенхэм Хотспур': 'Tottenham Hotspur',
                     'Вест Бромвич Альбион': 'West Bromwich Albion',
                     'Эвертон': 'Everton',
                     'Ньюкасл Юнайтед': 'Newcastle United',
                     'Вест Хэм Юнайтед': 'West Ham United',
                     'Сандерленд': 'Sunderland',
                     'Челси': 'Chelsea',
                     'Уиган Атлетик': 'Wigan Athletic',
                     'Суонси Сити': 'Swansea City',
                     'Сток Сити': 'Stoke City',
                     'Фулхэм': 'Fulham',
                     'Арсенал': 'Arsenal',
                     'Куинз Парк Рейнджерс': 'Queens Park Rangers',
                     'Ливерпуль': 'Liverpool',
                     'Норвич Сити': 'Norwich City',
                     'Манчестер Юнайтед': 'Manchester United',
                     'Рединг': 'Reading',
                     'Саутгемптон': 'Southampton',
                     'Халл Сити': 'Hull City',
                     'Кардифф Сити': 'Cardiff City',
                     'Кристал Пэлас': 'Crystal Palace'
                     }


def get_soup(url="http://www.championat.com/football/_england/773/result.html"):
    """Gets soup from url"""
    sock = urllib.request.urlopen(url)
    full_html = sock.read()
    sock.close()
    soup = BeautifulSoup(full_html)
    return soup


def get_results(soup):
    """Gets match result from match soup"""
    score = soup.find(attrs={'class': 'match__count__main'}).text
    score = re.findall(r'\d+', score)
    res = []
    if score[0] > score[1]:
        res.append(1)
    elif score[0] == score[1]:
        res.append(0.5)
    else:
        res.append(0)
    return res


def get_names(soup):
    """Gets team names from match soup"""
    res = []
    for i in soup.findAll(attrs={'class': 'match__team__name'}):
        res.append(i.text)
    return res


def get_date(soup):
    """Getting match date"""
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date = soup.find(attrs={'class': "match__autoupdate-block-1"})
    date = date.find(attrs={'class': "match__info"}).text
    day, month, year = date.split(',')[0].split()
    month = months.index(month) + 1
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    res = str(day) + '.' + month + '.' + year
    return res


def get_statto_soup(driver, date, url="http://www.statto.com/football/stats/england/premier-league/2013-2014/table"):
    """Dealing with statto shitty paging"""
    driver.get(url)
    element = driver.find_element_by_class_name('dates')
    all_options = element.find_elements_by_tag_name("option")
    pred = None
    for option in all_options:
        if option.get_attribute("text") == date:
                pred.click()
                break
        pred = option
    res = driver.page_source
    res = BeautifulSoup(res)
    return res


def get_statto_teams_info(team1, team2, statto, simple=True):
    """Getting statto info soup of 2 soups + first + last"""
    statto = statto.findAll('form')[1].findAll('tr')
    first, last = None, None
    values = [0, 0]
    goals = []
    for cnt, team in enumerate(statto):
        if cnt < 2:
            continue
        if cnt == 2:
            first = team
        if cnt == len(statto) - 1:
            last = team
        goals.append((int(team.findAll(text=re.compile('[0-9]+'))[-2]), team))
        if re.search(team1, team.text):
            values[0] = team
        elif re.search(team2, team.text):
            values[1] = team
    first_goals = max(goals, key=lambda x: x[0])[1]
    last_goals = min(goals, key=lambda x: x[0])[1]
    return values[0], values[1], first, last, first_goals, last_goals


def get_statto_teams_pos_diff(soup1, soup2):
    """Getting pos difference from statto by 2 soups"""
    pos1 = int(soup1.findAll(text=re.compile('[0-9]+'))[0])
    pos2 = int(soup2.findAll(text=re.compile('[0-9]+'))[0])
    return pos1 - pos2


def get_statto_score(soup):
    """Getting team score from statto by soup"""
    return int(soup.findAll(text=re.compile('[0-9]+'))[-1])


def get_tour_number(soup):
    """Gets tour number by soup"""
    texts = [i.text for i in soup.findAll('div', attrs={'class' : 'match__info'})]
    text = list(filter(lambda x: re.search('тур', x), texts))[0]
    text = text.split('-')[0].split()[-1]
    return int(text)


class ChromeDriver:
    """Chrome driver"""
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self.driver

    def __exit__(self, *exc_info):
        self.driver.close()